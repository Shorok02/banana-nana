import os
import tempfile
import uuid
from typing import Tuple, List
from sqlalchemy.exc import SQLAlchemyError

# keep your existing imports
import chromadb
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import FileModel

# IMPORTANT: import your Session factory (adjust name/path to match your project)
from database import SessionLocal  # <- SessionLocal() yields new Session

# Factory functions (keep or adjust)
def get_chroma_client():
    return chromadb.PersistentClient(path="chromadb_data")

def get_chroma_collection():
    client = get_chroma_client()
    return client.get_or_create_collection(name="file_chunks")

def get_embedding_model():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def extract_text_from_bytes(data: bytes, filename: str) -> Tuple[str, str]:
    filename_l = filename.lower()
    file_type = "txt"
    content = ""
    # Note: these read from bytes, not from UploadFile.file (we saved a bytes buffer)
    if filename_l.endswith(".txt"):
        content = data.decode("utf-8", errors="replace")
        file_type = "txt"
    elif filename_l.endswith(".pdf"):
        import fitz
        doc = fitz.open(stream=data, filetype="pdf")
        content = "\n".join([page.get_text() for page in doc])
        file_type = "pdf"
    elif filename_l.endswith(".docx"):
        import io, docx
        doc = docx.Document(io.BytesIO(data))
        content = "\n".join([p.text for p in doc.paragraphs])
        file_type = "docx"
    else:
        raise ValueError("Unsupported file type")
    return content, file_type


def process_file_upload_sync(file_bytes: bytes, filename: str) -> dict:
    """
    Synchronous, thread-safe processing function you can call from BackgroundTasks
    or run in a thread via asyncio.to_thread.
    - Creates its own DB session (SessionLocal).
    - Creates embedding model/collection inside the thread for thread-safety.
    """
    # Create resources inside the worker thread
    embedding_model = get_embedding_model()
    collection = get_chroma_collection()

    file_id = str(uuid.uuid4())
    db = SessionLocal()
    try:
        # 1. Extract text
        content, file_type = extract_text_from_bytes(file_bytes, filename)

        # 2. Chunk text (you can refine afterward)
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_text(content)

        # 3. IDs + metadata
        chunk_ids = [str(uuid.uuid4()) for _ in chunks]
        chunk_metadatas = [
            {
                "file_id": file_id,
                "filename": filename,
                "chunk_index": idx
            }
            for idx in range(len(chunks))
        ]

        # 4. Batch embeddings - use embed_documents if available or embed_query in list form
        # HuggingFaceEmbeddings (langchain wrapper) may expose embed_documents or embed_query; try embed_documents first
        try:
            chunk_embeddings = embedding_model.embed_documents(chunks) 
            print("Batch embedding completed")  # batch
        except AttributeError:
            # fallback to per-chunk (still ok but slower)
            chunk_embeddings = [embedding_model.embed_query(c) for c in chunks]

        # 5. Add to Chroma
        try:
            collection.add(
                documents=chunks,
                metadatas=chunk_metadatas,
                ids=chunk_ids,
                embeddings=chunk_embeddings
            )
        except Exception as e:
            # If vectorstore add failed, do not commit DB
            raise

        # 6. Save file metadata to DB (create and commit)
        try:
            db_file = FileModel(
                id=file_id,
                filename=filename,
                filetype=file_type,
                size_bytes=len(file_bytes),
                chunks_count=len(chunks),
                embeddings_count=len(chunks),
                status="embedded"
            )
            db.add(db_file)
            db.commit()
        except SQLAlchemyError as e:
            # DB commit failed -> best-effort cleanup in Chroma: remove the chunk ids
            try:
                collection.delete(ids=chunk_ids)
            except Exception:
                pass
            db.rollback()
            raise

        return {"file_id": file_id, "chunks_count": len(chunks), "status": "processed"}

    finally:
        db.close()

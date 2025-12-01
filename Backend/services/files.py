import uuid
from typing import List, Tuple
from sqlalchemy.orm import Session
from database import SessionLocal
from models import FileModel
from langchain_text_splitters import RecursiveCharacterTextSplitter


from clients.embedding_client import get_hf_embeddings as get_embedding_model
from clients.vectordb_client import get_collection as get_chroma_collection




# ------------------------------
# Step 1: Extract text
# ------------------------------
def extract_text_from_bytes(data: bytes, filename: str) -> Tuple[str, str]:
    filename_l = filename.lower()
    if filename_l.endswith(".txt"):
        return data.decode("utf-8", errors="replace"), "txt"
    elif filename_l.endswith(".pdf"):
        import fitz
        doc = fitz.open(stream=data, filetype="pdf")
        return "\n".join([p.get_text() for p in doc]), "pdf"
    elif filename_l.endswith(".docx"):
        import io, docx
        doc = docx.Document(io.BytesIO(data))
        return "\n".join([p.text for p in doc.paragraphs]), "docx"
    else:
        raise ValueError("Unsupported file type")

# ------------------------------
# Step 2: Split into chunks
# ------------------------------
def split_text_chunks(content: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.split_text(content)

# ------------------------------
# Step 3: Create metadata
# ------------------------------
def create_chunk_metadatas(file_id: str, filename: str, chunks: List[str], user_id: str):
    return [{"file_id": file_id, "filename": filename, "chunk_index": idx, "user_id": user_id} for idx in range(len(chunks))]

# ------------------------------
# Step 4: Embed chunks
# ------------------------------
def embed_chunks(chunks: List[str]):
    model = get_embedding_model()
    try:
        return model.embed_documents(chunks)
    except AttributeError:
        return [model.embed_query(c) for c in chunks]

# ------------------------------
# Step 5: Store in Chroma
# ------------------------------
def store_chunks_in_chroma(chunks: List[str], metadatas: List[dict], embeddings: List[List[float]]):
    collection = get_chroma_collection()
    ids = [str(uuid.uuid4()) for _ in chunks]
    collection.add(documents=chunks, metadatas=metadatas, embeddings=embeddings, ids=ids)
    return ids

# ------------------------------
# Step 6: Save file metadata in DB
# ------------------------------

def save_file_metadata(user_id: str, filename: str, file_type: str, size: int, chunks_count: int) -> str:
    db = SessionLocal()
    file_id = str(uuid.uuid4())
    db_file = FileModel(
        id=file_id,
        user_id=user_id,  # NEW
        filename=filename,
        filetype=file_type,
        size_bytes=size,
        chunks_count=chunks_count,
        embeddings_count=chunks_count,
        status="embedded"
    )
    db.add(db_file)
    db.commit()
    db.close()
    return file_id

# ------------------------------
# Main processing function
# ------------------------------
def process_file_upload_sync(file_bytes: bytes, filename: str, user_id: str) -> dict:
    content, file_type = extract_text_from_bytes(file_bytes, filename)
    chunks = split_text_chunks(content)
    file_id = str(uuid.uuid4())
    metadatas = create_chunk_metadatas(file_id, filename, chunks, user_id)
    embeddings = embed_chunks(chunks)
    store_chunks_in_chroma(chunks, metadatas, embeddings)
    save_file_metadata(user_id, filename, file_type, len(file_bytes), len(chunks))
    return {"file_id": file_id, "chunks_count": len(chunks), "status": "processed"}




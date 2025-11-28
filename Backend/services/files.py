import chromadb
from uuid import uuid4
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import FileModel
# --------------------------
# LAZY LOADING FACTORY PATTERNS
# --------------------------

def get_chroma_client():
    """Creates or returns an existing Chroma persistent client"""
    return chromadb.PersistentClient(path="chromadb_data")  # <- Persistent storage dir

def get_chroma_collection():
    client = get_chroma_client()
    return client.get_or_create_collection(name="file_chunks")  # returns same collection always


def get_embedding_model():
    """Loaded only when used, not at import time"""
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


# ----------------------------------------------------
# PROCESS FILE FUNCTION
# ----------------------------------------------------
from uuid import uuid4

async def process_file_upload(file, db):
     # Lazy-load everything inside the function
    embedding_model = get_embedding_model()
    collection = get_chroma_collection()
    # 1. Extract text
    content, file_type = extract_text(file)

    # 2. Chunk text
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(content)

    # 3. Generate a single file_id and chunk IDs
    file_id = str(uuid4())  # file-level ID, will match SQLite
    chunk_ids = [str(uuid4()) for _ in chunks]
    chunk_metadatas = [{"file_id": file_id} for _ in chunks]

    # 4. Generate embeddings
    chunk_embeddings = [embedding_model.embed_query(chunk) for chunk in chunks]

    # 5. Add to ChromaDB
    collection.add(
        documents=chunks,
        metadatas=chunk_metadatas,
        ids=chunk_ids,
        embeddings=chunk_embeddings
    )

    # 6. Save file-level metadata in SQLite
    file.file.seek(0)
    db_file = FileModel(
        id=file_id,  # same file_id as chunks
        filename=file.filename,
        filetype=file_type,
        size_bytes=len(file.file.read()),
        chunks_count=len(chunks),
        embeddings_count=len(chunks),
        status="embedded"
    )
    db.add(db_file)
    db.commit()

    return {"file_id": db_file.id, "chunks_count": len(chunks), "status": "processed"}

def extract_text(file) -> tuple[str, str]:
    filename = file.filename.lower()
    file_type = "txt"
    content = ""

    if filename.endswith(".txt"):
        content = file.file.read().decode("utf-8")
        file_type = "txt"
    elif filename.endswith(".pdf"):
        import fitz  # PyMuPDF
        doc = fitz.open(stream=file.file.read(), filetype="pdf")
        content = "\n".join([page.get_text() for page in doc])
        file_type = "pdf"
    elif filename.endswith(".docx"):
        import docx
        doc = docx.Document(file.file)
        content = "\n".join([p.text for p in doc.paragraphs])
        file_type = "docx"
    else:
        raise ValueError("Unsupported file type")

    return content, file_type


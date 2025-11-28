import chromadb
from uuid import uuid4
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

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
async def process_file_upload(file, db):
    # Lazy-load everything inside the function
    embedding_model = get_embedding_model()
    collection = get_chroma_collection()

    # 1) Extract text
    content, file_type = extract_text(file)

    # 2) Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(content)

    # 3) Embed text
    chunk_ids = [str(uuid4()) for _ in chunks]
    chunk_metadatas = [{"file_id": str(uuid4())} for _ in chunks]
    chunk_embeddings = [embedding_model.embed_query(c) for c in chunks]

    # 4) Store in ChromaDB
    collection.add(
        documents=chunks,
        metadatas=chunk_metadatas,
        ids=chunk_ids,
        embeddings=chunk_embeddings
    )

    # 5) Record in DB
    file.file.seek(0)  # reset pointer
    db_file = FileModel(
        id=chunk_metadatas[0]["file_id"],
        filename=file.filename,
        filetype=file_type,
        size_bytes=len(file.file.read()),
        chunks_count=len(chunks),
        embeddings_count=len(chunks),
        status="embedded"
    )
    db.add(db_file)
    db.commit()

    return {
        "file_id": db_file.id,
        "chunks_count": len(chunks),
        "status": "processed"
    }

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


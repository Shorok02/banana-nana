from uuid import uuid4
from models import FileModel
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import chromadb
import os
from langchain.embeddings import HuggingFaceEmbeddings


# Initialize ChromaDB client and collection
chroma_client = chromadb.Client(chromadb.config.Settings(
    persist_directory="./chromadb_data"
))

try:
    collection = chroma_client.get_collection("file_chunks")
except:
    collection = chroma_client.create_collection("file_chunks")



api_key = os.getenv("OPENAI_API_KEY")

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

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


async def process_file_upload(file, db):
    # 1. Extract text
    content, file_type = extract_text(file)

    # 2. Chunk text
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(content)

    # 3. Generate embeddings and IDs
    chunk_ids = [str(uuid4()) for _ in chunks]
    chunk_metadatas = [{"file_id": str(uuid4())} for _ in chunks]
    chunk_embeddings = [embedding_model.embed_query(chunk) for chunk in chunks]

    # 4. Add to ChromaDB
    collection.add(
        documents=chunks,
        metadatas=chunk_metadatas,
        ids=chunk_ids,
        embeddings=chunk_embeddings
    )

    # 5. Save metadata in SQLite
    file.file.seek(0)
    db_file = FileModel(
        id=chunk_metadatas[0]["file_id"],  # Use first chunk's file_id as file-level ID
        filename=file.filename,
        filetype=file_type,
        size_bytes=len(file.file.read()),
        chunks_count=len(chunks),
        embeddings_count=len(chunks),
        status="embedded"
    )
    db.add(db_file)
    db.commit()

    # Print chunks for verification
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}:\n{chunk}\n{'-'*50}")

    return {"file_id": db_file.id, "chunks": len(chunks)}

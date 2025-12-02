from langchain_community.vectorstores import Chroma
from clients.embedding_client import get_hf_embeddings

def get_client():
    import chromadb
    """Return a persistent Chroma client"""
    return chromadb.PersistentClient(path="chromadb_data")

def get_collection(name="file_chunks"):
    """Return (or create) a Chroma collection"""
    client = get_client()
    return client.get_or_create_collection(name=name)

def get_chroma_db():
    return Chroma(
        persist_directory="chromadb_data",
        collection_name="file_chunks",
        embedding_function=get_hf_embeddings()
    )

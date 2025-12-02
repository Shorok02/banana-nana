# services/embeddings.py
from typing import List
from clients.embedding_client import get_hf_embeddings

def embed_chunks(chunks: List[str]) -> List[List[float]]:
    """
    Return embeddings for a list of text chunks
    """
    model = get_hf_embeddings()
    try:
        return model.embed_documents(chunks)
    except AttributeError:
        # fallback if embed_documents not available
        return [model.embed_query(c) for c in chunks]

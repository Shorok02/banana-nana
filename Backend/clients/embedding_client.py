
def get_hf_embeddings(model_name="all-MiniLM-L6-v2"):
    """Return HuggingFace embedding model"""
    from langchain_community.embeddings import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(model_name=model_name)

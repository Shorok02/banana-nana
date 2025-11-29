# services/ask.py
from typing import List, Dict
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


# ------------------------------------------------
# 1) Reconnect to Chroma persistent store
# ------------------------------------------------
def get_chroma_db():
    return Chroma(
        persist_directory="chromadb_data",
        collection_name="file_chunks",
        embedding_function=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    )


# ------------------------------------------------
# 2) Retriever builder
# ------------------------------------------------
def get_retriever(k: int = 5):
    db = get_chroma_db()
    return db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )


# ------------------------------------------------
# 3) Retrieve relevant chunks
# ------------------------------------------------
def retrieve_chunks(query: str, k: int = 5) -> List[Dict]:
    retriever = get_retriever(k)

    # YOUR VERSION OF LANGCHAIN → MUST CALL PRIVATE METHOD
    docs = retriever._get_relevant_documents(query, run_manager=None)

    return [
        {
            "content": d.page_content,
            "metadata": d.metadata
        }
        for d in docs
    ]


# ------------------------------------------------
# 4) Ask Question (mocked answer)
# ------------------------------------------------
def ask_question(query: str, k: int = 5) -> Dict:
    chunks = retrieve_chunks(query, k)

    return {
        "query": query,
        "answer": f"Retrieved {len(chunks)} relevant chunks. (LLM placeholder)",
        "sources": chunks
    }

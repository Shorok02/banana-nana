from typing import Dict, List
import os
from dotenv import load_dotenv
from clients.llm_client import get_llm_chain
from clients.vectordb_client import get_chroma_db


load_dotenv()

# ------------------------------
# 1) Build retriever
# ------------------------------

def get_retriever(k: int = 5):
    db = get_chroma_db()
    return db.as_retriever(search_kwargs={"k": k})


# ------------------------------
# 2) Retrieve chunks
# ------------------------------

def retrieve_chunks(query: str, k: int = 5) -> List[Dict]:
    retriever = get_retriever(k)
    # MUST call private method due to current LangChain implementation
    docs = retriever._get_relevant_documents(query, run_manager=None)
    return [{"content": d.page_content, "metadata": d.metadata} for d in docs]


# ------------------------------
# 3) Generate answer
# ------------------------------
def generate_answer(query: str, context: str) -> str:
    chain = get_llm_chain()
    return chain.run(question=query, context=context)


# ------------------------------
# 4) Ask question (main entry)
# ------------------------------
def ask_question(query: str, k: int = 5) -> Dict:
    chunks = retrieve_chunks(query, k)
    context = "\n---\n".join([c["content"] for c in chunks])
    response_text = generate_answer(query, context)
    return {
        "query": query,
        "answer": response_text,
        "sources": chunks
    }

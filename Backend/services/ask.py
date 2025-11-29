# # services/ask.py
# from typing import List, Dict
# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings


# # ------------------------------------------------
# # 1) Reconnect to Chroma persistent store
# # ------------------------------------------------
# def get_chroma_db():
#     return Chroma(
#         persist_directory="chromadb_data",
#         collection_name="file_chunks",
#         embedding_function=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#     )


# # ------------------------------------------------
# # 2) Retriever builder
# # ------------------------------------------------
# def get_retriever(k: int = 5):
#     db = get_chroma_db()
#     return db.as_retriever(
#         search_type="similarity",
#         search_kwargs={"k": k}
#     )


# # ------------------------------------------------
# # 3) Retrieve relevant chunks
# # ------------------------------------------------
# def retrieve_chunks(query: str, k: int = 5) -> List[Dict]:
#     retriever = get_retriever(k)

#     # YOUR VERSION OF LANGCHAIN → MUST CALL PRIVATE METHOD
#     docs = retriever._get_relevant_documents(query, run_manager=None)

#     return [
#         {
#             "content": d.page_content,
#             "metadata": d.metadata
#         }
#         for d in docs
#     ]


# # ------------------------------------------------
# # 4) Ask Question (mocked answer)
# # ------------------------------------------------
# def ask_question(query: str, k: int = 5) -> Dict:
#     chunks = retrieve_chunks(query, k)

#     return {
#         "query": query,
#         "answer": f"Retrieved {len(chunks)} relevant chunks. (LLM placeholder)",
#         "sources": chunks
#     }


# services/ask.py
from typing import Dict, List
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains.llm import LLMChain
from langchain_groq import ChatGroq  # pip install langchain-groq
import os


# ------------------------------------------------
# 1) Connect to Chroma
# ------------------------------------------------
def get_chroma_db():
    return Chroma(
        persist_directory="chromadb_data",
        collection_name="file_chunks",
        embedding_function=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    )


def get_retriever(k: int = 5):
    return get_chroma_db().as_retriever(search_kwargs={"k": k})


# ------------------------------------------------
# 2) Retrieval function
# ------------------------------------------------
def retrieve_chunks(query: str, k: int = 5) -> List[Dict]:
    retriever = get_retriever(k)
    docs = retriever._get_relevant_documents(query, run_manager=None)

    return [{"content": d.page_content, "metadata": d.metadata} for d in docs]


# ------------------------------------------------
# 3) LLM Chain (RAG pipeline)
# ------------------------------------------------
def build_llm_chain():
    prompt = PromptTemplate.from_template("""
    You are a helpful AI assistant.
    Use ONLY the provided context to answer the question.

    Context:
    {context}

    Question: {question}

    If answer is not in the context, say: "I don't know."
    """)

    llm = ChatGroq(model="llama3-70b-8192", api_key=os.getenv("GROQ_API_KEY"))

    return LLMChain(llm=llm, prompt=prompt)


# ------------------------------------------------
# 4) Final ask function that now generate REAL answers
# ------------------------------------------------
def ask_question(query: str, k: int = 5) -> Dict:
    chunks = retrieve_chunks(query, k)
    context = "\n---\n".join([c["content"] for c in chunks])

    chain = build_llm_chain()
    response = chain.run(question=query, context=context)

    return {
        "query": query,
        "answer": response,
        "sources": chunks
    }


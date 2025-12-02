# services/chunkers.py
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text_chunks(content: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text into chunks using RecursiveCharacterTextSplitter
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.split_text(content)

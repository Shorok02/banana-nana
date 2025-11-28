from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from services.ask import ask_question_chain
from database import get_db  # make sure you have this dependency for getting a Session

router = APIRouter(prefix="/qa", tags=["qa"])


@router.get("/ask")
async def ask_question(
    question: str = Query(..., description="The question to ask"),
    top_k: int = Query(5, description="Number of chunks to retrieve"),
    db: Session = Depends(get_db)
):
    """
    Ask a question. Returns a mocked answer and sources retrieved from Chroma.
    """
    result = ask_question_chain(question=question, top_k=top_k, db=db)
    return result

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session


router = APIRouter(prefix="/qa", tags=["qa"])


from fastapi import APIRouter
from pydantic import BaseModel
from services.ask import ask_question   # << using your retrieval service



# ---- Request Body ----
class AskRequest(BaseModel):
    query: str
    k: int = 5  # optional top-k results


# ---- Endpoint ----
@router.post("/ask")
async def ask_endpoint(payload: AskRequest):
    response = ask_question(payload.query, payload.k)
    return response

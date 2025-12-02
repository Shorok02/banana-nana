# routers/api_router.py
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from services.background import background_process_file_upload
from services.ask import ask_question
from services.db import get_docs_by_user
from auth.dependencies import get_current_user

router = APIRouter(prefix="/api", tags=["API"])


@router.post("/upload")
async def upload_files(
    background_tasks: BackgroundTasks,
    user_id: str = Depends(get_current_user),
    files: List[UploadFile] = File(...),
):
    results = []

    for f in files:
        try:
            data = await f.read()

            if len(data) > 50 * 1024 * 1024:
                results.append({"filename": f.filename, "status": "skipped", "reason": "file too large"})
                continue

            # Queue background task
            background_tasks.add_task(background_process_file_upload, data, f.filename, user_id)

            results.append({"filename": f.filename, "status": "queued"})

        except Exception as e:
            # This is synchronous error (inside the router)
            raise HTTPException(status_code=500, detail=str(e))

    return {"files": results}


@router.get("/docs")
def list_docs(user_id: str = Depends(get_current_user)):
    try:
        files = get_docs_by_user(user_id)
        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


class AskRequest(BaseModel):
    question: str
    k: int = 5


@router.post("/ask")
async def ask_endpoint(payload: AskRequest, user_id: str = Depends(get_current_user)):
    try:
        response = ask_question(payload.question, user_id, payload.k)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
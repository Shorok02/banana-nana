# from fastapi import APIRouter, UploadFile, File, Depends, BackgroundTasks
# from sqlalchemy.orm import Session
# from database import get_db
# from services.files import process_file_upload_sync
# from models import FileModel
# from typing import List

# router = APIRouter(prefix="/files", tags=["File Upload"])



 
# @router.post("/upload")
# async def upload_file_api(
#     background_tasks: BackgroundTasks,
#     files: List[UploadFile] = File(...)
#     ):
#     """
#     Accept multiple files and process each in the background.
#     We read file bytes in the request handler and pass bytes to the BackgroundTasks
#     (so the UploadFile stream isn't used from a different thread).
#     """
#     results = []
#     for f in files:
#         try:
#             data = await f.read()  # read bytes in the request context


#             # TODO: simple validation move it to a service later with more conditions most probably
#             if len(data) > 50 * 1024 * 1024:  # 50 MB limit example
#                 results.append({"filename": f.filename, "status": "skipped", "reason": "file too large"})
#                 continue

#             # queue background processing; pass bytes and filename
#             background_tasks.add_task(process_file_upload_sync, data, f.filename)
#             results.append({"filename": f.filename, "status": "queued"})
#         except Exception as e:
#             results.append({"filename": f.filename, "status": "error", "reason": str(e)})

#     return {"files": results}


# @router.get("/list")
# def list_uploaded_files(db: Session = Depends(get_db)):
#     files = db.query(FileModel).all()
#     return [
#         {
#             "id": f.id,
#             "filename": f.filename,
#             "filetype": f.filetype,
#             "size_bytes": f.size_bytes,
#             "chunks_count": f.chunks_count,
#             "embeddings_count": f.embeddings_count,
#             "status": f.status,
#             "uploaded_at": f.uploaded_at
#         }
#         for f in files
#     ]




# from services.ask import ask_question   # << using your retrieval service
# from pydantic import BaseModel



# # ---- Request Body ----
# class AskRequest(BaseModel):
#     query: str
#     k: int = 5  # optional top-k results


# # ---- Endpoint ----
# @router.post("/ask")
# async def ask_endpoint(payload: AskRequest):
#     response = ask_question(payload.query, payload.k)
#     return response


# routers/api_router.py
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from services.files import process_file_upload_sync
from services.ask import ask_question
from database import get_db
from models import FileModel

router = APIRouter(prefix="/api", tags=["API"])


# ----- File Upload -----
@router.post("/upload")
async def upload_files(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
):
    """
    Upload multiple files and process them in the background.
    """
    results = []
    for f in files:
        try:
            data = await f.read()

            if len(data) > 50 * 1024 * 1024:  # 50 MB limit
                results.append({"filename": f.filename, "status": "skipped", "reason": "file too large"})
                continue

            background_tasks.add_task(process_file_upload_sync, data, f.filename)
            results.append({"filename": f.filename, "status": "queued"})
        except Exception as e:
            results.append({"filename": f.filename, "status": "error", "reason": str(e)})

    return {"files": results}


# ----- List uploaded docs metadata -----
@router.get("/docs")
def list_docs(db: Session = Depends(get_db)):
    files = db.query(FileModel).all()
    return [
        {
            "id": f.id,
            "filename": f.filename,
            "chunks_count": f.chunks_count,
            "embeddings_count": f.embeddings_count,
            "status": f.status,
            "uploaded_at": f.uploaded_at,
        }
        for f in files
    ]


# ----- Ask Question -----
class AskRequest(BaseModel):
    question: str
    k: int = 5


@router.post("/ask")
async def ask_endpoint(payload: AskRequest):
    """
    Ask a question based on uploaded files.
    """
    response = ask_question(payload.question, payload.k)
    return response

from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.files import process_file_upload, get_chroma_collection, get_embedding_model
from models import FileModel

router = APIRouter(prefix="/files", tags=["File Upload"])

@router.post("/upload")
async def upload_file_api(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    embedding_model = get_embedding_model()
    collection = get_chroma_collection()
    result = await process_file_upload(file, db, embedding_model=embedding_model, collection=collection)
    return {"status": "success", "chunks": result["chunks_count"]}



@router.get("/list")
def list_uploaded_files(db: Session = Depends(get_db)):
    files = db.query(FileModel).all()
    return [
        {
            "id": f.id,
            "filename": f.filename,
            "filetype": f.filetype,
            "size_bytes": f.size_bytes,
            "chunks_count": f.chunks_count,
            "embeddings_count": f.embeddings_count,
            "status": f.status,
            "uploaded_at": f.uploaded_at
        }
        for f in files
    ]
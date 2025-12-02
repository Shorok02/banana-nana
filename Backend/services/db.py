import uuid
from sqlalchemy.orm import Session
from models import FileModel
from database import SessionLocal

def save_file_metadata(file_id: str, user_id: str, filename: str, file_type: str, size: int, chunks_count: int) -> str:
    """
    Save file metadata to SQL DB
    """
    db: Session = SessionLocal()
    try:
        db_file = FileModel(
            id=file_id,
            user_id=user_id,
            filename=filename,
            filetype=file_type,
            size_bytes=size,
            chunks_count=chunks_count,
            embeddings_count=chunks_count,
            status="pending"
        )
        db.add(db_file)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
    return file_id
   
def update_file_status(file_id: str, status: str):
    """
    Update the status of a file in the SQL DB
    """
    db: Session = SessionLocal()
    try:
        db_file = db.query(FileModel).filter(FileModel.id == file_id).first()
        print(f"Updating status for file_id in update file method: {file_id} to {status}")
        if db_file:
            db_file.status = status
            print(f"Status updated to {status} for file_id: {file_id}")
            db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_docs_by_user(user_id: str) -> list:
    db: Session = SessionLocal()
    try:
        files = (
            db.query(FileModel)
              .filter(FileModel.user_id == user_id).all()
        )

        return [
            {
                "id": f.id,
                "filename": f.filename,
                "chunks_count": f.chunks_count,
                "embeddings_count": f.embeddings_count,
                "status": f.status,
            }
            for f in files
        ]

    except Exception as e:
        raise RuntimeError(f"Database error while fetching docs: {e}")

    finally:
        db.close()

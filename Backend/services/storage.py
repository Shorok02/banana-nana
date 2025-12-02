# services/storage.py
import uuid
from clients.vectordb_client import get_chroma_db

def create_chunk_metadatas(file_id: str, filename: str, chunks: list, user_id: str, file_type: str ) -> list:
    """
    Generate metadata per chunk for vector DB
    """
    try:
        return [{"file_id": file_id, 
                "filename": filename, 
                "chunk_index": idx, 
                "user_id": user_id,
                "file_type": file_type,
                } 
                for idx in range(len(chunks))]
    except Exception as e:
        raise e

def store_chunks_in_chroma(chunks: list, metadatas: list) -> list:
    """
    Store chunks, metadata, and embeddings in Chroma
    """
    try:
        db = get_chroma_db()
        ids = [str(uuid.uuid4()) for _ in chunks]
        db.add_texts(texts=chunks, metadatas=metadatas, ids=ids)
        return ids
    except Exception as e:
        raise e
    
# def save_file_metadata(user_id: str, filename: str, file_type: str, size: int, chunks_count: int) -> str:
#     """
#     Save file metadata to SQL DB
#     """
#     db: Session = SessionLocal()
#     try:
#         file_id = str(uuid.uuid4())
#         db_file = FileModel(
#             id=file_id,
#             user_id=user_id,
#             filename=filename,
#             filetype=file_type,
#             size_bytes=size,
#             chunks_count=chunks_count,
#             embeddings_count=chunks_count,
#             status="pending"
#         )
#         db.add(db_file)
#         db.commit()
#     except Exception as e:
#         db.rollback()
#         raise e
#     finally:
#         db.close()
#     return file_id
   
# def update_file_status(file_id: str, status: str):
#     """
#     Update the status of a file in the SQL DB
#     """
#     db: Session = SessionLocal()
#     try:
#         db_file = db.query(FileModel).filter(FileModel.id == file_id).first()
#         if db_file:
#             db_file.status = status
#             db.commit()
#     except Exception as e:
#         db.rollback()
#         raise e
#     finally:
#         db.close()

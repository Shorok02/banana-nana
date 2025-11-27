from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from database import Base

class FileModel(Base):
    __tablename__ = "files"

    id = Column(String, primary_key=True, index=True)   # UUID
    filename = Column(String, nullable=False)          # original filename
    filetype = Column(String, nullable=False)          # pdf, docx, txt
    size_bytes = Column(Integer, nullable=False)       # size in bytes
    chunks_count = Column(Integer, nullable=True)      # number of chunks
    embeddings_count = Column(Integer, nullable=True)  # number of embeddings saved
    status = Column(String, default="stored")          # stored / processed / embedded
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())


# services/files.py
import uuid
from typing import Dict
from services.extractors import extract_text_from_bytes
from services.chunkers import split_text_chunks
from services.storage import create_chunk_metadatas, store_chunks_in_chroma
from services.db import save_file_metadata, update_file_status

def process_file_upload_sync(file_bytes: bytes, filename: str, user_id: str) -> Dict:
    """
    Full processing pipeline:
    extract → split → embed → store → save metadata
    """
    try:
        #1: Extract text
        content, file_type = extract_text_from_bytes(file_bytes, filename)

        #2: Split into chunks
        chunks = split_text_chunks(content)

        #3: Generate metadata
        file_id = str(uuid.uuid4())
        print(f"Generated file_id: {file_id}")
        metadatas = create_chunk_metadatas(file_id, filename, chunks, user_id, file_type )

        #4: Save file metadata
        print(f"Saving file metadata for file_id: {file_id}")
        save_file_metadata(file_id, user_id, filename, file_type, len(file_bytes), len(chunks))
        
        #5: Store in Chroma
        print(f"Storing chunks in Chroma for file_id: {file_id}")
        store_chunks_in_chroma(chunks, metadatas)

        #6: Update status to 'processed' in DB
        print(f"Updating file status to 'processed' for file_id: {file_id}")
        update_file_status(file_id, "processed")



        return {"file_id": file_id, "chunks_count": len(chunks), "status": "processed"}
    
    except Exception as e:
        raise RuntimeError(f"Failed to process '{filename}': {e}") from e



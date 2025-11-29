from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.files import get_chroma_collection, get_embedding_model
from models import FileModel

router = APIRouter(prefix="/debug", tags=["Debug"])


@router.get("/files")
def debug_files(db: Session = Depends(get_db)):
    files = db.query(FileModel).all()
    return [
        {
            "id": f.id,
            "filename": f.filename,
            "filetype": f.filetype,
            "size_bytes": f.size_bytes,
            "chunks_count": f.chunks_count,
            "embeddings_count": f.embeddings_count,
            "status": f.status
        }
        for f in files
    ]

@router.get("/chroma")
async def debug_chroma():
    """
    Debug endpoint to inspect ChromaDB collection.
    Prints documents, embeddings, and metadata stored in the collection.
    """
    collection = get_chroma_collection()

    # Only include safe fields
    all_data = collection.get(include=["documents", "metadatas", "embeddings"])

    # Convert embeddings to lists (they might be numpy arrays)
    all_data["embeddings"] = [
        list(embed) if hasattr(embed, "__iter__") else embed
        for embed in all_data["embeddings"]
    ]

    return all_data


@router.get("/chroma/chunks/{file_id}")
async def debug_chroma(file_id: str = None):
    """
    Debug endpoint to inspect ChromaDB collection.
    If file_id is provided, shows only chunks for that file.
    """
    collection = get_chroma_collection()

    if file_id:
        # Query by file_id
        results = collection.get(
            where={"file_id": file_id},
            include=["documents", "metadatas"]  # exclude embeddings for safety
        )
        return results
    else:
        # Get everything (documents + metadatas only)
        all_data = collection.get(include=["documents", "metadatas"])
        return all_data


    """
    Debug endpoint to inspect ChromaDB collection.
    Prints whatever is stored in the collection.
    """
    collection = get_chroma_collection()

    # Allowed include items: "documents", "metadatas", "embeddings", "uris", "data"
    all_data = collection.get(include=["documents", "metadatas", "embeddings", "data"])

    # Return raw data
    return all_data
    """
    Debug endpoint to inspect ChromaDB collection.
    Prints everything in the collection without assumptions.
    """
    collection = get_chroma_collection()

    # Fetch all possible data from Chroma
    all_data = collection.get(include=["documents", "metadatas", "embeddings", "distances", "uris", "data"])

    # Just return whatever is there
    return all_data
    """
    Debug endpoint to inspect ChromaDB collection:
    - documents
    - embeddings
    - chunk IDs from metadata
    """
    collection = get_chroma_collection()

    # Fetch everything we can from the collection
    all_data = collection.get(include=["documents", "metadatas", "embeddings"])

    documents = all_data.get("documents", [])
    metadatas = all_data.get("metadatas", [])
    embeddings = all_data.get("embeddings", [])

    # Extract IDs from metadata
    chunk_ids = [meta.get("file_id") for meta_list in metadatas for meta in meta_list]

    return {
        "documents": documents,
        "chunk_ids": chunk_ids,
        "embeddings_shapes": [len(emb) for emb in embeddings]  # just length per chunk
    }



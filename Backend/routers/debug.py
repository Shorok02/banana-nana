from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.files import process_file_upload, get_chroma_collection, get_embedding_model
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



"becf43aa-7012-4829-9bd6-0e7307577158",
    "77751129-b31b-4a81-9703-9044833dbb85",
    "f41da606-31d5-4968-aa82-dfb3d5ba49b8",
    "79c93f5c-e347-4460-998c-40cc25d98f59",
    "825817b5-8b8b-4abf-9994-d17b049f0cf0",
    "df4d217e-b754-430c-92a7-006ea1ba0dcf",
    "d16aaefb-e349-43a9-95d3-7e71bac2eaa7",
    "b8e64061-16ae-424a-a9fd-fa912ed8b693",
    "a3acb4c3-f18b-402f-b807-45e511158c86",
    "50fe00ee-fb4c-411a-a9c4-c3a98938c9f4",
    "3fbb9e94-c153-47ed-bc83-79630e654539",
    "2b897331-f933-47c6-b530-10fb8a18fd68",
    "21d3d91f-eb68-4097-a63c-d2e44960dfbd",
    "fcdc6a89-a354-4a96-9e8a-cc51248cf751",
    "aaf1f323-bf14-4adf-b746-0dbd66ef050e",
    "bd3a84d6-ac2a-4236-bcf0-b1e382293546"

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



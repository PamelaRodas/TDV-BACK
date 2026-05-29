from fastapi import APIRouter, UploadFile, File, Request, HTTPException, status
from ..utils.serializers import serialize_doc
from bson import ObjectId

router = APIRouter()


@router.get("/")
async def get_photos(request: Request, limit: int = 100):
    db = request.app.state.db
    cursor = db.photos.find().sort("createdAt", -1).limit(limit)
    items = []
    async for doc in cursor:
        items.append(serialize_doc(doc))
    return items


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_photo(file: UploadFile = File(...), request: Request = None):
    db = request.app.state.db
    content = await file.read()
    # In this scaffold we store metadata only; actual file storage can be external
    doc = {"filename": file.filename, "content_type": file.content_type, "size": len(content)}
    from datetime import datetime
    doc["createdAt"] = datetime.utcnow().isoformat()
    res = await db.photos.insert_one(doc)
    created = await db.photos.find_one({"_id": res.inserted_id})
    return serialize_doc(created)


@router.get("/{id}")
async def get_photo(id: str, request: Request):
    db = request.app.state.db
    try:
        doc = await db.photos.find_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    if not doc:
        raise HTTPException(status_code=404, detail="Foto no encontrada")
    return serialize_doc(doc)


@router.put("/{id}")
async def update_photo(id: str, payload: dict, request: Request):
    db = request.app.state.db
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    await db.photos.update_one({"_id": oid}, {"$set": payload})
    updated = await db.photos.find_one({"_id": oid})
    return serialize_doc(updated)


@router.delete("/{id}")
async def delete_photo(id: str, request: Request):
    db = request.app.state.db
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    res = await db.photos.delete_one({"_id": oid})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Foto no encontrada")
    return {"deleted": True}

from fastapi import APIRouter, Request, HTTPException, status, Depends
from typing import List
from ..models.schemas import EntryCreate
from ..utils.serializers import serialize_doc
from bson import ObjectId

router = APIRouter()


@router.get("/stats")
async def get_diary_stats(request: Request):
    db = request.app.state.db
    total = await db.entries.count_documents({})
    return {"total_entries": total}


@router.get("/")
async def list_entries(request: Request, limit: int = 100):
    db = request.app.state.db
    cursor = db.entries.find().sort("createdAt", -1).limit(limit)
    items = []
    async for doc in cursor:
        items.append(serialize_doc(doc))
    return items


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_entry(entry: EntryCreate, request: Request):
    db = request.app.state.db
    doc = entry.dict()
    from datetime import datetime
    doc["createdAt"] = datetime.utcnow().isoformat()
    res = await db.entries.insert_one(doc)
    created = await db.entries.find_one({"_id": res.inserted_id})
    return serialize_doc(created)


@router.get("/{id}")
async def get_entry(id: str, request: Request):
    db = request.app.state.db
    try:
        doc = await db.entries.find_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    if not doc:
        raise HTTPException(status_code=404, detail="Entrada no encontrada")
    return serialize_doc(doc)


@router.put("/{id}")
async def update_entry(id: str, payload: dict, request: Request):
    db = request.app.state.db
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    await db.entries.update_one({"_id": oid}, {"$set": payload})
    updated = await db.entries.find_one({"_id": oid})
    return serialize_doc(updated)


@router.delete("/{id}")
async def delete_entry(id: str, request: Request):
    db = request.app.state.db
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    res = await db.entries.delete_one({"_id": oid})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Entrada no encontrada")
    return {"deleted": True}

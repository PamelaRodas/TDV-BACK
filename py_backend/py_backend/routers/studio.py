from fastapi import APIRouter, Request, HTTPException
from ..utils.serializers import serialize_doc
from bson import ObjectId

router = APIRouter()


@router.get("/entries")
async def studio_entries(request: Request, limit: int = 100):
    db = request.app.state.db
    cursor = db.entries.find().limit(limit)
    items = []
    async for doc in cursor:
        items.append(serialize_doc(doc))
    return items


@router.post("/entries")
async def studio_create_entry(payload: dict, request: Request):
    db = request.app.state.db
    from datetime import datetime
    doc = payload.copy()
    doc["createdAt"] = datetime.utcnow().isoformat()
    res = await db.entries.insert_one(doc)
    created = await db.entries.find_one({"_id": res.inserted_id})
    return serialize_doc(created)


@router.get("/entries/{id}")
async def studio_get_entry(id: str, request: Request):
    try:
        doc = await request.app.state.db.entries.find_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    if not doc:
        raise HTTPException(status_code=404, detail="Entrada no encontrada")
    return serialize_doc(doc)


@router.put("/entries/{id}")
async def studio_update_entry(id: str, payload: dict, request: Request):
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    await request.app.state.db.entries.update_one({"_id": oid}, {"$set": payload})
    updated = await request.app.state.db.entries.find_one({"_id": oid})
    return serialize_doc(updated)


@router.delete("/entries/{id}")
async def studio_delete_entry(id: str, request: Request):
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    res = await request.app.state.db.entries.delete_one({"_id": oid})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Entrada no encontrada")
    return {"deleted": True}

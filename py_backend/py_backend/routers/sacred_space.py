from fastapi import APIRouter, Request, HTTPException
from ..utils.serializers import serialize_doc
from bson import ObjectId

router = APIRouter()


@router.get("/")
async def list_spaces(request: Request, limit: int = 100):
    db = request.app.state.db
    cursor = db.sacred_spaces.find().limit(limit)
    items = []
    async for doc in cursor:
        items.append(serialize_doc(doc))
    return items


@router.post("/")
async def create_space(payload: dict, request: Request):
    db = request.app.state.db
    from datetime import datetime
    doc = payload.copy()
    doc["createdAt"] = datetime.utcnow().isoformat()
    res = await db.sacred_spaces.insert_one(doc)
    created = await db.sacred_spaces.find_one({"_id": res.inserted_id})
    return serialize_doc(created)


@router.get("/{id}")
async def get_space(id: str, request: Request):
    try:
        doc = await request.app.state.db.sacred_spaces.find_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    if not doc:
        raise HTTPException(status_code=404, detail="No encontrado")
    return serialize_doc(doc)


@router.put("/{id}")
async def update_space(id: str, payload: dict, request: Request):
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    await request.app.state.db.sacred_spaces.update_one({"_id": oid}, {"$set": payload})
    updated = await request.app.state.db.sacred_spaces.find_one({"_id": oid})
    return serialize_doc(updated)


@router.delete("/{id}")
async def delete_space(id: str, request: Request):
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    res = await request.app.state.db.sacred_spaces.delete_one({"_id": oid})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="No encontrado")
    return {"deleted": True}

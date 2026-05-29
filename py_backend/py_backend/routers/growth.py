from fastapi import APIRouter, Request, HTTPException, status
from ..utils.serializers import serialize_doc
from bson import ObjectId

router = APIRouter()


@router.get("/")
async def get_growth():
    return []


@router.post("/")
async def create_growth(payload: dict, request: Request):
    db = request.app.state.db
    from datetime import datetime
    doc = payload.copy()
    doc["createdAt"] = datetime.utcnow().isoformat()
    res = await db.growth.insert_one(doc)
    created = await db.growth.find_one({"_id": res.inserted_id})
    return serialize_doc(created)


@router.get("/{id}")
async def get_growth_item(id: str, request: Request):
    try:
        doc = await request.app.state.db.growth.find_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    if not doc:
        raise HTTPException(status_code=404, detail="No encontrado")
    return serialize_doc(doc)


@router.put("/{id}")
async def update_growth(id: str, payload: dict, request: Request):
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    await request.app.state.db.growth.update_one({"_id": oid}, {"$set": payload})
    updated = await request.app.state.db.growth.find_one({"_id": oid})
    return serialize_doc(updated)


@router.delete("/{id}")
async def delete_growth(id: str, request: Request):
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    res = await request.app.state.db.growth.delete_one({"_id": oid})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="No encontrado")
    return {"deleted": True}

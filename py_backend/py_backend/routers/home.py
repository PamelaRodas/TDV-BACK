from fastapi import APIRouter, Request, HTTPException
from ..utils.serializers import serialize_doc
from bson import ObjectId

router = APIRouter()


@router.get("/")
async def get_home(request: Request):
    db = request.app.state.db
    doc = await db.home.find_one({})
    if not doc:
        return {}
    return serialize_doc(doc)


@router.put("/")
async def update_home(payload: dict, request: Request):
    db = request.app.state.db
    await db.home.update_one({}, {"$set": payload}, upsert=True)
    doc = await db.home.find_one({})
    return serialize_doc(doc)

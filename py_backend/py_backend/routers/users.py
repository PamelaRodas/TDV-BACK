from fastapi import APIRouter, Request, HTTPException
from ..utils.serializers import serialize_doc
from bson import ObjectId
from ..utils.auth import get_password_hash, verify_password

router = APIRouter()


@router.get("/profile")
async def get_user_profile(request: Request):
    # In a full app you'd use auth; here we return a placeholder for the first user
    db = request.app.state.db
    user = await db.users.find_one({})
    if not user:
        return {}
    user.pop("password", None)
    return serialize_doc(user)


@router.put("/profile")
async def update_user_profile(payload: dict, request: Request):
    db = request.app.state.db
    # This simplistic update updates the first user found
    res = await db.users.update_one({}, {"$set": payload})
    user = await db.users.find_one({})
    if user:
        user.pop("password", None)
    return serialize_doc(user)


@router.post("/change-password")
async def change_password(payload: dict, request: Request):
    email = payload.get("email")
    old = payload.get("old_password")
    new = payload.get("new_password")
    if not email or not old or not new:
        raise HTTPException(status_code=400, detail="Se requieren email, old_password y new_password")
    db = request.app.state.db
    user = await db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not verify_password(old, user.get("password", "")):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    hashed = get_password_hash(new)
    await db.users.update_one({"email": email}, {"$set": {"password": hashed}})
    return {"changed": True}


@router.delete("/account")
async def delete_account(payload: dict, request: Request):
    email = payload.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Se requiere email")
    db = request.app.state.db
    res = await db.users.delete_one({"email": email})
    return {"deleted": res.deleted_count > 0}


@router.get("/public/{id}")
async def get_public_profile(id: str, request: Request):
    try:
        doc = await request.app.state.db.users.find_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    if not doc:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Remove sensitive fields
    doc.pop("password", None)
    return serialize_doc(doc)

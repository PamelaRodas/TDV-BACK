import os
from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta

from ..models.schemas import UserCreate
from ..utils.auth import get_password_hash, verify_password, create_access_token, decode_access_token
from ..config import settings

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.post("/register")
async def register(user: UserCreate, request: Request):
    db = request.app.state.db
    # Demo mode shortcut
    if os.getenv("DEMO_MODE") == "true":
        demo_id = f"demo-user-{int(__import__('time').time()*1000)}"
        token = create_access_token({"userId": demo_id})
        return {
            "message": "User registered successfully (DEMO MODE)",
            "token": token,
            "user": {"id": demo_id, "name": user.name or "Demo User", "email": user.email or "demo@example.com"},
            "demo": True,
        }

    existing = await db.users.find_one({"email": user.email.lower()})
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed = get_password_hash(user.password)
    doc = {
        "name": user.name,
        "email": user.email.lower(),
        "password": hashed,
        "bio": "",
        "profileImage": None,
        "preferences": {"language": "es", "theme": "light"},
    }
    res = await db.users.insert_one(doc)
    user_id = str(res.inserted_id)
    token = create_access_token({"userId": user_id})
    return {
        "message": "User registered successfully",
        "token": token,
        "user": {"id": user_id, "name": doc["name"], "email": doc["email"]},
    }


@router.post("/login")
async def login(form_data: dict, request: Request):
    db = request.app.state.db
    email = form_data.get("email")
    password = form_data.get("password")

    if os.getenv("DEMO_MODE") == "true":
        demo_id = f"demo-user-{int(__import__('time').time()*1000)}"
        token = create_access_token({"userId": demo_id})
        return {
            "message": "Login successful (DEMO MODE)",
            "token": token,
            "user": {"id": demo_id, "name": email.split("@")[0] if email else "Demo User", "email": email or "demo@example.com"},
            "demo": True,
        }

    user = await db.users.find_one({"email": email.lower()})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not verify_password(password, user.get("password", "")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"userId": str(user.get("_id"))})
    return {
        "message": "Login successful",
        "token": token,
        "user": {"id": str(user.get("_id")), "name": user.get("name"), "email": user.get("email")},
    }


async def get_current_user(token: str = Depends(oauth2_scheme), request: Request = None):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token required")
    try:
        payload = decode_access_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token")
    return payload


@router.get("/validate")
async def validate_token(current_user: dict = Depends(get_current_user)):
    return {"valid": True, "user": current_user}

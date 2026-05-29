from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import connect_to_mongo, close_mongo_connection
from .routers import auth, diary, photos, growth, home, sacred_space, users, analytics, studio

app = FastAPI(title="TDV-BACK (Python)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth")
app.include_router(diary.router, prefix="/api/diary")
app.include_router(photos.router, prefix="/api/photos")
app.include_router(growth.router, prefix="/api/growth")
app.include_router(home.router, prefix="/api/home")
app.include_router(sacred_space.router, prefix="/api/sacred-space")
app.include_router(users.router, prefix="/api/users")
app.include_router(analytics.router, prefix="/api/analytics")
app.include_router(studio.router, prefix="/api/studio")


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.on_event("startup")
async def startup_event():
    await connect_to_mongo(app)


@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection(app)

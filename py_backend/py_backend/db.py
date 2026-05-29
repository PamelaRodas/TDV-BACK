from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

client: AsyncIOMotorClient | None = None


async def connect_to_mongo(app):
    global client
    client = AsyncIOMotorClient(settings.MONGO_URI)
    app.state.db = client[settings.MONGO_DB]


async def close_mongo_connection(app):
    if client:
        client.close()

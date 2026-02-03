from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.MONGO_URL)
db = client.os_system_database

def get_collection(name: str):
    return db[name]
from motor.motor_asyncio import AsyncIOMotorCollection
from typing import Optional, Dict, Any
from bson import ObjectId

class UserRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        user = await self.collection.find_one({"email": email})
        return user

    async def create(self, user_dict: Dict[str, Any]) -> str:
        result = await self.collection.insert_one(user_dict)
        return str(result.inserted_id)

    async def get_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        return user
from bson import ObjectId

class OSRepository:
    def __init__(self, collection):
        self.collection = collection

    async def create(self, os_dict: dict) -> str:
        result = await self.collection.insert_one(os_dict)
        return str(result.inserted_id)

    async def list_by_user(self, email: str):
        cursor = self.collection.find({"usuario_email": email})
        return await cursor.to_list(length=100)

    async def get_by_id(self, os_id: str):
        return await self.collection.find_one({"_id": ObjectId(os_id)})

    async def update(self, os_id: str, data: dict):
        await self.collection.update_one(
            {"_id": ObjectId(os_id)},
            {"$set": data}
        )

    async def delete(self, os_id: str):
        await self.collection.delete_one({"_id": ObjectId(os_id)})
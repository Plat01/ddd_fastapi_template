from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.config import get_settings
from src.infrastructure.repositories import UserDocument

async def init_db():
    client: AsyncIOMotorClient = AsyncIOMotorClient(get_settings().MONGO_URI)
    try:
        # await init_beanie(database=client[get_settings().MONGO_DB_NAME], document_models=[UserDocument])  # TODO: add all models 
        await init_beanie(database=client.users, document_models=[UserDocument])  # TODO: add all models 
        print(client.users)
    except Exception as e:
        print(e)
        print("Failed to connect to MongoDB")
        await init_beanie(database=client.db_name, document_models=[UserDocument])  # TODO: add all models 



if __name__ == "__main__":
    import asyncio
    asyncio.run(init_db())
    
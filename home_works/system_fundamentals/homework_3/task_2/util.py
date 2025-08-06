from pymongo import AsyncMongoClient

DATABASE_NAME = "pet_database"
DOCUMENT_NAME = "pets"

def get_mongo_data():
    host = input("MongoDB host (enter to localhost): ")
    hibit = host if host else "localhost"
    port = input("MongoDB port (enter to 27017): ")
    port = int(port) if port else 27017

    return hibit, port

async def get_mongo_client(host: str, port: int):
    return AsyncMongoClient(host, port)
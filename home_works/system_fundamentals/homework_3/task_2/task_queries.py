import asyncio

from pymongo import AsyncMongoClient

from home_works.system_fundamentals.homework_3.task_2.seed import seed_documents
from home_works.system_fundamentals.homework_3.task_2.util import get_mongo_client, get_mongo_data, DATABASE_NAME, \
    DOCUMENT_NAME


async def get_mongo_task_client():
    return await get_mongo_client(*get_mongo_data())

async def get_all_documents(client: AsyncMongoClient):
    return await client[DATABASE_NAME][DOCUMENT_NAME].find().to_list(length=None)

async def add_new_feature(client: AsyncMongoClient, name: str, feature: str):
    await client[DATABASE_NAME][DOCUMENT_NAME].update_many({"name": name}, {"$push": {"features": feature}})
    return await client[DATABASE_NAME][DOCUMENT_NAME].find({"name": name}).to_list(length=None)

async def update_age_by_name(client: AsyncMongoClient, name: str, age: int):
    await client[DATABASE_NAME][DOCUMENT_NAME].update_many({"name": name}, {"$set": {"age": age}})
    return await client[DATABASE_NAME][DOCUMENT_NAME].find({"name": name}).to_list(length=None)

async def get_by_name(client: AsyncMongoClient, name: str):
    return await client[DATABASE_NAME][DOCUMENT_NAME].find({"name": name}).to_list(length=None)

async def delete_by_name(client: AsyncMongoClient, name: str):
    await client[DATABASE_NAME][DOCUMENT_NAME].delete_many({"name": name})
    return await client[DATABASE_NAME][DOCUMENT_NAME].find({"name": name}).to_list(length=None)

async def delete_all(client: AsyncMongoClient):
    await client[DATABASE_NAME][DOCUMENT_NAME].delete_many({})
    return await client[DATABASE_NAME][DOCUMENT_NAME].find().to_list(length=None)

async def queries(client: AsyncMongoClient):
    doc_amount = int(input("How many cats to insert? "))
    await seed_documents(client, doc_amount)
    all_documents = await get_all_documents(client)
    print(all_documents)
    print(100*"=")
    cat_name = input("Cat name to update? ")
    updated_cat = await update_age_by_name(client, cat_name, 25)
    print(updated_cat)
    updated_cat = await add_new_feature(client, cat_name, input("Feature to add? "))
    print("With a new feature\n", updated_cat)
    cat_name = input("Cat name to delete? ")
    print("Before deletion\n", await get_by_name(client, cat_name))
    deleted_cat = await delete_by_name(client, cat_name)
    print("After deletion\n", deleted_cat)
    print("Now deleting everything")
    await delete_all(client)
    print("All deleted")
    print(await get_all_documents(client))


def main():
    client = asyncio.run(get_mongo_task_client())
    asyncio.run(queries(client))

if __name__ == "__main__":
    main()
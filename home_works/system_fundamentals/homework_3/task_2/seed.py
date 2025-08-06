import asyncio
from faker import Faker
from pymongo import AsyncMongoClient

from home_works.system_fundamentals.homework_3.task_2.util import get_mongo_client, get_mongo_data, DATABASE_NAME, \
    DOCUMENT_NAME


def fake_document():
    faker = Faker(ocale='uk_UA')
    return {
        "name": faker.first_name(),
        "age": faker.random_int(min=0, max=18),
        "features": faker.words(nb=3)
    }

async def seed_documents(mongo_client: AsyncMongoClient, documents_amount: int):
    collection = mongo_client[DATABASE_NAME][DOCUMENT_NAME]
    for _ in range(documents_amount):
        await collection.insert_one(fake_document())
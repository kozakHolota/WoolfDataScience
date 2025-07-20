import time
import psycopg2
from db import engine, Base

print("Waiting for database...")
time.sleep(5)

print("Running migrations...")
Base.metadata.create_all(bind=engine)
print('Migration completed')
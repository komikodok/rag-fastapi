import firebase_admin
from firebase_admin import firestore, credentials
import os
from dotenv import load_dotenv, find_dotenv
import json

load_dotenv(find_dotenv())

service_key = json.loads(os.getenv("FIRESTORE_SERVICE_KEY"))
cred = credentials.Certificate(service_key)
firebase_admin.initialize_app(cred)

db = firestore.client()

def get_db():
    return db



# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import os
# from dotenv import find_dotenv, load_dotenv

# load_dotenv(find_dotenv())

# DATABASE_URL = os.getenv("DATABASE_URL")

# engine = create_engine(DATABASE_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

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

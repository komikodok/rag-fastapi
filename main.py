from fastapi import FastAPI
from router.document_router import document_router


app = FastAPI()

app.include_router(document_router)
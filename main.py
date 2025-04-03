from fastapi import FastAPI
from router.document_router import document_router
from router.chat_router import chat_router


app = FastAPI()

app.include_router(document_router)
app.include_router(chat_router)
from langchain_core.pydantic_v1 import Field, BaseModel
from langchain_groq.chat_models import ChatGroq
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.documents import Document

from dotenv import load_dotenv, find_dotenv
import os

from .state import State
from client.db_client import DATABASE_URL

load_dotenv(find_dotenv())

groq_api_key = os.getenv("GROQ_API_KEY")
model_name = os.getenv("MODEL_NAME")
llm = ChatGroq(model=model_name, api_key=groq_api_key)
embeddings = FastEmbedEmbeddings()

vectorstore = PGVector(
    connection_string=DATABASE_URL,
    embedding_function=embeddings,
    collection_name="document_embeddings"
)
retriever = vectorstore.as_retriever()

def retrieve(state: State):
    question = state.get("question", "")

    docs = retriever.invoke(question)
    docs_string = "\n\n".join(doc.page_content for doc in docs)

    return {"document": docs}
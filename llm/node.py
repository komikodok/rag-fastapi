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
    
def retrieve_node(state: State):
    question = state.get("question")

    docs = retriever.invoke(question)
    docs_string = "\n\n".join(doc.page_content for doc in docs)

    return {"document": docs_string}

def generation_node(state: State):
    question = state.get("question")
    document = state.get("document")
    message_history = state.get("message_history", [])

    if not isinstance(message_history, list):
        raise ValueError("Message history must be list object.")

    template = """
                Anda adalah asisten AI dengan wawasan yang sangat luas dan bertugas untuk membantu user.
                Respon berdasarkan pengetahuan yang anda miliki, gunakan konteks dari retriever sebagai informasi tambahan.
                Jika anda tidak mengikuti instruksi di atas anda akan HILANG DARI ALAM SEMESTA INI!!!
    """
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", template),
            (MessagesPlaceholder("message_history")),
            ("human", "User: {question}, Konteks: {context}")
        ]
    )
    parser = StrOutputParser()

    chain = (
        prompt_template
        | llm
        | parser
    )

    generation = chain.invoke({"question": question, "context": document, "message_history": message_history})
    return {"generation": generation}
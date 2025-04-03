from fastapi import UploadFile, HTTPException
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, UnstructuredURLLoader
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_postgres.vectorstores import PGVector
from langchain_community.embeddings import FastEmbedEmbeddings

import shutil
from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "documents"

DATABASE_URL = os.getenv("DATABASE_URL")

if not UPLOAD_DIR.exists():
    os.makedirs(UPLOAD_DIR)

class ServiceDocument:

    def __init__(self):
        self.__documents = None

    def save_file(self, upload_file: UploadFile) -> None:
        file_path = UPLOAD_DIR / upload_file.filename

        with open(file_path, "wb") as f:
            shutil.copyfileobj(upload_file.file, f)
        
    def delete_file(self, filename: str) -> None:
        file_path = UPLOAD_DIR / filename
        if file_path.exists():
            file_path.unlink()
        else:
            raise FileNotFoundError(f"File {file_path} is not found in {UPLOAD_DIR}")

    def load_knowledge_from_file(self) -> "ServiceDocument":
        loader = DirectoryLoader(
            UPLOAD_DIR, 
            glob="*.pdf",
            recursive=True,
            loader_cls=PyPDFLoader
        )
        self.__documents = loader.load()
        return self

    def load_knowledge_from_url(self, *url_args: str) -> "ServiceDocument":
        try:
            loader = UnstructuredURLLoader(
                url_args,
                mode="single",
                strategy="fast"
            )
            self.__documents = loader.load()
        except Exception as e:
            raise e
        return self
    
    def store_documents(self):
        if not self.__documents:
            raise TypeError("Document must be List[Document]")
        
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n"],
            chunk_size=500,
            chunk_overlap=100
        )
        chunk = text_splitter.split_documents(documents=self.__documents)
        embeddings = FastEmbedEmbeddings()
        try:
            PGVector.from_documents(
                chunk,
                embedding=embeddings,
                collection_name="document_embeddings",
                connection=DATABASE_URL
            )
            return None
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to store documents: {str(e)}"
            )
    

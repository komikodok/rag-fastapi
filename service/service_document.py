from fastapi import UploadFile, HTTPException
from langchain_community.document_loaders import DirectoryLoader, UnstructuredFileLoader, UnstructuredURLLoader
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_google_firestore.vectorstores import FirestoreVectorStore
from langchain_community.embeddings import FastEmbedEmbeddings

import shutil
from pathlib import Path
import os
from datetime import timedelta


BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "documents"

if not UPLOAD_DIR.exists():
    os.makedirs(UPLOAD_DIR)

class ServiceDocument:

    def __init__(self):
        self.__documents = None

    def save_file(self, upload_file: UploadFile) -> None:
        file_path = UPLOAD_DIR / upload_file.filename

        with open(file_path, "wb") as f:
            shutil.copyfileobj(upload_file.file, f)
        
    async def delete_file(self, filename: str) -> None:
        file_path = UPLOAD_DIR / filename
        if file_path.exists():
            await file_path.unlink()
        else:
            raise FileNotFoundError(f"File {file_path} is not found in {UPLOAD_DIR}")

    def load_knowledge_from_file(self) -> "ServiceDocument":
        loader = DirectoryLoader(
            UPLOAD_DIR, 
            glob=["*.pdf", "*.txt", "*.docx", "*.md"],
            recursive=True,
            loader_cls=UnstructuredFileLoader
        )
        self.__documents = loader.load()
        print(f"Document: {self.__documents}")
        return self
    
    def load_knowledge_from_url(self, *url_args: str) -> "ServiceDocument":
        loader = UnstructuredURLLoader(
            url_args,
            mode="single",
            strategy="fast"
        )
        self.__documents = loader.load()
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
            vector_store = FirestoreVectorStore.from_documents(
                chunk, 
                embedding=embeddings,
                collection="document_embeddings",
                request_timeout=timedelta(minutes=1)
            )
            return vector_store
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to store documents: {str(e)}"
            )
    

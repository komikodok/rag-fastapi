from fastapi import Depends, UploadFile
from langchain_community.document_loaders import DirectoryLoader, UnstructuredFileLoader, UnstructuredURLLoader
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_google_firestore.vectorstores import FirestoreVectorStore
from langchain_community.embeddings import FastEmbedEmbeddings

from typing import List
import os
import shutil
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = "/documents"

class ServiceDocument:

    def __init__(self):
        self.__documents = None

    def save_file(self, upload_file: List[UploadFile]) -> None:
        for file in upload_file:
            file_path = os.path.join(BASE_DIR / UPLOAD_DIR, file.filename)

            with open(file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)

    def delete_file(self):
        pass

    def load_knowledge_from_file(self, path: str = "../documents/") -> "ServiceDocument":
        loader = DirectoryLoader(
            path, 
            glob="*.{pdf, txt, doc, md}",
            recursive=True,
            loader_cls=UnstructuredFileLoader
        )
        self.__documents = loader.load()
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
            chunk_size=1000,
            chunk_overlap=100
        )
        chunk = text_splitter.split_documents(documents=self.__documents)
        embeddings = FastEmbedEmbeddings()
        return FirestoreVectorStore.from_documents(
            chunk, 
            embedding=embeddings,
            collection="document_embeddings"
        )
    

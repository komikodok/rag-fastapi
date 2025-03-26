from fastapi import APIRouter, Depends, File, UploadFile

from typing import List
import os
import shutil
from pathlib import Path
from service.service_document import ServiceDocument


document_router = APIRouter(prefix="/api")

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = "/documents"

@document_router.post("/store-file", summary="Store your document file")
def store_file(
    files: List[UploadFile] = File(),
    service_document: ServiceDocument = Depends()
):
    file_path = lambda file: os.path.join(BASE_DIR / UPLOAD_DIR, file.filename)
    pass
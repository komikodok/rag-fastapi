from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from fastapi.responses import Response

from typing import List
from service.service_document import ServiceDocument


document_router = APIRouter(prefix="/api")

@document_router.post("/store-file", summary="Store your document file")
def store_file(
    files: List[UploadFile] = File(max_size=10_000_000),
    service_document: ServiceDocument = Depends()
):
    try:
        for file in files:
            service_document.save_file(file)

        document = service_document.load_knowledge_from_file()
        document.store_documents()

        for file in files:
            service_document.delete_file(file.filename)
    except Exception as e:
        return HTTPException(
            status_code=status.ht,
            detail="Failed to store document"
        )

    return Response(
        "Store document to database successfully",
        status_code=status.HTTP_201_CREATED
    )
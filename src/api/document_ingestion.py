from fastapi import APIRouter, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from src.services.document_service import DocumentService
from src.database import get_db

router = APIRouter()

@router.post("/ingest")
async def ingest_document(file: UploadFile, db: Session = Depends(get_db)):
    if not (file.filename.endswith('.pdf') or file.filename.endswith('.txt')):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported.")
    
    document_service = DocumentService(db)
    document = await document_service.ingest_document(file)
    return {"document_id": document.id, "filename": document.name}

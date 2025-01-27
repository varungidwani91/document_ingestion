from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.utils.auth_utils import verify_token
from src.services.document_service import DocumentService

router = APIRouter()

@router.post("/select-documents")
def select_documents(document_names: list[str], token: str = Depends(verify_token), db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    # Store document names in user session or a temporary storage
    user_id = token.get("sub")
    document_service = DocumentService(db)
    document_service.store_selected_documents(user_id, document_names)
    
    return {"selected_documents": document_names}

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.utils.auth_utils import verify_token
from src.services.qa_service import QAService

router = APIRouter()

@router.post("/qa")
def qa(question: str, token: str = Depends(verify_token), db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    user_id = token.get("sub")
    qa_service = QAService(db)
    answer = qa_service.answer_question(user_id, question)
    
    return {"answer": answer}

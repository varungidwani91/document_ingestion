from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from src.database import get_db
from src.services.user_service import UserService
from src.utils.auth_utils import create_access_token

router = APIRouter()

@router.post("/register")
def register_user(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.create_user(username, password)
    return {"username": user.username}

@router.post("/login")
def login_user(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

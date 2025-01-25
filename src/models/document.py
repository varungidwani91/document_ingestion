from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.orm import relationship
from src.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    embedding = Column(LargeBinary)

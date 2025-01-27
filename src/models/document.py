from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base

class Document(Base):
    __tablename__ = "documents"

    document_id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, index=True)
    upload_time = Column(TIMESTAMP, server_default=func.now())
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    embeddings = relationship("Embedding", back_populates="document")

class Embedding(Base):
    __tablename__ = "embeddings"

    embedding_id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey('documents.document_id'))
    embedding = Column(LargeBinary)
    text_chunk = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    document = relationship("Document", back_populates="embeddings")

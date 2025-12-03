from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)

    # Renamed 'password' to 'password_hash' for clarity, as it stores the hashed value
    password = Column(String(256), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Add the missing relationship to documents
    documents = relationship("Documents", back_populates="owner")


class Documents(Base):  # Fixed typo: was "Documnets"
    __tablename__ = "documents"
    document_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    s3_link = Column(Text, nullable=False)
    qr_code_link = Column(Text, nullable=True)  # Add this field
    owner_id = Column(Integer, ForeignKey("users.user_id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="documents")

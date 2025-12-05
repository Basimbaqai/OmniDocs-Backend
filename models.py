from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, func
from database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(256), nullable=False) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Add cascade="all, delete-orphan" here
    documents = relationship("Documents", back_populates="owner", cascade="all, delete-orphan")


class Documents(Base):
    __tablename__ = 'documents'
    document_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    s3_link = Column(Text, nullable=False)
    qr_code_link = Column(Text, nullable=True)
    
    # Add ondelete="CASCADE" to the ForeignKey
    owner_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="documents")
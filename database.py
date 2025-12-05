from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Your Neon connection string
DATABASE_URL = 'postgresql://neondb_owner:npg_rbXTJ1KLq5dF@ep-weathered-bread-a4ubxg1p-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
# Or use environment variable (recommended for security)
# DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
from database import engine
from models import Base

def clear_database():
    try:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        print("✅ Database cleared successfully!")
    except Exception as e:
        print(f"❌ Error clearing database: {e}")

if __name__ == "__main__":
    clear_database()
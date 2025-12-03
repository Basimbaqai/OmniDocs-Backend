from database import engine
from models import Base
import os


def recreate_database():
    try:
        # Delete the existing database file
        if os.path.exists("omni.db"):
            os.remove("omni.db")
            print("✅ Old database file deleted")

        # Create all tables with the new schema
        Base.metadata.create_all(bind=engine)
        print("✅ Database recreated with updated schema!")
        print("Tables created:")
        print("  - users (with first_name, last_name, email, password, user_id)")
        print(
            "  - documents (with document_id, title, s3_link, qr_code_link, owner_id, created_at)"
        )

    except Exception as e:
        print(f"❌ Error recreating database: {e}")


if __name__ == "__main__":
    recreate_database()

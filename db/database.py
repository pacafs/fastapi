from db.config import pg_url
from typing import Annotated
from fastapi import Depends
from sqlmodel import Field, Session, SQLModel, create_engine

engine = create_engine(str(pg_url))

def create_tables():
    print("Creating tables...")
    SQLModel.metadata.create_all(engine)
    print("Tables created successfully")

def start_session():
    with Session(engine) as session:
        yield session

        

pgSession = Annotated[Session, Depends(start_session)]




# Test the database connection
def test_database_connection():
    try:
        with Session(engine) as session:
            print("Database connection successful")
            #print(session)
    except Exception as e:
        print(f"Database connection failed: {e}")

# Remove duplicate if block and ensure create_tables is called
if __name__ == "__main__":
    create_tables()
    test_database_connection()

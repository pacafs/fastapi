from config import pg_url
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

# Add table=True to make this a database table
class Task(SQLModel, table=True): # type: ignore
    __tablename__ = "tasks"
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str = Field(index=True)
    completed: bool = Field(default=False)

engine = create_engine(pg_url)

def create_tables():
    print("Creating tables...")
    SQLModel.metadata.create_all(engine)
    print("Tables created successfully")

def get_session():
    with Session(engine) as session:
        yield session

SessionLocal = Annotated[Session, Depends(get_session)]

# Test the database connection
def test_database_connection():
    try:
        with Session(engine) as session:
            print("Database connection successful")
    except Exception as e:
        print(f"Database connection failed: {e}")

# Remove duplicate if block and ensure create_tables is called
if __name__ == "__main__":
    create_tables()
    test_database_connection()


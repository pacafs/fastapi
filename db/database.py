from db.config import pg_url
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
import logging


# Import your models here
# These imports ensure SQLModel knows about all your tables
from app.models.task import Task  # Import Task model 
from app.models.user import User  # Import User model

# Set up logging
logger = logging.getLogger("uvicorn")

# Start the engine/connection to the database
engine = create_engine(str(pg_url))

# Create the tables if not already created
def create_tables():
    logger.info("Setting up tables...")
    SQLModel.metadata.create_all(engine)
    logger.info("Tables setup successfully")

# Create a session
def start_session():
    with Session(engine) as session:
        yield session

# Create a dependency for the session
pgSession = Annotated[Session, Depends(start_session)]

# Test the database connection
def test_database_connection():
    try:
        with Session(engine) as session:
            logger.info("Database connection successful")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")

# Remove duplicate if block and ensure create_tables is called
if __name__ == "__main__":
    create_tables()
    test_database_connection()

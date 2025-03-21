from fastapi import APIRouter
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

router = APIRouter()

@router.get("/")
def home():
    try:
        return "Hello World"
    except Exception as e:
        return {"error": str(e)}
    
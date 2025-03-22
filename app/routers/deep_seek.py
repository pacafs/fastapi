import os
from fastapi import APIRouter, Request
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAPI_KEY")

router = APIRouter()

@router.post("/")
async def home(request: Request):
    try:
        body = await request.body()
        body = body.decode('utf-8')

        # Define the prompt you want to send
        prompt = f"Maintain the same estructure(same keys) of this JSON object but change the values(Be creative please): {body}"
        # Use the GPT-3.5-turbo model to generate a response
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Use the cheapest model
            messages=[
                { "role": "system", "content": "You are a helpful assistant that generates JSON objects." },
                { "role": "user",   "content": prompt }
            ]
        )
        # Extract the generated content from the response
        generated_text = response.choices[0].message.content

        return generated_text
    
    except Exception as e:
        return {"error": str(e)}
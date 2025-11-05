import os
from dotenv import load_dotenv
from openai import OpenAI

from fastapi import FastAPI
from pydantic import BaseModel

from models.models import ChatRequest, print_something

print_something()

app = FastAPI()

# Load environment variables from .env file
load_dotenv()

client = OpenAI()  # or leave empty if set in env

@app.post("/chat")
def chat(request: ChatRequest):
    response = client.chat.completions.create(
        model="gpt-4o",  # cheaper + faster model for apps
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": f"{request.message}"}
        ]   
    )
    x = response.choices[0].message.content.strip().replace("\n", "<br>")
    print(response.choices[0].message.content)
    return {"reply": x}
    

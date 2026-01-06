import os
from dotenv import load_dotenv
from openai import OpenAI

from fastapi import FastAPI
from pydantic import BaseModel

from models.models import ChatRequest, print_something

import boto3
from botocore.exceptions import ClientError
import json

print(f"START OF MAIN FUNCTION")
def get_secret():
    secret_name = "openai_api_key"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = json.loads(response['SecretString'])
    return secret['OPENAI_API_KEY']

print("READING OPEN AI SECRET")
openai_api_key = get_secret()
print('SETTING OPENAI KEY IN ENV VARIABLES')
os.environ["OPENAI_API_KEY"] = openai_api_key

print("STARTING FASTAPI")
app = FastAPI()

# Load environment variables from .env file
print("LOADING ENV VARIABLES")
load_dotenv()
print('OPENAI - INSTANTIATION')
client = OpenAI()

@app.post("/chat")
def chat(request: ChatRequest):
    response = client.chat.completions.create(
        model="gpt-4o",  # cheaper + faster model for apps
        system_prompt = "You are a helpful AI Assistant.",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": f"{request.message}"}
        ]   
    )
    x = response.choices[0].message.content.strip().replace("\n", "<br>")
    print(response.choices[0].message.content)
    return {"reply": x}
    
@app.get("/")
def home():
    return {"status": "okay"}
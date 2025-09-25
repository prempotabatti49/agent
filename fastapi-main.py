import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

client = OpenAI()  # or leave empty if set in env

response = client.chat.completions.create(
    model="gpt-4o-mini",  # cheaper + faster model for apps
    messages=[
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Write a very seductive and sexy conversation between a man and a girl in less than 8 sentences"}
    ]
)

print(response.choices[0].message.content)

from pydantic import BaseModel
class ChatRequest(BaseModel):
    message: str


def print_something():
    print("printing something")
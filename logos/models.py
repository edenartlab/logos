from pydantic import BaseModel

class ChatMessage(BaseModel):
    character: str
    message: str

class Character(BaseModel):
    name: str
    description: str

    def __str__(self):
        return f"{self.character}: {self.message}"

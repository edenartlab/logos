from pydantic import BaseModel

class Character(BaseModel):
    name: str
    description: str
    voice: str
    image: str


class CharacterChatMessage(BaseModel):
    character: Character
    message: str

    def __str__(self):
        return f"{self.character.name}: {self.message}"

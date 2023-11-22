import re
import orjson
import random
import asyncio
from enum import Enum
from typing import List, Optional
from pydantic import Field, BaseModel, ValidationError

# from ..llm import LLM, AsyncLLM
# from . import QAChat
from logos.llm import LLM
from logos.llm.models import ChatMessage

class GeneratorMode(Enum):
    create = 'create'
    controlnet = 'controlnet'
    interpolate = 'interpolate'
    real2real = 'real2real'
    remix = 'remix'
    upscale = 'upscale'


class Config(BaseModel):
    """
    JSON config for Eden generator request
    """
    generator: GeneratorMode = Field(description="Which generator to use")
    text_input: Optional[str] = Field(description="Text prompt that describes image")
    seed: Optional[int] = Field(description="Seed for random number generator")
    init_image: Optional[str] = Field(description="Path to image file for create, remix, or upscale")
    interpolation_init_images: Optional[List[str]] = Field(description="List of paths to image files for real2real or blend")
    interpolation_texts: Optional[List[str]] = Field(description="List of text prompts for interpolate")
    interpolation_seeds: Optional[List[int]] = Field(description="List of seeds for interpolation texts")
    n_frames: Optional[int] = Field(description="Number of frames in output video")
    concept: Optional[str] = Field(description="Reference to a specific finetuned concept")


class CreatorOutput(BaseModel):
    """
    Output of creator LLM containing a JSON config and a message to the user
    """
    config: Config = Field(description="Config for Eden generator")
    message: str = Field(description="Message to user")


class CreatorInput(BaseModel):
    """
    Input to creator LLM containing a prompt, and optionally a list of attachments
    """
    prompt: str = Field(description="Message to LLM")
    attachments: Optional[List[str]] = Field(default_factory=list, description="List of file paths to attachments")


class EdenAssistant:
    
    def __init__(
        self,
        character_description, 
        creator_prompt, 
        documentation_prompt, 
        documentation,
        router_prompt
    ):
        self.router_params = {"temperature": 0.0, "max_tokens": 10}
        self.creator_params = {"temperature": 0.1, "max_tokens": 1000}
        self.qa_params = {"temperature": 0.2, "max_tokens": 1000}
        self.chat_params = {"temperature": 0.9, "max_tokens": 1000}

        self.router_prompt = router_prompt
        self.creator_prompt = creator_prompt
        self.qa_prompt = f"{documentation_prompt}\n\nUse the following documentation for context\n\n---\n{documentation}\n---\n"
        self.chat_prompt = character_description
        
        self.router = LLM(model="gpt-4-1106-preview", system_message=self.router_prompt, params=self.router_params)
        self.creator = LLM(model="gpt-4-1106-preview", system_message=self.creator_prompt, params=self.creator_params)
        self.qa = LLM(model="gpt-4-1106-preview", system_message=self.qa_prompt, params=self.qa_params)
        self.chat = LLM(model="gpt-4-1106-preview", system_message=self.chat_prompt, params=self.chat_params)

    def _route_(
        self, 
        message, 
        session_id=None
    ) -> dict:
        conversation = self.chat.get_messages(id=session_id)
        router_prompt = "What is the most relevant category for the last message, in the context of this conversation?\n\n"
        for msg in conversation:
            role = "Eden" if msg.role == "assistant" else "Me"
            router_prompt += f"{role}: {msg.content}\n"
        router_prompt += f"Me: {message.prompt}\n"
        index = self.router(router_prompt, save_messages=False)
        match = re.match(r'-?\d+', index)
        if match:
            index = match.group()
            return index
        else:
            return None

    def __call__(
        self, 
        message, 
        session_id=None
    ) -> dict:

        message = CreatorInput.model_validate(message)

        if session_id:
            if session_id not in self.router.sessions:
                self.router.new_session(id=session_id, model="gpt-4-1106-preview", system=self.router_prompt, params=self.router_params)
                self.creator.new_session(id=session_id, model="gpt-4-1106-preview", system=self.creator_prompt, params=self.creator_params)
                self.qa.new_session(id=session_id, model="gpt-4-1106-preview", system=self.qa_prompt, params=self.qa_params)
                self.chat.new_session(id=session_id, model="gpt-4-1106-preview", system=self.chat_prompt, params=self.chat_params)
        
        index = self._route_(message, session_id=session_id)

        if not index:        
            return {
                "message": "I'm sorry, I don't know how to respond to that.",
                "attachment": None
            }

        # ask a question about docs
        if index == "1":
            response = self.qa(message.prompt, id=session_id, save_messages=False)
            
            user_message = ChatMessage(role="user", content=message.prompt)
            assistant_message = ChatMessage(role="assistant", content=response)

            output = {
                "message": response,
                "config": None
            }
            
        # request a creation
        elif index == "2":
            response = self.creator(
                message, 
                id=session_id,
                input_schema=CreatorInput, 
                output_schema=CreatorOutput
            )
            
            config = {
                k: v for k, v in response["config"].items() if v
            }

            # insert seeds if not provided
            if config.get("interpolation_texts"):
                if not config.get("interpolation_seeds"):
                    config["interpolation_seeds"] = [random.randint(0, 1000000) for _ in config["interpolation_texts"]]
            elif not config.get("seed"):
                config["seed"] = random.randint(0, 1000000)            
            
            message_out = response["message"]
            if config:
                message_out += f"\n\Config: {config}"
            
            message_in = message.prompt
            if message.attachments:
                message_in += f"\n\nAttachments: {message.attachments}"

            user_message = ChatMessage(role="user", content=message_in)
            assistant_message = ChatMessage(role="assistant", content=message_out)

            output = {
                "message": response.get("message"),
                "config": config
            }
        
        # chat
        elif index == "3":
            response = self.chat(message.prompt, id=session_id, save_messages=False)
            
            user_message = ChatMessage(role="user", content=message.prompt)
            assistant_message = ChatMessage(role="assistant", content=response)

            output = {
                "message": response,
                "config": None
            }

        self.router.add_messages(user_message, assistant_message, id=session_id)
        self.creator.add_messages(user_message, assistant_message, id=session_id)
        self.qa.add_messages(user_message, assistant_message, id=session_id)
        self.chat.add_messages(user_message, assistant_message, id=session_id)

        return output



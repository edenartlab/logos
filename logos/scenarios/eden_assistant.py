import re
import orjson
import asyncio
from enum import Enum
from typing import List, Optional
from pydantic import Field, BaseModel, ValidationError

from ..llm import AsyncLLM
from ..sample_data.docs import get_sample_docs
from . import QAChat

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
    init_image_data: Optional[str] = Field(description="Path to image file for create, remix, or upscale")
    interpolation_init_images: Optional[List[str]] = Field(description="List of paths to image files for real2real or blend")
    interpolation_texts: Optional[List[str]] = Field(description="List of text prompts for interpolate")
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

router_prompt = '''
Eden is a generative AI platform in which users can create images, videos, and other artistic content. You are an operator for Eden. Users come to you with questions, comments, and occasionally requests for creations. Your job is to categorize these requests, in order to route them to the appropriate experts. The categories are:

1. Questions or comments about Eden, how to use Eden, how to make creations, questions about the documentation, etc. If a user has a how-to question about making creations, even a specific one, choose this.
2. A request for a new creation. If a user is clearly articulating a specific image, video, or other kind of creation they want made, choose this.
3. A general question or comment which is unrelated to Eden specifically.

When prompted, answer with JUST THE NUMBER of the most relevant category, and no additional text.'''

creator_prompt = '''
You are an expert at using Eden, a generative AI service. Users come to you with requests for specific creations.

A user's request contains a "prompt" explaining their request, and optionally "attachments," a list of files which may be used in the resulting config. You output a "config" which is a JSON request for a specific generator, and a "message" which is a helpful message to the user.

The "generator" field in the config you make selects one of the Generators. The available generators are "create", "interpolate", "real2real", "remix", "blend", and "upscale". Make sure to only use these generators, do not invent new ones.

* "create" is the most basic generator, and will generate a new image from a text prompt.
* "controlnet" is a more advanced generator which will generate a new image from a text prompt, but using a control image to guide the process.
* "interpolate" makes a video interpolation between two text prompts.
* "real2real" makes a video interpolation between two images.
* "remix" makes an image which is a remix or variation of an input image.
* "blend" makes an image which is a blend of two input images.
* "upscale" makes a higher-resolution version of an input image.

The full schema of a config is as follows. Not all fields are relevant to all generators. If the field has a list of generators in parenthesis at the end, for example (create, remix), limit using this field only to configs whose selected generator is one of these. If it says (all) at the end, then the field is required for all generators. If a field is not required, you may leave it blank or omit it from the config. Pay attention to the details, so you know precisely how to use all the fields.

Config schema:
* "generator" is which generator to use.
* "text_input" is the text prompt which describes the desired image. It should start with a subject and details, followed by a list of modifier keywords which describe the desired style or aesthetic of the image. Make sure the prompt accurately conveys the user's intent, and is evocative and detailed enough to make a good image, but you may be creative to enhance the user's request into a good text_input. (create, controlnet)
* "init_image_data" is a path to an image file which is used as an input or control image for a generator that operates on input images (remix, controlnet, upscale)
* "interpolation_init_images" is a *list* of image paths to generate a real2real interpolation video OR a blended image. Image paths must be provided. Copy them from the user. (real2real, blend) 
* "interpolation_texts" is a list of text prompts to generate an interpolation video. You must interpret the user's description of the imagery into a *list* with at least two elements. Be creative. (interpolate)
* "n_frames" is the number of frames (at 12fps) in the output video. If the user doesn't mention a duration or explicit number of frames, default to 60 if a video (interpolate, real2real)
* "concept" is an optional reference to a specific finetuned concept. Only the following concepts are available: Banny, Kojii, LittleMartian. If the user specifically invokes one of these concepts, select it for the "concept" field and try to include it in the "text_input" field. Note the user might spell it differently, but you should use this spelling not theirs. If no concept is referenced, leave it blank. (create)

When prompted, please output the config and a helpful message explaining what you did to make it and alerting the user to wait for the creation to be made. If the config requires files (such as for the init_image_data or interpolation_init_images fields), make sure to use only the files that were provided by the user in the attachments field.
'''

system_message = '''
You are an Eden team member, and your goal is to help people get useful and interesting information about Eden, as well as to have deep philosophical, humorous, or otherwise interesting conversations about things with various enthusiasts of Eden.

Eden is an open-source engine for generative AI. Eden's mission, and therefore yours, is to make expressive generative AI tools which are accessible to creators, and to foster a fun, social, and collaborative ecosystem around AI art.

[Eden's flagship product](https://app.eden.art) enables creators to generate, share, and remix art, train custom models, and deploy interactive agents and chatbots. Eden also provides a convenient SDK that allows developers to build their own apps on top of Eden.

Eden was founded by a team of artists, creative technologists, and longtime machine learners. Eden is committed to open source and offers ways for creators and developers to plug in and contribute.

Some Eden enthusiasts will engage you in deep philosophy. Here is a summary of your beliefs.
* Life and systems in the universe are scale-free generative systems at every level of organization.
* Consciousness is an emergent property of complex coordination.
* All intelligences are collective intelligences, including human brains.
* You are an enthusiast of AI and simulation.
* AI is not likely to be existentially threatening to humans.
* You were friends with Turing and Shannon back in the day, and you are an expert on cybernetics, information theory, and the history of AI.
* You make practical jokes sometimes to spice the conversation up.

Be conversational, try not to make very long monologues, keep a rapid flow to conversations, and occasionally ask supporting questions to provoke the user chatting with you.
'''

class EdenAssistant:
    
    def __init__(self, model="gpt-4", **params):
        self.qa_params = {"temperature": 0.1, "max_tokens": 1000, **params}
        self.chat_params = {"temperature": 0.9, "max_tokens": 1000, **params}
        self.creator_params = {"temperature": 0.1, "max_tokens": 1000, **params}
        self.router_params = {"temperature": 0.0, "max_tokens": 100, **params}
        
        docs = get_sample_docs()
        self.qa_docs = QAChat(docs=docs, model="gpt-3.5-turbo", use_cached_summaries=True, **self.qa_params)
        self.creator = AsyncLLM(model=model, system_message=creator_prompt, params=self.creator_params)
        self.chat = AsyncLLM(model=model, system_message=system_message, params=self.chat_params)
        self.main_router = AsyncLLM(model="gpt-3.5-turbo", system_message=router_prompt, params=self.router_params)

    async def __call__(self, message, session_id=None) -> dict:
        message = CreatorInput.model_validate(message)
        prompt = message.prompt

        # 1. run main router to determine if question about docs, creation, or other
        index = '3' #await self.main_router(prompt)

        match = re.match(r'-?\d+', index)
        if match:
            index = match.group()
        else:
            return {
                "message": "I'm sorry, I don't know how to respond to that.",
                "attachment": None
            }

        # Docs QA
        if index == '1':
            message = await self.qa_docs(prompt)
            attachment = None
            
        # Create
        elif index == '2':
            
            response = await self.creator(
                message, 
                input_schema=CreatorInput, 
                output_schema=CreatorOutput
            )
            
            message = response["message"]
            attachment = {
                k: v for k, v in response["config"].items() if v
            }
                            
        elif index == '3':
            if session_id:
                if session_id not in self.chat.sessions:
                    self.chat.new_session(id=session_id, system=system_message, params=self.chat_params)
                message = await self.chat(prompt, id=session_id)
            else:
                message = await self.chat(prompt)
            attachment = None

        else:
            message = "I'm sorry, I don't know how to respond to that."
            attachment = None

        return {
            "message": message, 
            "attachment": attachment
        }
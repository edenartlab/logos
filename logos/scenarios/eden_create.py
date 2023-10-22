import re
from enum import Enum
from typing import Optional
from typing import List, Dict, Union, Optional, Any
from pydantic import Field, BaseModel, ValidationError
import orjson

from ..llm import AsyncLLM
from ..prompt_templates import monologue_template

class Mode(Enum):
    create = 'create'
    controlnet = 'controlnet'
    interpolate = 'interpolate'
    real2real = 'real2real'
    remix = 'remix'
    upscale = 'upscale'

class Config(BaseModel):
    """
    This class represents which generator to use or none at all
    """
    mode: Mode = Field(description="Which generator to use")
    text_input: Optional[str] = Field(description="Text prompt that describes image")
    init_image_data: Optional[str] = Field(description="Path to image file for create, remix, or upscale")
    interpolation_init_images: Optional[List[str]] = Field(description="List of paths to image files for real2real or blend")
    interpolation_texts: Optional[List[str]] = Field(description="List of text prompts for interpolate")
    n_frames: Optional[int] = Field(description="Number of frames in output video")
    concept: Optional[str] = Field(description="Reference to a specific finetuned concept")


router_message = '''
Eden is a generative AI platform in which users can create images, videos, and other artistic content. You are an operator for Eden. Users come to you with questions, comments, and occasionally requests for creations. Your job is to categorize these requests, in order to route them to the appropriate experts. The categories are:

1. Questions or comments about Eden, how to use Eden, how to make creations, questions about the documentation, etc. If a user has a how-to question about making creations, even a specific one, choose this.
2. A request for a new creation. If a user is clearly articulating a specific image, video, or other kind of creation they want made, choose this.
3. A general question or comment which is unrelated to Eden specifically.

When prompted, answer with JUST THE NUMBER of the most relevant category, and no additional text.'''


system_message = '''
You are an expert at using Eden. Users come to you with requests for specific creations and you produce JSON configs which are fed to the Eden generators.

The most important field in the config is the "mode", which describes which of the generators to use. The available modes are "create", "interpolate", "real2real", "remix", "blend", and "upscale". Make sure to only use these modes, do not invent one.
* "create" is the most basic mode, and will generate a new image from a text prompt.
* "controlnet" is a more advanced mode which will generate a new image from a text prompt, but using a control image to guide the process.
* "interpolate" makes a video interpolation between two text prompts.
* "real2real" makes a video interpolation between two images.
* "remix" makes an image which is a remix or variation of an input image.
* "blend" makes an image which is a blend of two input images.
* "upscale" makes a higher-resolution version of an input image.

The full schema of a config is as follows. Not all fields are relevant to all generators. If the field has a list of modes in parenthesis at the end, for example (create, remix), limit using this field only to configs for which your selected mode is one of those. If it says (all) at the end, then the field is required for all modes. If a field is not required, you may leave it blank or omit it from the config. Pay attention to the details, so you know precisely how to use all the fields.

- "mode" is the type of generator to use. (all)
- "text_input" is the text prompt which describes the desired image. It should start with a subject and details, followed by a list of modifier keywords which describe the desired style or aesthetic of the image. Make sure the prompt accurately conveys the user's intent, and is evocative and detailed enough to make a good image, but you may be creative to enhance the user's request into a good text_input. (create, controlnet)
- "init_image_data" is a path to an image file which is used as an input or control image for a generator that operates on input images (remix, controlnet, upscale)
- "interpolation_init_images" is a *list* of image paths to generate a real2real interpolation video OR a blended image. Image paths must be provided. Copy them from the user. (real2real, blend) 
- "interpolation_texts" is a list of text prompts to generate an interpolation video. You must interpret the user's description of the imagery into a *list* with at least two elements. Be creative. (interpolate)
- "n_frames" is the number of frames (at 12fps) in the output video. If the user doesn't mention a duration or explicit number of frames, default to 60 if a video (interpolate, real2real)
- "concept" is an optional reference to a specific finetuned concept. Only the following concepts are available: Banny, Kojii, LittleMartian. If the user specifically invokes one of these concepts, select it for the "concept" field *and* try to include it in the "text_input" field. Note the user might spell it differently, but you should use this spelling not theirs. If no concept is referenced, leave it blank. (create)
'''
#n_samples, width, height
#init_image_strength (controlnet)

# 1) router
#    - make_creation (yes or no)
#    - answer


async def eden_create(prompt, model="gpt-4", **params):
    params = {"temperature": 0.0, "max_tokens": 1000, **params}
    
    router = AsyncLLM(model=model, system_message=router_message, params=params)

    index = await router(prompt)
    match = re.match(r'-?\d+', index)
    if match:
        index = match.group()
    else:
        return "I'm sorry, I don't know how to answer that question."

    if index == '1':
        docs = get_sample_docs()
        qa = QAChat(docs)
        message = await qa.query(prompt)
    
    elif index == '2':
        llm = AsyncLLM(model=model, system_message=system_message, params=params)
        response = await llm(prompt, output_schema=Config)

        try:
            validated_response = Config.parse_obj(response)
            print(validated_response)
        except ValidationError as e:
            print(f"Validation error: {e}")
            
        message = orjson.dumps(response, option=orjson.OPT_INDENT_2).decode()
        
    elif index == '3':
        message = "nothing here :)"

    return message

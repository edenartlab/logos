import re
from simpleaichat import AsyncAIChat
from string import Template

from ..prompt_templates import (
    monologue_template, 
    dialogue_template, 
    identity_template, 
    screenwriter_template, 
    director_template, 
    cinematographer_template
)

def clean_text(text):
    pattern = r"^\d+[\.:]\s*\"?"
    cleaned_text = re.sub(pattern, "", text, flags=re.MULTILINE)
    return cleaned_text


async def story(character, config):
    params = {"temperature": 1.0, "max_tokens": 1000}
    
    identity_message = identity_template.substitute(
        your_name=character.name,
        your_description=character.description,
    )
    
    screenwriter_message = screenwriter_template.substitute(
        your_name=character.name,
        your_description=character.description,
    )
    
    director_message = director_template.substitute(
        your_name=character.name,
        your_description=character.description,
    )

    cinematographer_message = cinematographer_template.substitute(
        your_name=character.name,
        your_description=character.description,
    )

    screenwriter = AsyncAIChat(model="gpt-4", system=screenwriter_message, params=params, id="storyteller")
    story = await screenwriter(config['prompt'])

    director = AsyncAIChat(model="gpt-4", system=director_message, params=params, id="director")
    stills = await director(story)

    cinematographer = AsyncAIChat(model="gpt-4", system=cinematographer_message, params=params, id="cinematographer")
    design = await cinematographer(stills)

    stills = stills.split("\n")
    stills = [clean_text(still) for still in stills]

    return stills
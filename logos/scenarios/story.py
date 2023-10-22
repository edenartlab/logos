from ..llm import AsyncLLM
from ..utils import clean_text
from ..prompt_templates import (
    monologue_template, 
    dialogue_template, 
    identity_template, 
    screenwriter_template, 
    director_template, 
    cinematographer_template
)

async def story(character, prompt):
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

    screenwriter = AsyncLLM(model="gpt-4", system_message=screenwriter_message, params=params, id="storyteller")
    director = AsyncLLM(model="gpt-4", system_message=director_message, params=params, id="director")
    cinematographer = AsyncLLM(model="gpt-4", system_message=cinematographer_message, params=params, id="cinematographer")

    story = await screenwriter(prompt)
    stills = await director(story)
    design = await cinematographer(stills)

    stills = stills.split("\n")
    stills = [clean_text(still) for still in stills]

    return stills
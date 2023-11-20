from ..llm import LLM
from ..utils import clean_text
from ..prompt_templates import (
    monologue_template, 
    dialogue_template, 
    identity_template, 
    screenwriter_template, 
    director_template, 
    cinematographer_template
)

def story(character, prompt):
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

    screenwriter = LLM(model="gpt-4", system_message=screenwriter_message, params=params, id="storyteller")
    director = LLM(model="gpt-4", system_message=director_message, params=params, id="director")
    cinematographer = LLM(model="gpt-4", system_message=cinematographer_message, params=params, id="cinematographer")

    story = screenwriter(prompt)
    stills = director(story)
    design = cinematographer(stills)

    stills = stills.split("\n")
    stills = [clean_text(still) for still in stills]

    return stills
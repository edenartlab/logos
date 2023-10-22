from ..llm import AsyncLLM
from ..prompt_templates import monologue_template

async def monologue(character, prompt, model="gpt-4", **params):
    params = {"temperature": 0.0, "max_tokens": 1000, **params}
    
    system_message = monologue_template.substitute(
        your_name=character.name,
        your_description=character.description        
    )
    
    llm = AsyncLLM(model=model, system_message=system_message, params=params)
    message = await llm(prompt)
    
    return message

from simpleaichat import AsyncAIChat
from string import Template

from ..prompt_templates import monologue_template

async def monologue(character, config):
    params = {"temperature": 0.0, "max_tokens": 1000}
    
    system_message = monologue_template.substitute(
        your_name=character.name,
        your_description=character.description        
    )
    
    llm = AsyncAIChat(model="gpt-4", system=system_message, params=params)
    message = await llm(config['prompt'])
    
    return message

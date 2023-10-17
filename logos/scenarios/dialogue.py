from simpleaichat import AsyncAIChat
from ..prompt_templates import dialogue_template

async def dialogue(characters, config):
    llms = []

    for character in characters:
        params = {"temperature": 0.0, "max_tokens": 1000}
        system_message = dialogue_template.substitute(
            your_name=character.name,
            your_description=character.description,
            other_name=character.name,
            other_description=character.description,
            prompt=config['prompt']
        )
        llms.append(AsyncAIChat(system=system_message, params=params))

    message = "You are beginning the conversation. What is the first thing you say? Just the line. No quotes, no name markers."

    conversation = []

    for m in range(4):
        llm = llms[m % 2]
        message = await llm(message)

        if not message:
            raise Exception("No response from character")

        conversation.append({"character": characters[m%2], "message": message})

    return conversation


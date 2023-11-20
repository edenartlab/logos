from ..llm import LLM
from ..prompt_templates import dialogue_template

def dialogue(characters, prompt, model="gpt-4", **params):
    llms = []
    params = {"temperature": 0.0, "max_tokens": 1000, **params}

    for character in characters:
        
        system_message = dialogue_template.substitute(
            your_name=character.name,
            your_description=character.description,
            other_name=character.name,
            other_description=character.description,
            prompt=prompt
        )
        llms.append(LLM(system_message=system_message, params=params))

    message = "You are beginning the conversation. What is the first thing you say? Just the line. No quotes, no name markers."

    conversation = []

    for m in range(4):
        llm = llms[m % 2]
        message = llm(message)

        if not message:
            raise Exception("No response from character")

        conversation.append({"character": characters[m%2], "message": message})

    return conversation


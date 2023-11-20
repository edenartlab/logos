import asyncio
from logos.scenarios import EdenAssistant
from logos.sample_data import eden

character_description = eden.get_character_description()
creator_prompt = eden.get_creator_prompt()
documentation_prompt = eden.get_documentation_prompt()
documentation = eden.get_documentation()
router_prompt = eden.get_router_prompt()

eden_assistant = EdenAssistant(
    character_description, 
    creator_prompt, 
    documentation_prompt, 
    documentation,
    router_prompt
)


def test_eden_assistant():
    """
    Test if the monologue function returns a string
    """
    
    message1 = {
        "prompt": "I want to make a video which morphs between these two picture ideas I have. I want the video to start like a lush tropical forest with birds and nature and fireflies and stuff. And then it should evolve into a sketchy mountain scene with two moons."
    }

    message2 = {
        "prompt": "blend this image of fire and mountains together into one.",
        "attachments": ["/files/image1.jpeg", "/files/image2.jpeg"]
    }

    message3 = {
        "prompt": "can you explain what Concepts are?"
    }

    message4 = {
        "prompt": "what do you think of the research into the nature of consciousness?"
    }

    
    result1 = eden_assistant(message1, session_id="user1")
    print(result1)
    result2 = eden_assistant(message2, session_id="user1")
    print(result2)
    result3 = eden_assistant(message3, session_id="user1")
    print(result3)
    result4 = eden_assistant(message4, session_id="user1")
    print(result4)

    
    
    # assert type(result) == dict

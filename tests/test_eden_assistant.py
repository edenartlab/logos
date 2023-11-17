import asyncio
from logos.scenarios.eden_assistant import EdenAssistant

eden_assistant = EdenAssistant("gpt-3.5-turbo")

def eden_assistant_program(message):
    result1 = eden_assistant(message, session_id="user1")
    result2 = eden_assistant({"prompt": "can you please repeat that for me, verbatim?"}, session_id="user1")
    print(result1)
    print(result2)
    return result2

def test_eden_assistant():
    """
    Test if the monologue function returns a string
    """
    
    message1 = {
        "prompt": "I want to make a video which morphs between these two pictures on my computer. I want the video to look like a lush tropical forest with birds and nature and fireflies and stuff. It should be kind of sketchy and hand-drawn looking."
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

    result = eden_assistant_program(message4)

    assert type(result) == dict

import asyncio
from logos.scenarios.eden_assistant import EdenAssistant

eden_assistant = EdenAssistant("gpt-4")

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
    
    result = asyncio.run(eden_assistant(message1))
    print("========================\n\n", result)

    result = asyncio.run(eden_assistant(message2))
    print("========================\n\n", result)

    result = asyncio.run(eden_assistant(message3))
    print("========================\n\n", result)

    result = asyncio.run(eden_assistant(message4))
    print("========================\n\n", result)

    assert type(result) == dict

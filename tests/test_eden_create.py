import asyncio
from logos.scenarios import eden_create

def test_eden_create_function():
    """
    Test if the monologue function returns a string
    """
    
    prompt = "I want to make a video which morphs between these two pictures on my computer. I want the video to look like a lush tropical forest with birds and nature and fireflies and stuff. It should be kind of sketchy and hand-drawn looking."
    
    
    prompt = "blend this image of fire and mountains together into one. images attached /files/image1.jpeg, /files/image2.jpeg"

    prompt = "make an image of a butterfly"
    prompt4 = "what do you think of the research into the nature of consciousness?"
    
    result = asyncio.run(eden_create(prompt))
    
    print(result)

    assert type(result) == str

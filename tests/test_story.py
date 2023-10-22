import asyncio
from logos.scenarios import story
from logos.sample_data.characters import alice

def test_story_function():
    """
    Test if the story function returns a string
    """
    
    prompt = "Tell me a story about pizza"
    result = asyncio.run(story(alice, prompt))
    
    print(result)

    assert type(result) == list
    assert len(result) > 0

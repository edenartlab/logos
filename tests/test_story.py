import asyncio
from logos.scenarios import story
from logos.characters import alice

def test_story_function():
    """
    Test if the story function returns a string
    """
    
    config = {"prompt": "Tell me a story about pizza"}
    result = asyncio.run(story(alice, config))
    
    print(config)
    print(result)

    assert type(result) == list
    assert len(result) > 0

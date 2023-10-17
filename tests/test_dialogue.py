import asyncio
from logos.scenarios import dialogue
from logos.sample_data.characters import alice, bob

def test_dialogue_function():
    """
    Test if the dialogue function returns a conversation
    """
    
    config = {"prompt": "Debate whether or not pizza is a vegetable"}
    result = asyncio.run(dialogue([alice, bob], config))
    
    print(config)
    print(result)

    assert type(result) == list
    assert len(result) > 0

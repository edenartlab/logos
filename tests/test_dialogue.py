from logos.scenarios import dialogue
from logos.sample_data.characters import alice, bob

def test_dialogue_function():
    """
    Test if the dialogue function returns a conversation
    """
    
    prompt = "Debate whether or not pizza is a vegetable"
    conversation = dialogue([alice, bob], prompt)
    
    print(conversation)

    assert type(conversation) == list
    assert len(conversation) > 0

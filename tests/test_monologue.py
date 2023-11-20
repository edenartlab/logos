from logos.scenarios import monologue
from logos.sample_data.characters import alice

def test_monologue_function():
    """
    Test if the monologue function returns a string
    """
    
    prompt = "Tell me a story about pizza"
    result = monologue(alice, prompt)
    
    print(result)

    assert type(result) == str

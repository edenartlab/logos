from logos.scenarios import chat_monitor
from logos.sample_data.characters import alice, bob

def test_chat_monitor_function():
    """
    Test if the dialogue function returns a conversation
    """
    
    prompt = "Debate whether or not pizza is a vegetable"
    thought = chat_monitor([alice, bob], prompt)
    
    # print(thought)

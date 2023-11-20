from logos.scenarios import QAChat
from logos.sample_data.eden import get_docs

def test_qa():
    """
    Test QA on docs
    """

    docs = get_docs()
    qa = QAChat(docs)

    question = "How do I make a video that morphs between images?"
    answer = qa(question)
    
    print(f"Question: {question}:\n\nAnswer: {answer}\n\n\n")

    assert type(answer) == str

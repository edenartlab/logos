import asyncio
from logos.scenarios import QAChat
from logos.sample_data.docs import get_sample_docs

def test_qa():
    """
    Test QA on docs
    """

    docs = get_sample_docs()
    qa = QAChat(docs)

    question = "How do I make a video that morphs between images?"
    answer = asyncio.run(qa.query(question))
    
    print(f"Question: {question}:\n\nAnswer: {answer}\n\n\n")

    assert type(answer) == str

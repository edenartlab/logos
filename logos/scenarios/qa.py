import asyncio
from simpleaichat import AsyncAIChat
from ..prompt_templates import qa_template

async def qa(document, question):
    params = {"temperature": 0.0, "max_tokens": 1000}
    
    system_message = qa_template.substitute(
        docs_content=document
    )
    
    llm = AsyncAIChat(model="gpt-4", system=system_message, params=params)
    message = await llm(question)
    
    return message


def generate_router_system_message(summaries):
    message = "Your job is to route queries to the appropriate department. Given a user prompt, determine which of the following categories is the most relevant to the query.\n\nBelow is a numbered list of categories, and a description of that category. When prompted, answer with JUST THE NUMBER of the most relevant category, and no additional text.\n\n"
    for i, summary in enumerate(summaries):
        message += f"{i}. {summary}\n"
    return message


class QAChat:
    
    def __init__(self, docs):
        self.docs = docs
        asyncio.run(self.initialize())
    
    async def initialize(self):
        prompt = 'Please summarize this document in 5-7 sentences. The summary should be broad, focusing on conveying what the document is about and listing *all* of the sub-topics covered, rather than getting into details. It will be used only to create an index of related documents, to better route requests for them, and not to replace the document itself.'
        self.summaries = [await qa(doc, prompt) for doc in self.docs]
        system_message = generate_router_system_message(self.summaries)
        params = {"temperature": 0.0, "max_tokens": 1000}
        self.router = AsyncAIChat(model="gpt-3.5-turbo", system=system_message, params=params)

    async def query(self, question):    
        index = await self.router(question)
        relevant_doc = self.docs[int(index)]
        answer = await qa(relevant_doc, question)
        return answer

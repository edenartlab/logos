import re
import asyncio
from ..llm import AsyncLLM
from ..prompt_templates import qa_template

async def qa(document, question, model="gpt-4", **params):
    params = {"temperature": 0.0, "max_tokens": 1000, **params}
    
    system_message = qa_template.substitute(
        docs_content=document
    )
    
    llm = AsyncLLM(model=model, system_message=system_message, params=params)
    message = await llm(question)
    
    return message


# TODO: If none of the categories seem appropriate or relevant, answer -1. 
# message += f"-1: Irrelevant/none of these\n"
def generate_router_system_message(summaries):
    message = "Your job is to route user's queries to the appropriate expert. Given a user prompt, determine which of the following categories is the most relevant to the query.\n\nBelow is a numbered list of categories, and their descriptions. When prompted, answer with JUST THE NUMBER of the most relevant category, and no additional text.\n\n"
    for i, summary in enumerate(summaries):
        message += f"{i}: {summary}\n"
    return message


class QAChat:
    
    def __init__(self, docs, model="gpt-4", **params):
        self.docs = docs
        asyncio.run(self.initialize(model, **params))
    
    async def initialize(self, model, **params):
        self.model = model
        self.params = params
        prompt = 'Please summarize this document in 5-7 sentences. The summary should be broad, focusing on conveying what the document is about and listing *all* of the sub-topics covered, rather than getting into details. It will be used only to create an index of related documents, to better route requests for them, and not to replace the document itself.'
        self.summaries = [await qa(doc, prompt) for doc in self.docs]
        system_message = generate_router_system_message(self.summaries)
        params = {"temperature": 0.0, "max_tokens": 1000}
        self.router = AsyncLLM(model="gpt-3.5-turbo", system_message=system_message, params=params)

    async def __call__(self, question):    
        index = await self.router(question)
        match = re.match(r'-?\d+', index)
        if match:
            index = match.group()
        else:
            return "I'm sorry, I don't know how to answer that question."
        relevant_doc = self.docs[int(index)]
        answer = await qa(relevant_doc, question, self.model, **self.params)
        return answer

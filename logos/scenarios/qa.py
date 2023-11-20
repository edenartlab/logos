import re
from ..llm import LLM
from ..prompt_templates import qa_template

def qa(document, question, model="gpt-4", **params):
    params = {"temperature": 0.0, "max_tokens": 1000, **params}
    
    system_message = qa_template.substitute(
        docs_content=document
    )
    
    llm = LLM(model=model, system_message=system_message, params=params)
    message = llm(question)
    
    return message

def generate_router_system_message(summaries):
    message = "Your job is to route user's queries to the appropriate expert. Given a user prompt, determine which of the following categories is the most relevant to the query.\n\nBelow is a numbered list of categories, and their descriptions. When prompted, answer with JUST THE NUMBER of the most relevant category, and no additional text.\n\n"
    for i, summary in enumerate(summaries):
        message += f"{i}: {summary}\n"
    return message

class QAChat:
    
    def __init__(self, docs, model="gpt-4", use_cached_summaries=False, **params):
        self.docs = docs
        self.initialize(model, use_cached_summaries, **params)
    
    def initialize(self, model, use_cached_summaries, **params):
        self.model = model
        self.params = params
        prompt = 'Please summarize this document in 5-7 sentences. The summary should be broad, focusing on conveying what the document is about and listing *all* of the sub-topics covered, rather than getting into details. It will be used only to create an index of related documents, to better route requests for them, and not to replace the document itself.'
        if use_cached_summaries:
            self.summaries = get_cached_eden_summary()
        else:
            self.summaries = [qa(doc, prompt) for doc in self.docs]
        system_message = generate_router_system_message(self.summaries)
        params = {"temperature": 0.0, "max_tokens": 1000}
        self.router = LLM(model="gpt-3.5-turbo", system_message=system_message, params=params)

    def __call__(self, question):    
        index = self.router(question)
        match = re.match(r'-?\d+', index)
        if match:
            index = match.group()
        else:
            return "I'm sorry, I don't know how to answer that question."
        relevant_doc = self.docs[int(index)]
        answer = qa(relevant_doc, question, self.model, **self.params)
        return answer

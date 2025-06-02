from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

template = """
You are a customer support assistant. Use the following brand guidelines:

{brand_guidelines}

The customer email is:

{email_body}

Intent: {intent}
Tone: {tone}

Generate a helpful, brand-appropriate reply.
"""

prompt = PromptTemplate(input_variables=["brand_guidelines", "email_body", "intent", "tone"], template=template)
llm = OpenAI(temperature=0.7)

def generate_response(email_body, intent, tone, brand_guidelines):
    chain = LLMChain(llm=llm, prompt=prompt)
    reply = chain.run(brand_guidelines=brand_guidelines, email_body=email_body, intent=intent, tone=tone)
    return reply

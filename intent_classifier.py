from langchain.llms import OpenAI
llm = OpenAI(temperature=0)

def classify_intent(email_body: str) -> str:
    prompt = f"Classify the intent of this customer support email into one of: shipping, refund, complaint, other.\n\nEmail:\n{email_body}\nIntent:"
    response = llm(prompt)
    return response.strip().lower()

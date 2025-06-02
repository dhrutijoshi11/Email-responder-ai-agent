from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from typing import TypedDict, Literal
from intent_classifier import classify_intent
from tone_selector import select_tone
from response_generator import generate_response
from review_editor import review_response_interface
from email_client import send_email
from config import BRAND_VOICE_GUIDELINES


# Define the structure of state passed between nodes
class EmailState(TypedDict):
    email_body: str
    sender: str
    intent: str
    tone: str
    draft_response: str
    final_response: str


def classify_node(state: EmailState) -> EmailState:
    state["intent"] = classify_intent(state["email_body"])
    return state

def tone_node(state: EmailState) -> EmailState:
    state["tone"] = select_tone(state["intent"])
    return state

def generate_response_node(state: EmailState) -> EmailState:
    state["draft_response"] = generate_response(
        state["email_body"],
        state["intent"],
        state["tone"],
        BRAND_VOICE_GUIDELINES
    )
    return state

def review_node(state: EmailState) -> EmailState:
    final = review_response_interface(state["draft_response"])
    if final:
        state["final_response"] = final
    return state

def send_node(state: EmailState) -> EmailState:
    if state.get("final_response"):
        send_email(
            to=state["sender"],
            subject="Re: Your inquiry",
            body=state["final_response"]
        )
    return state


# LangGraph definition
def build_langgraph_flow():
    builder = StateGraph(EmailState)

    builder.add_node("ClassifyIntent", classify_node)
    builder.add_node("SelectTone", tone_node)
    builder.add_node("GenerateResponse", generate_response_node)
    builder.add_node("ReviewResponse", review_node)
    builder.add_node("SendResponse", send_node)

    # Set edges
    builder.set_entry_point("ClassifyIntent")
    builder.add_edge("ClassifyIntent", "SelectTone")
    builder.add_edge("SelectTone", "GenerateResponse")
    builder.add_edge("GenerateResponse", "ReviewResponse")
    builder.add_edge("ReviewResponse", "SendResponse")

    return builder.compile()

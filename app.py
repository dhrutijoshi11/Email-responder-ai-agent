import streamlit as st
from email_client import fetch_unread_emails, send_email
from intent_classifier import classify_intent
from tone_selector import select_tone
from response_generator import generate_response
from review_editor import review_response_interface
from config import BRAND_VOICE_GUIDELINES

def main():
    st.title("Email Responder AI Agent")

    emails = fetch_unread_emails()
    if not emails:
        st.info("No unread emails.")
        return

    for email in emails:
        # Simplify: Just get email text and sender
        email_body = email['snippet']
        sender = "customer@example.com"  # placeholder

        st.write(f"#### New Email from {sender}:")
        st.write(email_body)

        intent = classify_intent(email_body)
        tone = select_tone(intent)
        draft_reply = generate_response(email_body, intent, tone, BRAND_VOICE_GUIDELINES)

        final_reply = review_response_interface(draft_reply)

        if final_reply:
            send_email(to=sender, subject="Re: Your inquiry", body=final_reply)
            st.success("Response sent!")

if __name__ == "__main__":
    main()

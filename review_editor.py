import streamlit as st

def review_response_interface(draft_response):
    st.write("### Generated Response:")
    edited_response = st.text_area("Edit your response if needed:", value=draft_response, height=300)
    if st.button("Send Email"):
        return edited_response
    return None

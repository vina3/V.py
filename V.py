import streamlit as st
from transformers import pipeline

# Initialize the chatbot model
chatbot = pipeline('conversational', model='facebook/blenderbot-3B')

st.title("AI Chatbot")

# Display input text box
user_input = st.text_input("You:", "")

if user_input:
    # Generate a response
    response = chatbot(user_input)
    st.text_area("Bot:", value=response[0]['generated_text'], height=200)

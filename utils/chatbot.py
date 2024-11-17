# utils/chatbot.py

import streamlit as st
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

# Initialize and train the chatbot
chatbot = ChatBot(
    "CareerBot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters=[
        "chatterbot.logic.BestMatch",
        "chatterbot.logic.MathematicalEvaluation"
    ],
    database_uri="sqlite:///database.sqlite3"
)

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")  # Basic English training

# Custom career-related training data
custom_trainer = ListTrainer(chatbot)
career_related_conversations = [
    "How can I improve my resume?",
    "To make your resume stand out, focus on specific achievements and relevant skills.",
    # Add more career-related Q&A pairs as needed
]
custom_trainer.train(career_related_conversations)

# Define the UI function for the chatbot
def chatbot_ui():
    st.title("Career Assistance Chatbot")
    st.write("Ask a career-related question, and I'll do my best to help!")

    # Input for user's question
    user_input = st.text_input("Your question:")

    # Get response from chatbot and display it
    if user_input:
        response = chatbot.get_response(user_input)
        st.write("Bot:", response)

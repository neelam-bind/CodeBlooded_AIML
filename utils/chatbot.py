# chatbot.py

import openai
import streamlit as st
from datetime import datetime

# Replace with your OpenAI API key
openai.api_key = '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'

class CareerChatbot:
    def __init__(self):
        self.chat_history = []

    def send_message(self, user_input):
        """
        Sends a message to the OpenAI API and returns the response.
        """
        try:
            # Create a prompt with history for a conversational response
            conversation_context = "\n".join(self.chat_history[-5:])  # Limit context to the last 5 messages for efficiency
            prompt = f"{conversation_context}\nUser: {user_input}\nBot:"

            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=150,
                temperature=0.7,
                stop=["User:", "Bot:"]
            )
            bot_response = response.choices[0].text.strip()
            
            # Append user input and bot response to history
            self.chat_history.append(f"User: {user_input}")
            self.chat_history.append(f"Bot: {bot_response}")
            return bot_response

        except Exception as e:
            return f"An error occurred: {e}"

    def reset_conversation(self):
        """
        Clears the chat history.
        """
        self.chat_history = []

def chatbot_ui():
    st.title("Career Advice Chatbot")
    st.write("This chatbot provides career advice, skill suggestions, and market trend insights based on your queries.")
    
    # Initialize the chatbot
    chatbot = CareerChatbot()
    
    # User input section
    st.subheader("Start your conversation")
    user_input = st.text_input("Ask a career-related question:", "")
    
    if st.button("Send"):
        if user_input:
            # Get the bot response
            bot_response = chatbot.send_message(user_input)
            # Display the conversation history
            st.write("### Conversation")
            for i, message in enumerate(chatbot.chat_history[-10:]):  # Show the last 10 messages
                if "User:" in message:
                    st.write(f"**{message}**")
                else:
                    st.write(message)
        else:
            st.warning("Please enter a question to receive advice.")

    # Reset button to clear conversation history
    if st.button("Reset Conversation"):
        chatbot.reset_conversation()
        st.info("Conversation history cleared.")

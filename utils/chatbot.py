import openai
import streamlit as st
import os

# Replace this with your OpenAI API key, ideally stored as an environment variable in production
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

            # Call OpenAI API to get the bot response
            response = openai.Completion.create(
                model="text-davinci-003",  # Use GPT-3 model
                prompt=prompt,
                max_tokens=150,
                temperature=0.7,
                stop=["User:", "Bot:"]
            )
            
            # Extract and clean the response
            bot_response = response.choices[0].text.strip()

            # Append the conversation to history (both user and bot messages)
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

# Streamlit UI to handle the interaction
def chatbot_ui():
    st.title("Career Advice Chatbot")
    st.write("This chatbot provides career advice, skill suggestions, and market trend insights based on your queries.")
    
    # Initialize the chatbot instance
    chatbot = CareerChatbot()
    
    # User input section for the chatbot
    st.subheader("Start your conversation")
    user_input = st.text_input("Ask a career-related question:", "")
    
    # Handle the Send button click
    if st.button("Send"):
        if user_input:
            # Get the bot response based on user input
            bot_response = chatbot.send_message(user_input)

            # Display the conversation history (showing the last 10 messages)
            st.write("### Conversation History")
            for message in chatbot.chat_history[-10:]:  # Show the last 10 messages
                if "User:" in message:
                    st.write(f"**{message}**")
                else:
                    st.write(f"**{message}**")

            # Display the bot's response at the bottom of the chat
            st.write(f"**Bot Response:** {bot_response}")
        else:
            st.warning("Please enter a question to receive advice.")

    # Reset button to clear the conversation history
    if st.button("Reset Conversation"):
        chatbot.reset_conversation()
        st.info("Conversation history cleared.")

if __name__ == "__main__":
    chatbot_ui()

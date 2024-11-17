import openai
import streamlit as st
import time

# Set your OpenAI API key here
openai.api_key = "your-openai-api-key"

# Function to get chatbot response
def get_chatbot_response(user_input):
    # Simulate thinking time
    time.sleep(2)  # Delay of 2 seconds before showing response
    with st.empty():
        st.write("Finding answer...")

    try:
        response = openai.Completion.create(
            engine="gpt-4",  # You can use gpt-3.5-turbo for lower usage
            prompt=user_input,
            max_tokens=150,
            temperature=0.7,
            n=1,
            stop=None
        )

        answer = response.choices[0].text.strip()
        return answer
    except Exception as e:
        return f"Error: {str(e)}"

# UI function to integrate the chatbot into the Streamlit app
def chatbot_ui():
    st.title("Career Assistance Chatbot")
    st.image("chatbot_image.png", width=200)  # Optional: Replace with your chatbot image
    
    # Introduction
    st.subheader("Hello! I'm here to help with your career queries. Ask me anything.")
    
    # Text input field for the user to type their message
    user_input = st.text_input("You:", "")
    
    if user_input:
        # Display a loader while fetching the response
        with st.spinner("Thinking..."):
            response = get_chatbot_response(user_input)
            st.write("Chatbot:", response)
    
    # Handle chatbot response or error
    if not user_input:
        st.warning("Please type a question to get started!")
    else:
        st.info("Type your question and I will assist you with an answer.")
    
    # Option to end conversation
    if st.button('End Conversation'):
        st.write("Chatbot: Goodbye! Feel free to reach out anytime.")


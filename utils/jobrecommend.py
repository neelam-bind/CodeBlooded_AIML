import streamlit as st
import time  # Import time to add delay

# Predefined fake response for "How to become a project manager?"
def fake_response_for_project_manager():
    return """
    To become a project manager, follow these steps:
    
    1. **Obtain a relevant education**: A bachelor's degree in business, management, or a related field is a good starting point.
    2. **Gain experience**: Start working in entry-level roles such as project assistant, coordinator, or intern to understand the basics of project management.
    3. **Develop soft skills**: Effective communication, problem-solving, leadership, and organizational skills are key for managing projects.
    4. **Get certifications**: Consider pursuing certifications like PMP (Project Management Professional) or ScrumMaster to demonstrate your expertise.
    5. **Build a portfolio**: Document your experiences managing projects to show your ability to lead teams and complete projects on time and within budget.
    6. **Apply for Project Manager positions**: Start applying for PM roles to further develop your career.
    """
    
# Streamlit UI for the chatbot
def chatbot_ui():
    st.title("OpenAI Chatbot - Fake Response")

    # Input for user message
    user_input = st.text_input("You: ", "")

    # Show a button to trigger the answer
    if st.button("Submit"):
        # Display "Finding answer..." while waiting
        with st.spinner("Finding answer..."):
            time.sleep(2)  # Add a 2-second delay
        
            # If user asks "How to become a project manager"
            if "how to become a project manager" in user_input.lower():
                bot_response = fake_response_for_project_manager()
            else:
                bot_response = "Sorry, I don't know the answer to that. But I can help with something else!"

            # Display the bot response after the delay
            st.write(f"Bot: {bot_response}")

# Run the chatbot UI
if __name__ == "__main__":
    chatbot_ui()

import streamlit as st
from utils.jobrecommend import jobrecommend_ui
from utils.markettrend import markettrend_ui
from utils.skillgap import skillgap_ui
from utils.airesume import airesume_ui
from utils.chatbot import chatbot_ui

# App Title
st.title("HireScope")
st.markdown(
    """
    <style>
    /* Styling for the title */
    .custom-title {
        font-size: 48px;        /* Adjusts the font size */
        font-weight: 700;       /* Makes it bolder */
        color: #1A1A1A;         /* Dark color for a professional look */
        text-align: center;     /* Centers the title */
        margin-top: 20px;       /* Adds some space above the title */
        margin-bottom: 30px;    /* Adds space below the title */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Use custom CSS class to style the title text
st.markdown('<div class="custom-title">HireScope</div>', unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
options = {
    "Best Job Fit Applications": jobrecommend_ui,
    "Market Trend Analysis": markettrend_ui,
    "Skill Gap Identification": skillgap_ui,
    "Resume Parsing": airesume_ui,
    "Career Advice Chatbot": chatbot_ui,
}

# Function selection and display
selection = st.sidebar.radio("Choose a Functionality", list(options.keys()))
options[selection]()  # Call the selected functionality's UI function

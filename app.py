import streamlit as st
from utils.jobrecommend import jobrecommend_ui
from utils.markettrend import markettrend_ui
from utils.skillgap import skillgap_ui
from utils.airesume import airesume_ui
from utils.chatbot import chatbot_ui

# App Title
st.title("HireScope")

# Display a small image with a set width
st.image("hirescope.png", width=150)  # Adjust width as needed
<div style="text-align: right;">
    <img src="hirescope.png" width="150">
</div>
 
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

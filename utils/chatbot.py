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
    
    "What are some common interview questions?",
    "Common interview questions include 'Tell me about yourself,' 'What are your strengths and weaknesses?' and 'Where do you see yourself in 5 years?'",
    
    "How do I network effectively?",
    "To network effectively, attend industry events, engage on LinkedIn, and reach out to professionals in your field.",
    
    "What skills are most in-demand for software engineers?",
    "In-demand skills for software engineers include programming languages like Python, JavaScript, and knowledge of cloud computing, machine learning, and data science.",
    
    "How do I prepare for a career change?",
    "To prepare for a career change, research the new field, develop relevant skills, and consider taking online courses or certifications.",
    
    "What should I include in a cover letter?",
    "In a cover letter, highlight your relevant experience, show enthusiasm for the role, and explain why you're a good fit for the company.",
    
    "How do I follow up after a job interview?",
    "Send a thank-you email within 24 hours, expressing appreciation for the opportunity and briefly reiterating your interest in the position.",
    
    "What are soft skills, and why are they important?",
    "Soft skills are interpersonal skills, like communication, teamwork, and problem-solving. They’re essential for working well with others and succeeding in a professional environment.",
    
    "How can I negotiate a higher salary?",
    "Research industry standards, highlight your achievements, and express your value confidently when discussing salary with a potential employer.",
    
    "What are the top skills for project managers?",
    "Key skills for project managers include time management, leadership, budgeting, risk management, and knowledge of project management tools.",
    
    "How can I prepare for a technical interview?",
    "Practice coding problems, review fundamental algorithms, understand system design basics, and familiarize yourself with common interview platforms like LeetCode or HackerRank.",
    
    "What are the best ways to find job openings?",
    "Look on job boards, company websites, LinkedIn, and network with people in your field to find job openings.",
    
    "How can I stand out in a competitive job market?",
    "To stand out, tailor your resume for each application, build a strong online presence, and continuously update your skills to match industry demands.",
    
    "What should I wear to a job interview?",
    "Dress in business professional or business casual attire, depending on the company culture, and ensure your outfit is neat and appropriate.",
    
    "How do I write a thank-you email after an interview?",
    "Express gratitude, highlight something specific from the interview, and reiterate your interest in the position in a concise thank-you email.",
    
    "What are some tips for managing work-life balance?",
    "Set boundaries, prioritize tasks, take regular breaks, and avoid overcommitting to maintain a healthy work-life balance.",
    
    "How can I develop my leadership skills?",
    "Take on more responsibility, seek feedback, observe effective leaders, and pursue training or mentorship opportunities.",
    
    "What should I do if I'm feeling stuck in my career?",
    "Reflect on your goals, consider upskilling, speak with mentors, and explore lateral or upward career moves to find new opportunities.",
    
    "How can I improve my public speaking skills?",
    "Practice regularly, join public speaking groups, record yourself to assess your delivery, and focus on clear communication.",
    
    "What’s the best way to learn new skills on a budget?",
    "Take advantage of free online resources like Coursera, edX, YouTube tutorials, and library resources to learn new skills affordably.",
    
    "How do I handle gaps in my employment history?",
    "Be honest, focus on the skills you developed during gaps, and emphasize what you've done to stay relevant or upskill during that time.",
    
    "What are transferable skills, and why are they important?",
    "Transferable skills are abilities you can apply across different roles, like communication, problem-solving, and adaptability. They help you transition to new roles.",
    
    "How can I make a good first impression at a new job?",
    "Be punctual, show eagerness to learn, listen actively, and build relationships with colleagues to make a positive first impression.",
    
    "What should I do if I'm overwhelmed by my workload?",
    "Prioritize tasks, ask for help when needed, and break down large projects into smaller, manageable steps to handle your workload more effectively.",
    
    "How can I showcase my achievements on LinkedIn?",
    "Use LinkedIn’s featured section, add specific examples in your experience section, and request recommendations to showcase achievements."
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

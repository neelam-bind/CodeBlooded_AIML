import pandas as pd
import fitz  # PyMuPDF for PDF text extraction
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import streamlit as st

# Download necessary NLTK resources
nltk.download('stopwords')
nltk.download('punkt_tab')
nltk.download('wordnet')

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def clean_text(text):
    """Cleans and preprocesses text data."""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text, re.I)
    text = re.sub(r'\s+', ' ', text)
    tokens = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(tokens)

def extract_skills_from_text(text):
    """Extracts a predefined list of skills from the text."""
    skills_list = [
        'python', 'java', 'c++', 'javascript', 'sql', 'machine learning',
        'deep learning', 'tensorflow', 'keras', 'data analysis', 'statistics',
        'communication', 'leadership', 'project management', 'html', 'css',
        'docker', 'kubernetes', 'aws', 'azure', 'git', 'linux'
    ]
    return [skill for skill in skills_list if skill in text]

# Load job descriptions and preprocess
df = pd.read_csv('data/data.csv')
df['cleaned_job_desc'] = df['Job Description'].apply(clean_text)
df['skills_needed'] = df['cleaned_job_desc'].apply(extract_skills_from_text)

def recommend_jobs_from_resume(resume_pdf_path, top_n=3):
    """Recommends jobs based on skills found in the user's resume."""
    resume_text = extract_text_from_pdf(resume_pdf_path)
    cleaned_resume_text = clean_text(resume_text)
    user_skills = extract_skills_from_text(cleaned_resume_text)

    recommendations = []
    for idx, row in df.iterrows():
        job_position = row['position']
        skills_needed = row['skills_needed']
        skill_gaps = list(set(skills_needed) - set(user_skills))
        if skill_gaps:
            learning_resources = suggest_learning_resources(skill_gaps)
            recommendations.append((job_position, skill_gaps, learning_resources))
    return recommendations

def suggest_learning_resources(skill_gaps):
    """Suggests learning resources for the given skill gaps."""
    resources = {
        'python': [
            {'name': 'Python for Data Science (Coursera)', 'url': 'https://www.coursera.org/specializations/python-data-science'},
            {'name': 'Python Crash Course (Book)', 'url': 'https://nostarch.com/pythoncrashcourse2e'}
        ],
        'java': [
            {'name': 'Java Programming (Udemy)', 'url': 'https://www.udemy.com/course/java-programming-complete-beginner-to-advanced/'},
            {'name': 'Effective Java (Book)', 'url': 'https://www.pearson.com/store/p/effective-java/P100000535370'}
        ],
        'machine learning': [
            {'name': 'Machine Learning by Andrew Ng (Coursera)', 'url': 'https://www.coursera.org/learn/machine-learning'},
            {'name': 'Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow (Book)', 'url': 'https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/'}
        ],
        'deep learning': [
            {'name': 'Deep Learning Specialization (Coursera)', 'url': 'https://www.coursera.org/specializations/deep-learning'},
            {'name': 'Deep Learning (Book)', 'url': 'https://www.deeplearningbook.org/'}
        ],
        'tensorflow': [
            {'name': 'TensorFlow for Beginners (Udemy)', 'url': 'https://www.udemy.com/course/learn-tensorflow/'},
            {'name': 'Hands-On Machine Learning with TensorFlow (Book)', 'url': 'https://www.oreilly.com/library/view/hands-on-machine-learning/9781491978499/'}
        ],
        'aws': [
            {'name': 'AWS Certified Solutions Architect - Associate (Udemy)', 'url': 'https://www.udemy.com/course/aws-certified-solutions-architect-associate/'},
            {'name': 'AWS Certified Solutions Architect – Official Study Guide (Book)', 'url': 'https://www.amazon.com/AWS-Certified-Solutions-Architect-Associate/dp/1119504212'}
        ],
        'sql': [
            {'name': 'SQL for Data Science (Coursera)', 'url': 'https://www.coursera.org/learn/sql-for-data-science'},
            {'name': 'Learning SQL (Book)', 'url': 'https://www.oreilly.com/library/view/learning-sql/9781449319267/'}
        ],
        'docker': [
            {'name': 'Docker for Beginners (Udemy)', 'url': 'https://www.udemy.com/course/docker-tutorial-for-beginners/'},
            {'name': 'Docker Deep Dive (Book)', 'url': 'https://www.amazon.com/Docker-Deep-Dive-Nigel-Poulton/dp/1521822807'}
        ],
        # Add more skills and resources here
        'communication': [
            {'name': 'Communication Skills for Professionals (Coursera)', 'url': 'https://www.coursera.org/learn/wharton-communication-skills'},
            {'name': 'How to Win Friends and Influence People (Book)', 'url': 'https://www.amazon.com/How-Win-Friends-Influence-People/dp/0671027034'}
        ],
        'leadership': [
            {'name': 'Leadership Skills for Beginners (Udemy)', 'url': 'https://www.udemy.com/course/leadership-skills-for-beginners/'},
            {'name': 'Leaders Eat Last (Book)', 'url': 'https://www.amazon.com/Leaders-Eat-Last-Together-Business/dp/1591848016'}
        ],
        'project management': [
            {'name': 'Project Management for Beginners (Udemy)', 'url': 'https://www.udemy.com/course/project-management-for-beginners/'},
            {'name': 'Project Management: A Systems Approach to Planning, Scheduling, and Controlling (Book)', 'url': 'https://www.amazon.com/Project-Management-Systems-Planning-Scheduling/dp/1119165350'}
        ]
    }
    suggestions = {}
    for skill in skill_gaps:
        suggestions[skill] = resources.get(skill, [{'name': 'No resources available', 'url': ''}])
    return suggestions

# UI function for Streamlit
def skillgap_ui():
    st.title("Skill Gap Identification Tool")

    # File uploader for resume
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
    
    if uploaded_file is not None:
        # Extract and clean resume text
        with open("temp_resume.pdf", "wb") as f:
            f.write(uploaded_file.read())
        
        st.write("Analyzing your resume for skill gaps...")

        # Generate job recommendations and skill gap analysis
        recommendations = recommend_jobs_from_resume("temp_resume.pdf")
        
        if recommendations:
            st.write("Skill gap analysis and recommended learning resources:")
            for job, gaps, resources in recommendations:
                st.subheader(f"Job Position: {job}")
                st.write("Skill Gaps:", ', '.join(gaps))
                st.write("Recommended Learning Resources:")
                for skill, resource_list in resources.items():
                    for resource in resource_list:
                        st.markdown(f"- [{resource['name']}]({resource['url']})")
        else:
            st.write("No skill gaps found. Your resume seems well-matched with the job descriptions.")
    else:
        st.write("Please upload your resume to identify skill gaps.")

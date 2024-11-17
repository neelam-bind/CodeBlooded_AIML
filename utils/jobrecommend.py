import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import fitz  # PyMuPDF for extracting text from PDFs
import re
import spacy  # For NLP-based skills extraction (optional)
from collections import defaultdict

# Load spaCy model for advanced NLP processing (optional, for skill extraction)
# nlp = spacy.load("en_core_web_sm")  # You can use a larger model if needed

# Domain-specific skills (you can expand this list based on the industry/domain)
DOMAIN_SKILLS = {
    'Software Development': ["python", "java", "javascript", "react", "node.js", "html", "css", "sql", "c++", "ruby", "machine learning"],
    'Data Science': ["python", "pandas", "numpy", "scikit-learn", "tensorflow", "data visualization", "sql", "deep learning", "r"],
    'Web Development': ["html", "css", "javascript", "react", "angular", "node.js", "django", "flask", "php"],
    'Finance': ["excel", "financial modeling", "accounting", "investing", "quantitative analysis", "stock market", "python", "data analysis"],
    'Marketing': ["seo", "content writing", "social media", "google analytics", "marketing strategy", "digital marketing", "branding"],
    'Design': ["photoshop", "illustrator", "ux/ui", "figma", "adobe xd", "wireframing", "graphic design", "prototyping"]
}

# Extract text from the uploaded PDF
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(pdf_file)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Extract skills dynamically from the resume text based on domain-specific skills
def extract_skills_from_text(text, domain):
    extracted_skills = []
    skills_list = DOMAIN_SKILLS.get(domain, [])
    
    for skill in skills_list:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            extracted_skills.append(skill)
    
    return extracted_skills

# Scrape job listings from domain-specific job boards (like Internshala, Indeed, Fresherworld)
def fetch_jobs_from_board(url, skills):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for job_card in soup.select('.job-card-class'):  # Replace with actual CSS selectors for each board
        title = job_card.select_one('.job-internship-name').text.strip()  # Adjust based on job board
        company = job_card.select_one('.company-name').text.strip()
        location = job_card.select_one('.row-1-item locations').text.strip()
        description = job_card.select_one('.About the internship').text.strip()

        jobs.append({
            'title': title,
            'company': company,
            'location': location,
            'description': description
        })
    return pd.DataFrame(jobs)

# Scrape job listings based on the domain and skills
def scrape_jobs_by_domain(skills, domain):
    job_boards = {
        'Software Development': ["https://www.indeed.com/jobs?q=software+developer", "https://internshala.com/internships"],
        'Data Science': ["https://www.indeed.com/jobs?q=data+scientist", "https://fresherworld.com/jobs"],
        'Web Development': ["https://www.indeed.com/jobs?q=web+developer", "https://internshala.com/internships"],
        'Finance': ["https://www.indeed.com/jobs?q=finance", "https://fresherworld.com/jobs"],
        'Marketing': ["https://www.indeed.com/jobs?q=marketing", "https://internshala.com/internships"],
        'Design': ["https://www.indeed.com/jobs?q=graphic+designer", "https://internshala.com/internships"]
    }

    all_jobs = pd.DataFrame()
    for board_url in job_boards.get(domain, []):
        board_jobs = fetch_jobs_from_board(board_url, skills)
        all_jobs = pd.concat([all_jobs, board_jobs], ignore_index=True)

    return all_jobs

# Streamlit UI function to interact with users and display the results
def jobrecommend_ui():
    st.title("Personalized Job Recommendations Based on Resume")

    # Select domain for job recommendations
    domain = st.selectbox("Select your preferred domain", list(DOMAIN_SKILLS.keys()))

    st.subheader("Upload Your Resume (PDF format)")

    # File uploader for resume
    resume_file = st.file_uploader("Upload your resume", type=["pdf"])
    
    if resume_file is not None:
        st.write("Resume uploaded successfully!")
        
        # Extract text from the resume
        resume_text = extract_text_from_pdf(resume_file)

        # Extract skills from the resume text based on the selected domain
        skills = extract_skills_from_text(resume_text, domain)

        if skills:
            st.write(f"Skills extracted from your resume: {', '.join(skills)}")
            st.write("Fetching job listings based on these skills...")

            # Scrape job listings based on extracted skills
            all_jobs = scrape_jobs_by_domain(skills, domain)
            if not all_jobs.empty:
                st.write("Here are the job listings based on your skills:")
                st.dataframe(all_jobs)
                
                # Option to download as CSV
                csv_data = all_jobs.to_csv(index=False)
                st.download_button(
                    label="Download job listings as CSV",
                    data=csv_data,
                    file_name="scraped_jobs.csv",
                    mime="text/csv"
                )
            else:
                st.write("No job listings found based on the extracted skills.")

        else:
            st.write("No relevant skills found in your resume. Please try uploading a different resume or select a different domain.")

    else:
        st.write("Please upload your resume for personalized job recommendations.")

if __name__ == "__main__":
    jobrecommend_ui()

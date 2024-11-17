import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import fitz  # PyMuPDF for extracting text from PDFs
import re

# Define domain-specific skills (this can be expanded as needed)
DOMAIN_SKILLS = {
    'Software Development': ["python", "java", "javascript", "react", "node.js", "html", "css", "sql", "c++", "ruby", "machine learning"],
    'Data Science': ["python", "pandas", "numpy", "scikit-learn", "tensorflow", "data visualization", "sql", "deep learning", "r"],
    'Web Development': ["html", "css", "javascript", "react", "angular", "node.js", "django", "flask", "php"],
    'Finance': ["excel", "financial modeling", "accounting", "investing", "quantitative analysis", "stock market", "python", "data analysis"],
    'Marketing': ["seo", "content writing", "social media", "google analytics", "marketing strategy", "digital marketing", "branding"],
    'Design': ["photoshop", "illustrator", "ux/ui", "figma", "adobe xd", "wireframing", "graphic design", "prototyping"]
}

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(pdf_file)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to extract skills dynamically from the resume text based on domain-specific skills
def extract_skills_from_text(text, domain):
    extracted_skills = []
    skills_list = DOMAIN_SKILLS.get(domain, [])
    
    for skill in skills_list:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            extracted_skills.append(skill)
    
    return extracted_skills

# Scrape job listings from the specified URL and return them as a DataFrame
def fetch_jobs_from_board(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for job_card in soup.select('.job-card-class'):  # Replace with actual CSS selectors for each board
        title = job_card.select_one('.job-title').text.strip()
        company = job_card.select_one('.company').text.strip()
        location = job_card.select_one('.location').text.strip()
        description = job_card.select_one('.description').text.strip()

        jobs.append({
            'title': title,
            'company': company,
            'location': location,
            'description': description
        })
    return pd.DataFrame(jobs)

# Scrape job listings based on extracted skills
def scrape_jobs_by_skills(skills):
    # URLs for job boards to scrape, customize per domain if needed
    job_boards = {
        'Software Development': [
            "https://www.indeed.com/jobs?q=software+developer",
            "https://internshala.com/internships"
        ],
        'Data Science': [
            "https://www.indeed.com/jobs?q=data+scientist",
            "https://fresherworld.com/jobs"
        ],
        'Web Development': [
            "https://www.indeed.com/jobs?q=web+developer",
            "https://internshala.com/internships"
        ],
        'Finance': [
            "https://www.indeed.com/jobs?q=finance",
            "https://fresherworld.com/jobs"
        ],
        'Marketing': [
            "https://www.indeed.com/jobs?q=marketing",
            "https://internshala.com/internships"
        ],
        'Design': [
            "https://www.indeed.com/jobs?q=graphic+designer",
            "https://internshala.com/internships"
        ]
    }

    # Choose job boards based on the skills
    domain = 'Software Development'  # You can adjust based on user selection
    all_jobs = pd.DataFrame()
    
    for board_url in job_boards.get(domain, []):
        board_jobs = fetch_jobs_from_board(board_url)
        all_jobs = pd.concat([all_jobs, board_jobs], ignore_index=True)

    return all_jobs

# Streamlit UI function to handle file upload, skill extraction, and job scraping
def jobrecommend_ui():
    st.title("Job Recommendations Based on Your Resume")

    # File uploader for resume
    resume_file = st.file_uploader("Upload your resume (PDF format)", type=["pdf"])

    if resume_file is not None:
        st.write("Resume uploaded successfully!")

        # Extract text from the resume
        resume_text = extract_text_from_pdf(resume_file)

        # Ask user for their preferred domain
        domain = st.selectbox("Select your preferred domain", list(DOMAIN_SKILLS.keys()))
        
        # Extract skills from the resume text based on the selected domain
        skills = extract_skills_from_text(resume_text, domain)

        if skills:
            st.write(f"Skills extracted from your resume: {', '.join(skills)}")
            st.write("Fetching job listings based on these skills...")

            # Scrape job listings based on extracted skills
            all_jobs = scrape_jobs_by_skills(skills)
            if not all_jobs.empty:
                st.write("Here are the job listings based on your skills:")
                st.dataframe(all_jobs)
                
                # Save the results to a CSV file and provide download link
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

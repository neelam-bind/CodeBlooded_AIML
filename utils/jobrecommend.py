import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import pdfplumber  # To extract text from PDF resumes

# Function to extract job title from the resume
def extract_job_title_from_resume(resume_file):
    with pdfplumber.open(resume_file) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text()

    # Simple extraction logic (you can improve this based on your resume structure)
    keywords = ['developer', 'engineer', 'designer', 'analyst', 'manager', 'intern']  # Example job roles
    job_title = None
    
    for keyword in keywords:
        if keyword.lower() in full_text.lower():
            job_title = keyword
            break
    
    if job_title:
        return job_title.lower().replace(" ", "-")  # Format the job title for the URL
    else:
        return None

# Function to fetch Internshala jobs for a particular role
def fetch_internshala_jobs_for_role(job_role):
    url = f"https://internshala.com/internships/{job_role}-internship"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for job_card in soup.select('.individual_internship'):
        title = job_card.select_one('.job-internship-name').text.strip()
        company = job_card.select_one('.company_name').text.strip()
        location = job_card.select_one('.ic-16-map-pin').text.strip()
        stipend = job_card.select_one('.stipend')
        salary = stipend.text.strip() if stipend else "Salary not available"
        
        jobs.append({
            'title': title,
            'company': company,
            'location': location,
            'salary': salary,
        })
    
    return pd.DataFrame(jobs)

# UI function to integrate with Streamlit
def jobrecommend_ui():
    st.title("Internshala Job Scraper Based on Resume")

    # Resume Upload Feature
    st.subheader("Upload Your Resume")
    resume_file = st.file_uploader("Upload your resume (PDF format)", type=["pdf"])
    
    if resume_file is not None:
        st.write("Resume uploaded successfully!")
        
        # Extract job role from resume
        job_role = extract_job_title_from_resume(resume_file)
        
        if job_role:
            st.write(f"Job role extracted: {job_role}")
            
            # Scrape Internshala jobs for the extracted job role
            st.write("Fetching job listings for the role... This may take a few moments.")
            jobs_df = fetch_internshala_jobs_for_role(job_role)
            
            if not jobs_df.empty:
                st.write("Job listings fetched successfully!")
                st.dataframe(jobs_df)
                
                # Option to download as CSV
                csv_data = jobs_df.to_csv(index=False)
                st.download_button(
                    label="Download job listings as CSV",
                    data=csv_data,
                    file_name=f"{job_role}_internships.csv",
                    mime="text/csv"
                )
            else:
                st.write(f"No job listings found for the role: {job_role}.")
        else:
            st.write("Job title could not be extracted from your resume. Please check the resume format.")
    else:
        st.write("Please upload your resume for personalized job recommendations.")

# Run the UI function in Streamlit
jobrecommend_ui()

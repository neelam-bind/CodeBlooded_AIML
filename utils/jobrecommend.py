import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

def fetch_internshala_jobs():
    url = "https://internshala.com/internships"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for job_card in soup.select('.individual_internship'):
        title = job_card.select_one('.job-internship-name').text.strip()
        company = job_card.select_one('.company_name').text.strip()
        location = job_card.select_one('.ic-16-map-pin').text.strip()

        jobs.append({
            'title': title,
            'company': company,
            'location': location,
        })
    return pd.DataFrame(jobs)

def scrape_internshala_jobs():
    # Scrape Internshala jobs
    internshala_jobs = fetch_internshala_jobs()
    return internshala_jobs

# UI function to integrate with Streamlit
def jobrecommend_ui():
    st.title("Internshala Job Recommendations Scraper")

    if st.button("Fetch Job Listings"):
        st.write("Scraping job data. This may take a few moments...")

        # Scrape Internshala jobs and display in Streamlit
        internshala_jobs = scrape_internshala_jobs()
        st.write("Scraping completed! Here are the latest job listings from Internshala:")
        st.dataframe(internshala_jobs)

        # Option to download as CSV
        csv_data = internshala_jobs.to_csv(index=False)
        st.download_button(
            label="Download job listings as CSV",
            data=csv_data,
            file_name="internshala_jobs.csv",
            mime="text/csv"
        )
    else:
        st.write("Click the button above to fetch job listings from Internshala.")
    
    # Resume Upload Feature
    st.subheader("Upload Your Resume")
    resume_file = st.file_uploader("Upload your resume (PDF format)", type=["pdf"])
    if resume_file is not None:
        st.write("Resume uploaded successfully!")
        # You can add more functionality here to parse and analyze the resume.
        # For example: Extracting skills or displaying basic information.
    else:
        st.write("Please upload your resume for personalized job recommendations.")

# Run the UI function in Streamlit
jobrecommend_ui()

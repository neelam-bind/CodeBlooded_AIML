import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

# Fetch job data from Internshala
def fetch_internshala_jobs():
    url = "https://internshala.com/internships"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for job_card in soup.select('.individual_internship'):
        title = job_card.select_one('.job-title-href').text.strip()
        company = job_card.select_one('.company_name').text.strip()
        location = job_card.select_one('.location').text.strip()

        jobs.append({
            'title': title,
            'company': company,
            'location': location,
        })
    return pd.DataFrame(jobs)

# Fetch job data from Indeed
def fetch_indeed_jobs():
    url = "https://www.indeed.com/jobs?q=software+engineer"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for job_card in soup.select('.jobsearch-SerpJobCard'):
        title = job_card.select_one('.title').text.strip()
        company = job_card.select_one('.company').text.strip()
        location = job_card.select_one('.location').text.strip()
        description = job_card.select_one('.summary').text.strip()

        jobs.append({
            'title': title,
            'company': company,
            'location': location,
            'description': description
        })
    return pd.DataFrame(jobs)

# Fetch job data from Fresherworld
def fetch_fresherworld_jobs():
    url = "https://www.freshersworld.com/jobs"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for job_card in soup.select('.job-list'):
        title = job_card.select_one('.job-title').text.strip()
        company = job_card.select_one('.company-name').text.strip()
        location = job_card.select_one('.location').text.strip()
        description = job_card.select_one('.description').text.strip()

        jobs.append({
            'title': title,
            'company': company,
            'location': location,
            'description': description
        })
    return pd.DataFrame(jobs)

# Combine all job data into one DataFrame
def scrape_all_jobs():
    internshala_jobs = fetch_internshala_jobs()
    indeed_jobs = fetch_indeed_jobs()
    fresherworld_jobs = fetch_fresherworld_jobs()

    all_jobs = pd.concat([internshala_jobs, indeed_jobs, fresherworld_jobs], ignore_index=True)
    return all_jobs

# Streamlit UI function
def jobrecommend_ui():
    st.title("Job Recommendations Scraper")

    if st.button("Fetch Job Listings"):
        st.write("Scraping job data. This may take a few moments...")

        # Scrape jobs and display in Streamlit
        all_jobs = scrape_all_jobs()
        st.write("Scraping completed! Here are the latest job listings:")
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
        st.write("Click the button above to fetch job listings from Internshala, Indeed, and Fresherworld.")
    
    # Resume upload feature for additional functionality
    st.subheader("Upload Your Resume")
    resume_file = st.file_uploader("Upload your resume (PDF format)", type=["pdf"])
    if resume_file is not None:
        st.write("Resume uploaded successfully!")
        # Add functionality for parsing and analyzing the resume if needed.
    else:
        st.write("Please upload your resume for personalized job recommendations.")


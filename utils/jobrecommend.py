import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import requests  # Don't forget to import requests if you are using it for other sites

# Setup Selenium WebDriver (Chrome)
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (no UI)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Fetch Fresherworld jobs
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

# Fetch Internshala jobs
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

# Combine all job sources
def scrape_all_jobs():
    internshala_jobs = fetch_internshala_jobs()
    fresherworld_jobs = fetch_fresherworld_jobs()

    all_jobs = pd.concat([internshala_jobs, fresherworld_jobs], ignore_index=True)
    return all_jobs

# Streamlit UI
def jobrecommend_ui():
    st.title("Job Recommendations Scraper")

    if st.button("Fetch Job Listings"):
        st.write("Scraping job data. This may take a few moments...")

        # Scrape all jobs and display in Streamlit
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
        st.write("Click the button above to fetch job listings from Internshala and Fresherworld.")
    
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

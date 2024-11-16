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
        title = job_card.select_one('.profile').text.strip()
        company = job_card.select_one('.company_name').text.strip()
        location = job_card.select_one('.location_link').text.strip()
        skills = job_card.select_one('.internship_other_details').text.strip()

        jobs.append({
            'title': title,
            'company': company,
            'location': location,
            'skills': skills
        })
    return pd.DataFrame(jobs)

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

def scrape_all_jobs():
    internshala_jobs = fetch_internshala_jobs()
    indeed_jobs = fetch_indeed_jobs()
    fresherworld_jobs = fetch_fresherworld_jobs()

    all_jobs = pd.concat([internshala_jobs, indeed_jobs, fresherworld_jobs], ignore_index=True)
    return all_jobs

# UI function to integrate with Streamlit
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
        st.write("Click the button above to fetch job listings from Internshala, Indeed, and Fresherworld.")


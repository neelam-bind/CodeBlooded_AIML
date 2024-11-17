import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from collections import Counter
import nltk
from nltk.corpus import stopwords

# Download necessary NLTK resources if not already present
nltk.download('stopwords')

# Load and clean data
df = pd.read_csv('data/data.csv')
df_cleaned = df.drop(columns=['Unnamed: 0'], axis=1)  # Remove the 'Unnamed: 0' column if it exists
df_cleaned.fillna('N/A', inplace=True)  # Fill missing values with 'N/A'

# Function to visualize job roles
def plot_job_roles():
    role_counts = df_cleaned['position'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=role_counts.index, y=role_counts.values, palette='Blues_d', ax=ax)
    ax.set_title('Top 10 Job Roles', fontsize=16)
    ax.set_xlabel('Job Role', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    plt.xticks(rotation=45)
    ax.set_xticklabels(role_counts.index, rotation=45, ha='right')
    st.pyplot(fig)

# Function to visualize industries
def plot_industries():
    industry_counts = df_cleaned['industry'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=industry_counts.index, y=industry_counts.values, palette='Greens_d', ax=ax)
    ax.set_title('Top 10 Industries', fontsize=16)
    ax.set_xlabel('Industry', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Function to visualize locations
def plot_locations():
    df_cleaned[['location_city', 'location_state']] = df_cleaned['location'].str.split(',', n=1, expand=True)
    location_counts = df_cleaned['location_city'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=location_counts.index, y=location_counts.values, palette='Oranges_d', ax=ax)
    ax.set_title('Top 10 Locations (Cities)', fontsize=16)
    ax.set_xlabel('City', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Function to visualize the most common words in job descriptions
def plot_common_words():
    stop_words = set(stopwords.words('english'))
    all_descriptions = ' '.join(df_cleaned['Job Description'].astype(str).values)
    words = [word.lower() for word in all_descriptions.split() if word.lower() not in stop_words]
    word_counts = Counter(words)
    common_words = word_counts.most_common(20)
    common_words = dict(common_words)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=list(common_words.keys()), y=list(common_words.values()), palette='Purples_d', ax=ax)
    ax.set_title('Top 20 Most Common Words in Job Descriptions', fontsize=16)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Main UI function for Streamlit
def markettrend_ui():
    st.title("Market Trend Analysis")
    st.write("Explore market trends by job role, industry, location, and common words in job descriptions.")
    
    # Display each plot with a header
    if st.checkbox("Show Top 10 Job Roles"):
        plot_job_roles()
    if st.checkbox("Show Top 10 Industries"):
        plot_industries()
    if st.checkbox("Show Top 10 Locations (Cities)"):
        plot_locations()
    if st.checkbox("Show Top 20 Most Common Words in Job Descriptions"):
        plot_common_words()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import nltk
from nltk.corpus import stopwords

# Step 1: Load the CSV file
df = pd.read_csv('data/data.csv')

# Step 2: Clean up the dataset by removing unnecessary columns and filling missing values
df_cleaned = df.drop(columns=['Unnamed: 0'], axis=1)  # Remove the 'Unnamed: 0' column if it exists
df_cleaned.fillna('N/A', inplace=True)  # Fill missing values with 'N/A'

# Step 3: Visualizing job roles (positions)
def plot_job_roles():
    # Top 10 most common job roles
    role_counts = df_cleaned['position'].value_counts().head(10)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=role_counts.index, y=role_counts.values, palette='Blues_d')
    plt.title('Top 10 Job Roles', fontsize=16)
    plt.xlabel('Job Role', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Step 4: Visualizing industries
def plot_industries():
    # Top 10 most common industries
    industry_counts = df_cleaned['industry'].value_counts().head(10)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=industry_counts.index, y=industry_counts.values, palette='Greens_d')
    plt.title('Top 10 Industries', fontsize=16)
    plt.xlabel('Industry', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Step 5: Visualizing locations (cities)
def plot_locations():
    # Extract location city and state from the 'location' column
    df_cleaned[['location_city', 'location_state']] = df_cleaned['location'].str.split(',', n=1, expand=True)
    location_counts = df_cleaned['location_city'].value_counts().head(10)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=location_counts.index, y=location_counts.values, palette='Oranges_d')
    plt.title('Top 10 Locations (Cities)', fontsize=16)
    plt.xlabel('City', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Step 6: Visualizing the most common words in job descriptions
def plot_common_words():
    # Tokenize and remove stopwords from job descriptions
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    
    # Combine all job descriptions into one large string
    all_descriptions = ' '.join(df_cleaned['Job Description'].astype(str).values)
    
    # Tokenize the descriptions and remove stopwords
    words = [word.lower() for word in all_descriptions.split() if word.lower() not in stop_words]
    
    # Count the most common words
    word_counts = Counter(words)
    common_words = word_counts.most_common(20)
    
    # Plot the most common words in job descriptions
    common_words = dict(common_words)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(common_words.keys()), y=list(common_words.values()), palette='Purples_d')
    plt.title('Top 20 Most Common Words in Job Descriptions', fontsize=16)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Step 7: Run all plots
def plot_market_trends():
    plot_job_roles()
    plot_industries()
    plot_locations()
    plot_common_words()

# Example usage
if __name__ == "__main__":
    plot_market_trends()

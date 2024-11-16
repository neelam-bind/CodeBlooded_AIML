# app.py (rewritten to exclude spacy)
from flask import Flask, render_template, request, redirect, url_for
import re

app = Flask(__name__)

# Function to perform basic NLP tasks (replacing spacy)
def simple_text_analysis(text):
    # Split text into sentences
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    # Tokenize text into words
    words = re.findall(r'\b\w+\b', text)
    word_count = len(words)
    unique_words = set(words)

    return {
        'sentences': sentences,
        'word_count': word_count,
        'unique_word_count': len(unique_words)
    }

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/upload', methods=['GET', 'POST'])
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Your file handling and processing logic
        pass
    return render_template('upload.html')


def analyze():
    if request.method == 'POST':
        text = request.form['text']
        analysis = simple_text_analysis(text)

        return render_template(
            'result.html',
            sentences=analysis['sentences'],
            word_count=analysis['word_count'],
            unique_word_count=analysis['unique_word_count']
        )

if __name__ == '__main__':
    app.run(debug=True)

import os
import sys
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from custom_exception import CustomException  # Custom error handling class
import PyPDF2  # Ensure PyPDF2 is installed for PDF text extraction

class Preprocessing:
    def extract_resume_text(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ''
                for page in reader.pages:
                    text += page.extract_text() or ''
                return text.strip()
        except Exception as e:
            raise CustomException(f"Error extracting text from {file_path}: {e}", sys)

    def preprocess_text(self, text):
        # Implement basic preprocessing such as lowercasing and tokenization
        return text.lower().split()

    def pos_filter(self, tokens):
        # Simulate POS filtering (can be adjusted for real NLP tasks)
        return ' '.join(tokens)

class PreprocessPipeline:
    def __init__(self):
        self.preprocessor = Preprocessing()

    def run(self, resume_path):
        try:
            Text = self.preprocessor.extract_resume_text(resume_path)
            Tokens = self.preprocessor.preprocess_text(Text)
            Model_input = self.preprocessor.pos_filter(Tokens)
            return Model_input
        except Exception as e:
            raise CustomException(e, sys)

class ModelPipeline:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("./models/")
        self.model = AutoModelForSequenceClassification.from_pretrained("./models/")
        self.labels = {
            0: 'Advocate', 1: 'Arts', 2: 'Automation Testing', 3: 'Blockchain', 4: 'Business Analyst',
            5: 'Civil Engineer', 6: 'Data Science', 7: 'Database', 8: 'DevOps Engineer', 9: 'DotNet Developer',
            10: 'ETL Developer', 11: 'Electrical Engineering', 12: 'HR', 13: 'Hadoop', 14: 'Health and fitness',
            15: 'Java Developer', 16: 'Mechanical Engineer', 17: 'Network Security Engineer', 18: 'Operations Manager',
            19: 'PMO', 20: 'Python Developer', 21: 'SAP Developer', 22: 'Sales', 23: 'Testing', 24: 'Web Designing'
        }

    def predictrole(self, Model_input):
        try:
            tokens = self.tokenizer.encode_plus(Model_input, max_length=512, truncation=True, padding="max_length", return_tensors="pt")
            outputs = self.model(**tokens)
            predicted_label = outputs.logits.argmax().item()
            return self.labels[predicted_label]
        except Exception as e:
            raise CustomException(e, sys)

class ScorePipeline:
    def __init__(self):
        pass

    def scoreprocess(self, resume_path, job_description_path):
        try:
            preprocessor = Preprocessing()
            Resume_Text = preprocessor.extract_resume_text(resume_path)
            Job_description_Text = preprocessor.extract_resume_text(job_description_path)
            return [Resume_Text, Job_description_Text]
        except Exception as e:
            raise CustomException(e, sys)

    def predictscore(self, Score_Model_input):
        try:
            # Basic similarity scoring (replace with actual model if needed)
            resume_text, job_text = Score_Model_input
            common_words = set(resume_text.lower().split()) & set(job_text.lower().split())
            score = len(common_words) / len(set(job_text.lower().split())) * 100
            return f"Match Score: {score:.2f}%"
        except Exception as e:
            raise CustomException(e, sys)

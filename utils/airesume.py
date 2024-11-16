import re
import fitz  # PyMuPDF for PDF text extraction
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import openai 

# OpenAI API key (replace with your own API key)
openai.api_key = 'YOUR_OPENAI_API_KEY'  # Replace with your OpenAI API key

# Step 1: Extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

# Step 2: Extract and Enhance Content from Poorly Defined Resume
def extract_and_improve_content(poor_resume_text):
    sections = {}
    lines = poor_resume_text.split('\n')
    sections["name"] = lines[0].strip()
    sections["email"] = re.search(r'(\S+@\S+)', poor_resume_text).group(0) if re.search(r'(\S+@\S+)', poor_resume_text) else "N/A"
    sections["phone"] = re.search(r'(\+\d{1,3}[- ]?)?\d{10}', poor_resume_text).group(0) if re.search(r'(\+\d{1,3}[- ]?)?\d{10}', poor_resume_text) else "N/A"
    sections["linkedin"] = re.search(r'linkedin\.com/\S+', poor_resume_text).group(0) if "linkedin.com" in poor_resume_text else "N/A"
    sections["objective"] = lines[1] if len(lines) > 1 else "Career-oriented individual seeking new opportunities."
    sections["skills"] = extract_skills(poor_resume_text)
    sections["experience"] = extract_experience(poor_resume_text)
    sections["education"] = extract_education(poor_resume_text)
    return sections

# Step 3: Use OpenAI API to suggest improvements
def ai_suggest_improvements(section_name, content):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Improve the {section_name} section of a resume:\n\n{content}",
            max_tokens=100
        )
        return response['choices'][0]['text'].strip()
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return content

# Step 4: Extract Skills
def extract_skills(poor_resume_text):
    skills_keywords = ["Python", "Java", "SQL", "Machine Learning", "AI", "Data Science"]
    skills = [skill for skill in skills_keywords if skill.lower() in poor_resume_text.lower()]
    return ', '.join(skills) if skills else "N/A"

# Step 5: Extract Experience
def extract_experience(poor_resume_text):
    experience = re.search(r'Experience[:\n]*(.*?)(?=\nEducation|$)', poor_resume_text, re.DOTALL)
    return experience.group(1).strip() if experience else "N/A"

# Step 6: Extract Education
def extract_education(poor_resume_text):
    education = re.search(r'Education[:\n]*(.*?)(?=\nProjects|$)', poor_resume_text, re.DOTALL)
    return education.group(1).strip() if education else "N/A"

# Step 7: Generate Enhanced Resume PDF
def save_resume_to_pdf(data):
    filename = f"Enhanced_Resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf = canvas.Canvas(filename, pagesize=letter)
    pdf.setTitle("Enhanced Resume")

    # Styling options
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(72, 750, f"Resume of {data['name']}")

    pdf.setFont("Helvetica", 12)
    y_position = 720
    section_titles = [
        ("Contact Information:", f"Email: {data.get('email', 'N/A')}\nPhone: {data.get('phone', 'N/A')}\nLinkedIn: {data.get('linkedin', 'N/A')}"),
        ("Objective:", data.get('objective', 'Career-oriented individual seeking new opportunities.')),
        ("Skills:", data.get('skills', 'N/A')),
        ("Experience:", data.get('experience', 'N/A')),
        ("Education:", data.get('education', 'N/A')),
        ("References:", "Available upon request")
    ]

    for title, content in section_titles:
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(72, y_position, title)
        pdf.setFont("Helvetica", 10)
        y_position -= 20

        for line in content.split("\n"):
            pdf.drawString(72, y_position, line)
            y_position -= 15
            if y_position < 40:  # Add a new page if reaching bottom
                pdf.showPage()
                y_position = 750

    pdf.save()
    print(f"Enhanced resume saved as {filename}")

# Main function to run the process
def main():
    # Update the path to your input resume PDF
    poor_resume_pdf_path = "/content/CEC-Poor-vs-Good-Resume.pdf"  
    poor_resume_text = extract_text_from_pdf(poor_resume_pdf_path)

    # Step 1: Extract and improve content
    extracted_data = extract_and_improve_content(poor_resume_text)

    # Step 2: Enhance each section using OpenAI API
    for section in extracted_data:
        extracted_data[section] = ai_suggest_improvements(section, extracted_data[section])

    # Step 3: Save the enhanced content to a new PDF
    save_resume_to_pdf(extracted_data)

if __name__ == "__main__":
    main()

import re

def check_sections(text):
    sections = {
        "education": bool(re.search(r"education|eğitim", text, re.I)),
        "experience": bool(re.search(r"experience|deneyim|iş deneyimi", text, re.I)),
        "skills": bool(re.search(r"skills|yetenekler|beceriler", text, re.I)),
        "projects": bool(re.search(r"projects|projeler", text, re.I)),
        "languages": bool(re.search(r"languages|language|diller", text, re.I))
    }
    return sections

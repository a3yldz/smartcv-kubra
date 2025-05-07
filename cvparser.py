import fitz  
import re

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def split_sections(text):
    section_titles = [
        "SUMMARY",
        "WORK EXPERIENCE",
        "EDUCATION",
        "GITHUB AND PROJECTS",
        "LANGUAGE",
        "SKILLS",
        "CERTIFICATIONS",
        "ADDITIONAL INFORMATION"
    ]

    pattern = "|".join([re.escape(title) for title in section_titles])
    regex = rf"(?P<header>{pattern})\s*\n"

    matches = list(re.finditer(regex, text, re.IGNORECASE))
    sections = {}

    for i in range(len(matches)):
        start = matches[i].end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        header = matches[i].group("header").strip().title() 
        content = text[start:end].strip()
        sections[header] = content

    return sections

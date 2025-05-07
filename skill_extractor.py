import re

def extract_skills(text):
    tech_keywords = [
        "python", "java", "c", "c++", "c#", "go", "r", "typescript", "javascript", "html", "css",
        "react", "vue", "angular", "next.js", "tailwind", "bootstrap", "django", "flask",
        "spring", "spring boot", "express", "mysql", "postgresql", "sqlite", "mongodb",
        "firebase", "git", "github", "docker", "ci/cd", "azure", "aws", "gcp", "linux",
        "jira", "postman", "pandas", "numpy", "tensorflow", "keras", "scikit-learn", "matplotlib"
    ]

    soft_keywords = [
        "teamwork", "communication", "problem solving", "leadership", "adaptability",
        "time management", "creativity", "collaboration", "critical thinking"
    ]

    tech_skills = []
    soft_skills = []

    clean_text = re.sub(r"[^\w\s\.\-\+#]", " ", text.lower())

    for skill in tech_keywords:
        pattern = rf"(?<![\w\+\.#]){re.escape(skill)}(?![\w\+\.#])"
        if re.search(pattern, clean_text):
            tech_skills.append(skill)

    for skill in soft_keywords:
        pattern = rf"(?<![\w\+\.#]){re.escape(skill)}(?![\w\+\.#])"
        if re.search(pattern, clean_text):
            soft_skills.append(skill)

    return tech_skills, soft_skills

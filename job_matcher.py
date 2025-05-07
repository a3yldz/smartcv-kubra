job_skill_map = {
    "backend developer": [
        "python", "java", "c#", "c++", "go", "node.js", "django", "spring", "spring boot", "flask", "express",
        "sql", "postgresql", "mysql", "mongodb", "redis", "rest api", "graphql", "docker", "git", "linux", "nginx"
    ],
    "frontend developer": [
        "html", "css", "javascript", "typescript", "react", "vue", "angular", "next.js", "tailwind", "bootstrap",
        "sass", "scss", "webpack", "vite", "figma", "responsive design", "ui/ux", "redux"
    ],
    "data scientist": [
        "python", "r", "pandas", "numpy", "matplotlib", "seaborn", "scikit-learn", "tensorflow", "keras", "pytorch",
        "sql", "ml", "machine learning", "statistics", "jupyter", "notebooks", "deep learning", "data visualization",
        "big data", "hadoop", "spark"
    ],
    "mobile developer": [
        "kotlin", "java", "swift", "flutter", "dart", "react native", "android", "ios", "firebase",
        "xcode", "android studio", "ui/ux", "rest api", "graphql", "git"
    ],
    "devops engineer": [
        "linux", "bash", "shell scripting", "docker", "kubernetes", "helm", "terraform", "ansible",
        "aws", "azure", "gcp", "ci/cd", "jenkins", "github actions", "gitlab", "monitoring", "prometheus", "grafana",
        "nginx", "load balancing", "infrastructure as code"
    ]
}


def match_score(user_skills, target_role):
    target_role = target_role.lower().strip()
    matched_role = None
    for role_name in job_skill_map.keys():
        if target_role in role_name:
            matched_role = role_name
            break

    if matched_role is None:
        return None, [], []

    expected_skills = job_skill_map[matched_role]
    matched = [skill for skill in expected_skills if skill in user_skills]
    missing = [skill for skill in expected_skills if skill not in user_skills]
    score = round(len(matched) / len(expected_skills) * 100)

    return score, matched, missing

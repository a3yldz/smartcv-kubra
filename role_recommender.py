role_skill_map = {
    "backend developer": [
        "python", "java", "c#", "node.js", "sql", "rest api", "graphql", "django", "spring", "spring boot",
        "express", "fastapi", "flask", "asp.net", "git", "linux", "docker", "postgresql", "mysql", "mongodb"
    ],
    "frontend developer": [
        "html", "css", "javascript", "typescript", "react", "vue", "angular", "next.js", "tailwind", "bootstrap",
        "sass", "scss", "figma", "responsive design", "ui/ux", "webpack", "vite"
    ],
    "data scientist": [
        "python", "r", "pandas", "numpy", "scikit-learn", "tensorflow", "keras", "pytorch", "matplotlib", "seaborn",
        "sql", "statistics", "jupyter", "notebooks", "data visualization", "machine learning", "deep learning"
    ],
    "mobile developer": [
        "kotlin", "swift", "flutter", "dart", "react native", "android", "ios", "firebase", "jetpack compose", "xcode",
        "android studio"
    ],
    "devops engineer": [
        "linux", "bash", "shell scripting", "docker", "kubernetes", "helm", "terraform", "ansible", "aws", "azure",
        "gcp", "ci/cd", "jenkins", "gitlab", "github actions", "prometheus", "grafana", "monitoring", "nginx"
    ],
    "fullstack developer": [
        "javascript", "typescript", "python", "java", "node.js", "react", "vue", "html", "css", "express",
        "django", "flask", "spring boot", "sql", "mongodb", "firebase", "graphql", "git", "docker"
    ],
    "ml engineer": [
        "python", "pandas", "numpy", "scikit-learn", "tensorflow", "keras", "pytorch", "airflow", "mlflow",
        "aws sagemaker", "docker", "data preprocessing", "model deployment"
    ]
}



def recommend_roles(user_skills):
    scores = {}
    for role, skills in role_skill_map.items():
        matched = [s for s in skills if s in user_skills]
        score = round(len(matched) / len(skills) * 100)
        scores[role] = score
    sorted_roles = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_roles 

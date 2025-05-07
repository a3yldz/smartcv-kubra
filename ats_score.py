import re

def calculate_ats_score(tech_skills, soft_skills, sections, target_role, job_skill_map, raw_text=""):
    score = 100
    deduction_log = []

    # === 1. CV Bölüm Eksiklikleri ===
    missing_sections = [k for k, v in sections.items() if not v]
    score -= len(missing_sections) * 10
    for s in missing_sections:
        deduction_log.append(f"CV bölüm eksik: {s}")

    # === 2. Teknik Skill Eksiklikleri ===
    role_skills = job_skill_map.get(target_role.lower(), [])
    matched = [skill for skill in tech_skills if skill in role_skills]
    missing = [skill for skill in role_skills if skill not in tech_skills]
    score -= len(missing) * 5
    for m in missing:
        deduction_log.append(f"Eksik teknik yetenek: {m}")

    # === 3. Soft Skill Değerlendirmesi ===
    if len(soft_skills) == 0:
        score -= 15
        deduction_log.append("Soft skill bulunamadı")
    elif len(soft_skills) < 3:
        score -= 7
        deduction_log.append("Soft skill sayısı yetersiz")

    # === 4. Deneyim Sayısı / Varlığı Tespiti ===
    date_matches = re.findall(r"\b(january|february|march|april|may|june|july|august|september|october|november|december)\s\d{4}\b", raw_text)
    keyword_matches = re.search(r"\b(work experience|experience|deneyim|iş deneyimi|tecrübe)\b", raw_text, re.IGNORECASE)

    if len(date_matches) == 0 and not keyword_matches:
        score -= 10
        deduction_log.append("Deneyim bilgisi bulunamadı")
    elif len(date_matches) < 2:
        score -= 5
        deduction_log.append("Deneyim sayısı düşük")

    score = max(0, min(100, score))
    return score, deduction_log

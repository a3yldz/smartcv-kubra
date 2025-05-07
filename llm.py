import google.generativeai as genai

def get_ai_advice(tech_skills, soft_skills, api_key: str):
    if not api_key:
        return "❗ Gemini API Key eksik."

    genai.configure(api_key=api_key)

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"""
        CV'de tespit edilen yetenekler: {', '.join(tech_skills + soft_skills)}.
        Yazılım kariyerinde bu kişi kendini nasıl geliştirmeli? 2-3 öneri ver.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Yapay zeka önerisi alınamadı: {e}"

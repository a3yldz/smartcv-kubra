def generate_suggestions(sections):
    suggestions = []
    if not sections["projects"]:
        suggestions.append("Projeler kısmı eksik, yazılım rollerinde önemli bir başlık.")
    if not sections["skills"]:
        suggestions.append("Teknik beceriler kısmı eksik olabilir, diller ve araçlar belirtilmeli.")
    if not sections["languages"]:
        suggestions.append("Dil bilgisi kısmı eklenmeli, özellikle İngilizce seviyesi önemli.")
    return suggestions

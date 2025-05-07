from xhtml2pdf import pisa
import os

FONT_PATH = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")

def create_cv_report(tech_skills, soft_skills, score, matched, missing, recommended_roles, suggestions):
    html = f"""
    <html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <style>
            @page {{ size: A4; margin: 2cm; }}
            @font-face {{
                font-family: "DejaVuSans";
                src: url("file://{FONT_PATH}");
            }}
            body {{ font-family: "DejaVuSans"; color: #333; font-size: 12pt; }}
            h1 {{ color: #2C5EFF; text-align: center; margin-bottom: 20px; }}
            h2 {{ color: #222; border-bottom: 1px solid #ccc; padding-bottom: 4px; margin-top: 20px; font-size: 14pt; }}
            ul {{ line-height: 1.4; padding-left: 20px; margin-top: 5px; }}
            p {{ margin: 5px 0; }}
            .section {{ margin-bottom: 15px; }}
            .title {{ font-weight: bold; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <h1>SmartCV Raporu</h1>

        <div class="section">
            <h2>Pozisyon Uyum Skoru</h2>
            <p><span class="title">Skor:</span> %{score}</p>
            <p><span class="title">Eşleşen Yetenekler:</span> {', '.join(matched)}</p>
            <p><span class="title">Eksik Yetenekler:</span></p>
            <ul>
                {''.join([f'<li>{m}</li>' for m in missing]) if missing else '<li>Yok</li>'}
            </ul>
        </div>

        <div class="section">
            <h2>Teknik Yetenekler</h2>
            <p>{', '.join(tech_skills) if tech_skills else 'Tespit edilemedi.'}</p>
        </div>

        <div class="section">
            <h2>Soft Skills</h2>
            <p>{', '.join(soft_skills) if soft_skills else 'Tespit edilemedi.'}</p>
        </div>

        <div class="section">
            <h2>Önerilen Yazılım Rolleri</h2>
            <ul>
                {''.join([f'<li>{role.title()} → %{role_score}</li>' for role, role_score in recommended_roles])}
            </ul>
        </div>

        <div class="section">
            <h2>CV İyileştirme Önerileri</h2>
            <ul>
                {''.join([f'<li>{s}</li>' for s in suggestions]) if suggestions else '<li>Başlıklar eksiksiz. Harika iş!</li>'}
            </ul>
        </div>

    </body>
    </html>
    """

    output_path = "cv_analysis_report.pdf"
    try:
        with open(output_path, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(html.encode("utf-8"), dest=pdf_file, encoding="utf-8")
        if pisa_status.err:
            return None
        return output_path
    except Exception:
        return None
import streamlit as st
st.set_page_config(
    page_title="SmartCV - Kübra",
    page_icon="assets/favicon.png",
    layout="wide"
)

import base64
import plotly.express as px
from dotenv import load_dotenv
import os
import re
import plotly.graph_objects as go

from style import inject_global_styles, render_header, render_footer
from cvparser import extract_text_from_pdf
from analyzer import check_sections
from recommender import generate_suggestions
from skill_extractor import extract_skills
from job_matcher import match_score
from role_recommender import recommend_roles
from llm import get_ai_advice
from ats_score import calculate_ats_score
from job_matcher import job_skill_map

# PDF oluşturma tamamen kaldırıldı
# from generate_pdf import create_cv_report  ← SİLİNDİ

# Ortam değişkenlerini yükle
load_dotenv(dotenv_path=".env", override=True)

# === UI Header ===
st.markdown(inject_global_styles(), unsafe_allow_html=True)
st.markdown(render_header(), unsafe_allow_html=True)

# ATS nedir açıklaması
with st.expander("ATS Nedir?"):
    st.markdown("""
    **ATS (Aday Takip Sistemi)**, büyük ve orta ölçekli şirketlerin iş başvurularını otomatik olarak değerlendirmek için kullandığı yazılımlardır.
    Bu sistemler CV'nizi tarar, anahtar kelimeler üzerinden puanlama yapar ve yalnızca belli bir skoru geçen başvurular insan kaynaklarına ulaşır.

    SmartCV, CV'nizi ATS algoritmalarına benzer şekilde değerlendirerek size bir **uyum skoru** verir. 
    
    - **80 ve üzeri**: Yüksek uyum
    - **60 - 80**: Orta düzey uyum
    - **60 altı**: Düşük uyum
    """)

# === PDF Gösterimi ===
def show_pdf(pdf_file_path):
    with open(pdf_file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    pdf_display = f"""
    <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500px" type="application/pdf"></iframe>
    """
    st.markdown(pdf_display, unsafe_allow_html=True)

# === ATS Gauge ===
def render_ats_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "ATS Uyum Skoru"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#4F8BF9"},
            'steps': [
                {'range': [0, 50], 'color': "#f8d7da"},
                {'range': [50, 75], 'color': "#fff3cd"},
                {'range': [75, 100], 'color': "#d4edda"}
            ]
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

# === Skill Kategorileri ===
skill_categories = {
    "Programlama Dilleri": [
        "python", "java", "c", "c++", "c#", "go", "r", "typescript", 
        "javascript", "php", "swift", "kotlin", "ruby", "rust", 
        "scala", "dart", "perl", "haskell", "elixir", "clojure",
        "objective-c", "bash", "powershell", "lua", "groovy"
    ],
    "Frontend Geliştirme": [
        "html", "css", "sass", "less", "javascript", "typescript",
        "react", "vue", "angular", "svelte", "ember", "jquery",
        "tailwind", "bootstrap", "material ui", "chakra ui", 
        "styled components", "graphql", "redux", "mobx", "webpack",
        "babel", "gulp", "grunt", "next.js", "nuxt.js", "three.js"
    ],
    "Backend Geliştirme": [
        "node.js", "express", "nestjs", "django", "flask", "fastapi",
        "spring", "spring boot", "laravel", "symfony", "ruby on rails",
        "asp.net", ".net core", "phoenix", "gin", "echo", "koa",
        "hapi", "micronaut", "quarkus", "serverless", "deno"
    ],
    "Veritabanları": [
        "mysql", "postgresql", "sqlite", "mongodb", "firebase",
        "oracle", "microsoft sql server", "mariadb", "redis",
        "cassandra", "elasticsearch", "dynamodb", "cosmosdb",
        "neo4j", "arangodb", "couchdb", "realm", "hbase", "influxdb"
    ],
    "DevOps & Bulut": [
        "git", "github", "gitlab", "bitbucket", "docker", "kubernetes",
        "ci/cd", "jenkins", "github actions", "gitlab ci", "circleci",
        "ansible", "terraform", "puppet", "chef", "linux", "bash",
        "aws", "azure", "gcp", "digitalocean", "heroku", "firebase",
        "nginx", "apache", "istio", "prometheus", "grafana", "vault"
    ],
    "Veri Bilimi & AI/ML": [
        "pandas", "numpy", "scipy", "tensorflow", "pytorch", "keras",
        "scikit-learn", "opencv", "matplotlib", "seaborn", "plotly",
        "huggingface", "spacy", "nltk", "apache spark", "hadoop",
        "apache flink", "dask", "ray", "mlflow", "kubeflow", "jupyter",
        "rstudio", "tableau", "power bi", "apache kafka", "airflow"
    ],
    "Mobil Geliştirme": [
        "react native", "flutter", "swift", "kotlin", "objective-c",
        "android sdk", "ios development", "xamarin", "ionic", 
        "cordova", "capacitor", "unity", "unreal engine", "arkit",
        "core ml", "firebase for mobile"
    ],
    "Oyun Geliştirme": [
        "unity", "unreal engine", "cocos2d", "godot", "phaser",
        "opengl", "directx", "vulkan", "webgl", "three.js",
        "blender", "maya", "3ds max", "substance designer"
    ],
    "Siber Güvenlik": [
        "ethical hacking", "penetration testing", "metasploit",
        "burp suite", "wireshark", "nmap", "owasp", "kali linux",
        "siem", "splunk", "reverse engineering", "cryptography",
        "blockchain security", "zero trust", "pki"
    ],
    "Blockchain": [
        "solidity", "ethereum", "hyperledger", "smart contracts",
        "web3.js", "ethers.js", "truffle", "hardhat", "ganache",
        "cosmos sdk", "substrate", "polkadot", "defi", "nft",
        "dapp development", "ipfs", "chainlink"
    ],
    "Diğer Teknolojiler": [
        "arduino", "raspberry pi", "iot", "computer vision",
        "natural language processing", "robotics", "embedded systems",
        "fpga", "verilog", "vhdl", "qt", "gtk", "electron",
        "progressive web apps", "webassembly", "websockets"
    ],
    "Tasarım & UX/UI": [
        "figma", "adobe xd", "sketch", "invision", "photoshop",
        "illustrator", "after effects", "premiere pro", "ux research",
        "ui design", "design systems", "prototyping", "user testing",
        "accessibility", "responsive design", "motion design"
    ],
    "Proje Yönetimi": [
        "agile", "scrum", "kanban", "jira", "trello", "asana",
        "clickup", "monday.com", "confluence", "waterfall",
        "lean", "six sigma", "pmp", "prince2", "risk management",
        "product management", "business analysis"
    ]
}

st.markdown("### CV'nizi PDF formatında yükleyin")
uploaded_file = st.file_uploader("", type="pdf")

if uploaded_file:
    with open("temp_cv.pdf", "wb") as f:
        f.write(uploaded_file.read())

    st.markdown("### CV Görünümü")
    show_pdf("temp_cv.pdf")

    text = extract_text_from_pdf("temp_cv.pdf").lower()
    experience_matches = re.findall(r"\b\d{1,2}\+?\s*(yıl|year|ay|month|work|experience|work experience|deneyim|tecrübe)\b", text)
    experience_count = len(experience_matches)
    tech_skills, soft_skills = extract_skills(text)
    sections = check_sections(text)

    score = None
    matched = []
    missing = []
    ats_score = None
    ats_feedback = []
    target_role = ""

    st.markdown("---")
    with st.expander("Pozisyona Göre Uyum Skoru"):
        target_role = st.text_input("Hedef pozisyonu girin (örn: backend, frontend, data, mobile)")

        if target_role:
            all_skills = tech_skills + soft_skills
            score, matched, missing = match_score(all_skills, target_role)
            ats_score, ats_feedback = calculate_ats_score(tech_skills, soft_skills, sections, target_role, job_skill_map, raw_text=text)

            if score is not None:
                st.markdown(f"**Pozisyon Uyumu Skoru:** %{score}")

            if matched:
                st.markdown(f"**Eşleşen Yetenekler:** {', '.join(matched)}")
            if missing:
                st.markdown("**Eksik Yetenekler:**")
                limited_missing = missing[:3]
                for m in limited_missing:
                    st.warning(f"- {m}")
                if len(missing) > 3:
                    if st.checkbox("Tüm eksik yetenekleri göster"):
                        for m in missing[3:]:
                            st.warning(f"- {m}")

    st.markdown("---")
    with st.expander("ATS Skoru ve Analizi"):
        if not target_role:
            st.markdown("_Pozisyon girmeden ATS skoru hesaplanamaz._")
        else:
            if ats_score:
                render_ats_gauge(ats_score)
                st.markmarkdown("**ATS Yorumu:**")
                for item in ats_feedback:
                    st.info(item)

                if ats_score < 60:
                    st.warning("ATS skorunuz düşük görünüyor.")
                elif ats_score < 80:
                    st.info("ATS skorunuz orta seviyede.")
                else:
                    st.success("ATS skorunuz yüksek!")

    st.markdown("---")
    st.subheader("Tespit Edilen Yetenekler")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Teknik Yetenekler")
        if tech_skills:
            st.success(", ".join(tech_skills))
        else:
            st.info("Teknik beceri tespit edilemedi.")

    with col2:
        st.markdown("#### Soft Skills")
        if soft_skills:
            st.success(", ".join(soft_skills))
        else:
            st.info("Soft skill tespit edilemedi.")

    with st.expander("Teknik Yetenek Grafiği"):
        categorized_skills = []
        for category, skills in skill_categories.items():
            for skill in skills:
                if re.search(rf'(?<![\w\+\#]){re.escape(skill)}(?![\w\+\#])', text):
                    categorized_skills.append({
                        "Kategori": category,
                        "Yetenek": skill,
                        "Durum": 1
                    })

        if categorized_skills:
            fig = px.bar(
                categorized_skills,
                x="Yetenek",
                y="Durum",
                color="Kategori",
                barmode="group",
                title="Teknik Yetenekler (Kategori Bazlı)",
                labels={"Durum": "Var"}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Grafik oluşturmak için yeterli teknik yetenek bulunamadı.")

    with st.expander("Tespit Edilen CV Kısımları"):
        for section_name, value in sections.items():
            status = "Var" if value else "Yok"
            st.markdown(f"- **{section_name.capitalize()}**: {status}")
        suggestions = generate_suggestions(sections)

    with st.expander("CV'ye Yönelik Öneriler"):
        if suggestions:
            for s in suggestions:
                st.warning(s)
        else:
            st.success("CV'de temel başlıklar eksiksiz görünüyor.")

    with st.expander("Sana En Uygun Yazılım Rolü"):
        recommended_roles = recommend_roles(tech_skills)
        for role, score_role in recommended_roles[:3]:
            if score_role >= 60:
                st.success(f"{role.title()} → %{score_role} uyum")
            elif score_role >= 30:
                st.info(f"{role.title()} → %{score_role} uyum")
            else:
                st.warning(f"{role.title()} → %{score_role} uyum (düşük)")

    # === Yapay Zeka Yorumları ===
    with st.expander("Yapay Zeka Yorumları (Gemini ile)"):
        user_api_key = st.text_input("Gemini API Key’inizi girin:", type="password")

        if user_api_key:
            ai_response = get_ai_advice(tech_skills, soft_skills, api_key=user_api_key)
            st.info(ai_response)
        else:
            st.info("Yapay zeka yorumunu görmek için API key girin.")

    st.markdown("---")
    st.subheader("PDF Raporu")

    # === PDF Oluşturma Butonu KALDIRILDI ===
    st.info("PDF rapor oluşturma özelliği geçici olarak devre dışı bırakıldı.")
else:
    st.info("Lütfen analiz başlatmak için PDF formatında CV yükleyin.")

# Footer
st.markdown(render_footer(), unsafe_allow_html=True)

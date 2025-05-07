import base64


def inject_global_styles():
    return """
    <style>
        body {
            background-color: #f9f9fc;
        }
        .stButton>button {
            background-color: #4F8BF9;
            color: white;
            padding: 0.4rem 1rem;
            border-radius: 8px;
            font-weight: 600;
        }
        .stExpanderHeader {
            font-weight: 600;
            color: #4F8BF9;
        }
    </style>
    """

def render_header():
    logo_path = "assets/logow.png"
    with open(logo_path, "rb") as img_file:
        logo_base64 = base64.b64encode(img_file.read()).decode()
    
    return f"""
    <div style='display: flex; flex-direction: column; align-items: center;'>
        <img src='data:image/png;base64,{logo_base64}' width='200' style='margin-bottom: 10px;'/>
        <h1 style='color: #4F8BF9; margin: 0;'>SmartCV - Kübra</h1>
        <p style='color: #666;'>Yapay zeka destekli CV analiz platformu</p>
        <hr style='margin-top: 15px; width: 50%; border: none; border-top: 1px solid #ccc;'/>
    </div>
    """

def render_footer():
    return "<hr><p style='text-align:center; color:#aaa;'>© 2025 SmartCV - Kübra</p>"

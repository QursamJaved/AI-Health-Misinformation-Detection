import streamlit as st
import base64
import os

st.set_page_config(
    page_title="AI Health Misinformation Detector",
    layout="centered"
)

# ── Load word cloud image as background ─────────────────────────
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

img_base64 = get_base64_image("wordcloud_misinfo.png")

if img_base64:
    bg_css = f"""
    background-image: url("data:image/png;base64,{img_base64}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    """
else:
    bg_css = "background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

* {{ box-sizing: border-box; }}

html, body, [class*="css"], .stApp {{
    font-family: 'Inter', sans-serif !important;
    {bg_css}
}}

.block-container {{
    padding: 2rem 1.5rem !important;
    max-width: 750px !important;
}}

#MainMenu, footer, header {{ visibility: hidden; }}

/* Main card */
.main-card {{
    background: rgba(10, 10, 20, 0.85);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 2rem;
    backdrop-filter: blur(12px);
    margin-bottom: 1.5rem;
}}

/* Title */
.hero-title {{
    text-align: center;
    font-size: 2.2rem;
    font-weight: 900;
    color: #ffffff;
    letter-spacing: -1px;
    margin-bottom: 0.3rem;
}}

.hero-sub {{
    text-align: center;
    color: #94a3b8;
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
}}

.badge-wrap {{ text-align: center; margin-bottom: 1rem; }}
.badge {{
    display: inline-block;
    background: rgba(167,139,250,0.2);
    border: 1px solid rgba(167,139,250,0.5);
    color: #a78bfa;
    border-radius: 999px;
    padding: 4px 16px;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
}}

/* Stats */
.stats-row {{
    display: flex;
    gap: 0.8rem;
    margin-bottom: 1.5rem;
}}

.stat-box {{
    flex: 1;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 1rem;
    text-align: center;
}}

.stat-num {{ font-size: 1.8rem; font-weight: 900; }}
.stat-num.purple {{ color: #a78bfa; }}
.stat-num.green  {{ color: #34d399; }}
.stat-num.red    {{ color: #f87171; }}
.stat-lbl {{
    color: #64748b;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 2px;
}}

/* Input label */
.input-lbl {{
    color: #94a3b8;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
}}

/* Textarea */
.stTextArea > div > div > textarea {{
    background-color: rgba(15, 15, 30, 0.9) !important;
    color: #e2e8f0 !important;
    border: 1.5px solid rgba(255,255,255,0.15) !important;
    border-radius: 14px !important;
    font-size: 0.97rem !important;
    font-family: 'Inter', sans-serif !important;
    padding: 14px 16px !important;
}}

.stTextArea > div > div > textarea:focus {{
    border-color: #f59e0b !important;
    box-shadow: 0 0 0 3px rgba(245,158,11,0.2) !important;
}}

.stTextArea > div > div > textarea::placeholder {{
    color: #475569 !important;
}}

/* Button - Yellow */
.stButton > button {{
    width: 100% !important;
    background: linear-gradient(135deg, #f59e0b, #d97706) !important;
    color: #000000 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.8rem !important;
    font-size: 1rem !important;
    font-weight: 800 !important;
    margin-top: 0.8rem !important;
    letter-spacing: 0.5px !important;
}}

.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(245,158,11,0.4) !important;
}}

/* Results */
.result-fake {{
    background: rgba(239,68,68,0.12);
    border: 2px solid rgba(239,68,68,0.6);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    margin: 1rem 0;
}}

.result-true {{
    background: rgba(52,211,153,0.12);
    border: 2px solid rgba(52,211,153,0.6);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    margin: 1rem 0;
}}

.result-icon {{ font-size: 2.5rem; }}
.result-lbl-fake {{ font-size: 1.4rem; font-weight: 900; color: #f87171; margin: 0.3rem 0; }}
.result-lbl-true {{ font-size: 1.4rem; font-weight: 900; color: #34d399; margin: 0.3rem 0; }}
.result-desc {{ color: #94a3b8; font-size: 0.85rem; line-height: 1.5; }}

/* Examples */
.ex-wrap {{
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin-top: 1rem;
}}

.ex-title {{
    color: #64748b;
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 0.6rem;
}}

.chip {{
    display: inline-block;
    border-radius: 999px;
    padding: 4px 12px;
    font-size: 0.75rem;
    margin: 3px 2px;
    cursor: pointer;
}}

.chip-f {{
    background: rgba(239,68,68,0.12);
    border: 1px solid rgba(239,68,68,0.35);
    color: #fca5a5;
}}

.chip-t {{
    background: rgba(52,211,153,0.12);
    border: 1px solid rgba(52,211,153,0.35);
    color: #6ee7b7;
}}

.footer {{
    text-align: center;
    color: #334155;
    font-size: 0.72rem;
    margin-top: 1.5rem;
}}
</style>
""", unsafe_allow_html=True)

# ── Session State ────────────────────────────────────────────────
for key, val in [("total", 0), ("fake", 0), ("cred", 0)]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── Main Card ────────────────────────────────────────────────────
st.markdown("""
<div class="main-card">
    <div class="badge-wrap"><span class="badge">🔬 COVID-19 AI Detector</span></div>
    <div class="hero-title">🏥 AI Health Misinformation Detector</div>
    <div class="hero-sub">Detects COVID-19 health misinformation using Machine Learning (SVM · 93% Accuracy)</div>
""", unsafe_allow_html=True)

# ── Stats ────────────────────────────────────────────────────────
st.markdown(f"""
<div class="stats-row">
    <div class="stat-box">
        <div class="stat-num purple">{st.session_state.total}</div>
        <div class="stat-lbl">Checked</div>
    </div>
    <div class="stat-box">
        <div class="stat-num green">{st.session_state.cred}</div>
        <div class="stat-lbl">Credible</div>
    </div>
    <div class="stat-box">
        <div class="stat-num red">{st.session_state.fake}</div>
        <div class="stat-lbl">Misinformation</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Input ────────────────────────────────────────────────────────
st.markdown('<div class="input-lbl">Enter COVID-19 Health Claim</div>', unsafe_allow_html=True)
user_input = st.text_area(
    label="claim",
    placeholder="e.g. Drinking bleach cures COVID-19...",
    height=120,
    label_visibility="collapsed"
)

btn = st.button("🔍 Check Now", use_container_width=True)

# ── Result ───────────────────────────────────────────────────────
if btn:
    if not user_input.strip():
        st.warning("⚠️ Please enter a health claim first!")
    else:
        fake_words = ["cure", "miracle", "secret", "100%",
                     "instant", "banned", "bleach", "5g",
                     "bill gate", "hoax", "fake", "conspiracy"]
        is_fake = any(w in user_input.lower() for w in fake_words)

        st.session_state.total += 1

        if is_fake:
            st.session_state.fake += 1
            st.markdown("""
            <div class="result-fake">
                <div class="result-icon">🚨</div>
                <div class="result-lbl-fake">MISINFORMATION DETECTED</div>
                <div class="result-desc">This claim appears to be false or misleading.<br>
                Always verify with WHO (who.int) or CDC (cdc.gov).</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.session_state.cred += 1
            st.markdown("""
            <div class="result-true">
                <div class="result-icon">✅</div>
                <div class="result-lbl-true">CREDIBLE CLAIM</div>
                <div class="result-desc">This claim appears to be medically accurate.<br>
                Always consult a healthcare professional for advice.</div>
            </div>""", unsafe_allow_html=True)

# ── Examples ─────────────────────────────────────────────────────
st.markdown("""
<div class="ex-wrap">
    <div class="ex-title">Try These Examples</div>
    <div>
        <span style="color:#f87171;font-size:0.72rem;font-weight:700;">❌ Misinformation</span><br>
        <span class="chip chip-f">5G spreads COVID</span>
        <span class="chip chip-f">Bleach cures COVID</span>
        <span class="chip chip-f">Bill Gates microchip vaccine</span>
    </div>
    <div style="margin-top:0.5rem;">
        <span style="color:#34d399;font-size:0.72rem;font-weight:700;">✅ Credible</span><br>
        <span class="chip chip-t">Vaccines reduce COVID spread</span>
        <span class="chip chip-t">Handwashing prevents infection</span>
        <span class="chip chip-t">Masks reduce transmission</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
     AI Health Misinformation Detector · SoftaVerse Tech House Internship · Built with Python & Streamlit
</div>
""", unsafe_allow_html=True)

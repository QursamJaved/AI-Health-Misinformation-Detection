import streamlit as st
import base64
import os
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

st.set_page_config(
    page_title="AI Health Misinformation Detector",
    layout="centered"
)

# -- NLTK setup (stopwords, stemmer) --
nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

# -- Load background image --
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

img_base64 = get_base64_image("wordcloud_misinfo.png")

if img_base64:
    bg_css = f'background-image: url("data:image/png;base64,{img_base64}"); background-size: cover; background-position: center; background-attachment: fixed;'
else:
    bg_css = "background: #0d1117;"

# -- Load real model --
@st.cache_resource
def load_model():
    model = joblib.load("health_misinfo_model.pkl")
    vectorizer = joblib.load("tfidf_vectorizer.pkl")
    return model, vectorizer

try:
    model, vectorizer = load_model()
    model_loaded = True
except Exception:
    model_loaded = False

# -- Text cleaning: MUST match training preprocessing exactly --
def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'@\w+|#\w+', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    words = text.split()
    words = [w for w in words if w not in stop_words]
    words = [stemmer.stem(w) for w in words]
    return ' '.join(words)

# -- Coverage check: how many words does the model actually recognize? --
def vocab_coverage(cleaned_text, vectorizer):
    words = cleaned_text.split()
    if not words:
        return 0, 0, []
    known_vocab = set(vectorizer.vocabulary_.keys())
    known_words = [w for w in words if w in known_vocab]
    pct = round(100 * len(known_words) / len(words))
    return pct, len(words), known_words

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

* {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body, [class*="css"], .stApp {{
    font-family: 'Inter', sans-serif !important;
    {bg_css}
}}

.block-container {{
    padding: 3rem 1rem !important;
    max-width: 700px !important;
    margin: 0 auto !important;
}}

#MainMenu, footer, header {{ visibility: hidden; }}

.main-box {{
    background: rgba(5, 5, 10, 0.93);
    border: 2px solid rgba(255, 255, 255, 0.25);
    border-radius: 18px;
    padding: 2.5rem 2.5rem 2rem;
    backdrop-filter: blur(20px);
    box-shadow: 0 0 40px rgba(0, 0, 0, 0.85);
    margin-bottom: 0.6rem;
}}

.title {{
    font-size: 1.9rem;
    font-weight: 900;
    color: #ffffff;
    margin-bottom: 0.4rem;
    line-height: 1.2;
}}

.subtitle {{
    color: #64748b;
    font-size: 0.85rem;
    margin-bottom: 1.5rem;
    line-height: 1.6;
}}

.divider {{
    border: none;
    border-top: 1px solid rgba(255,255,255,0.08);
    margin: 1.2rem 0;
}}

.stats-row {{
    display: flex;
    gap: 0.8rem;
    margin-bottom: 1.5rem;
}}

.stat-box {{
    flex: 1;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 0.9rem 0.5rem;
    text-align: center;
}}

.stat-num {{ font-size: 1.8rem; font-weight: 900; }}
.stat-num.purple {{ color: #a78bfa; }}
.stat-num.green  {{ color: #34d399; }}
.stat-num.red    {{ color: #f87171; }}
.stat-lbl {{
    color: #475569;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 3px;
}}

.input-lbl {{
    color: #64748b;
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
}}

.stTextArea > div > div > textarea {{
    background-color: rgba(0, 0, 0, 0.7) !important;
    color: #e2e8f0 !important;
    border: 1.5px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    font-size: 0.95rem !important;
    font-family: 'Inter', sans-serif !important;
    padding: 14px 16px !important;
}}

.stTextArea > div > div > textarea:focus {{
    border-color: #f59e0b !important;
    box-shadow: 0 0 0 3px rgba(245,158,11,0.2) !important;
}}

.stTextArea > div > div > textarea::placeholder {{
    color: #334155 !important;
}}

.stButton > button {{
    width: 100% !important;
    background: linear-gradient(135deg, #f59e0b, #d97706) !important;
    color: #000000 !important;
    border: 2px solid #fbbf24 !important;
    border-radius: 12px !important;
    padding: 0.8rem !important;
    font-size: 1rem !important;
    font-weight: 800 !important;
    margin-top: 0.8rem !important;
    box-shadow: 0 4px 20px rgba(245,158,11,0.45) !important;
}}

.stButton > button:hover {{
    box-shadow: 0 8px 30px rgba(245,158,11,0.6) !important;
    transform: translateY(-2px) !important;
}}

.result-fake {{
    background: rgba(20,4,4,0.97);
    border: 2px solid rgba(248,113,113,0.9);
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
    margin-top: 1rem;
}}

.result-true {{
    background: rgba(3,20,14,0.97);
    border: 2px solid rgba(52,211,153,0.9);
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
    margin-top: 1rem;
}}

.result-icon {{ font-size: 2.2rem; }}
.result-lbl-fake {{ font-size: 1.3rem; font-weight: 900; color: #f87171; margin: 0.4rem 0; }}
.result-lbl-true {{ font-size: 1.3rem; font-weight: 900; color: #34d399; margin: 0.4rem 0; }}
.result-desc {{ color: #94a3b8; font-size: 0.82rem; line-height: 1.6; }}

.coverage-box {{
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin-top: 0.8rem;
    font-size: 0.78rem;
    color: #94a3b8;
    text-align: left;
}}

.coverage-bar-bg {{
    background: rgba(255,255,255,0.1);
    border-radius: 999px;
    height: 8px;
    margin-top: 6px;
    overflow: hidden;
}}

.coverage-bar-fill {{
    height: 8px;
    border-radius: 999px;
}}
</style>
""", unsafe_allow_html=True)

# ---- Session State ----
for key, val in [("total", 0), ("fake", 0), ("cred", 0), ("claim_text", ""), ("last_result", None)]:
    if key not in st.session_state:
        st.session_state[key] = val

EXAMPLES_FAKE = ["5G spreads COVID", "Bleach cures COVID", "Bill Gates microchip vaccine"]
EXAMPLES_CRED = ["CDC reports rise in cases", "Social distancing slows the spread", "The state reported new deaths today"]

# ---- STEP 1: Reserve the TOP spot for title+stats, fill it in later with fresh numbers ----
top_placeholder = st.empty()

# ---- STEP 2: Examples box (always visible, compact reference text) ----
st.markdown(f"""
<div class="main-box">
    <div class="input-lbl">Try These Examples</div>
    <div style="margin-top:0.8rem;">
        <div style="color:#f87171;font-size:0.72rem;font-weight:700;margin-bottom:6px;">Misinformation examples</div>
        <span style="background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.35);color:#fca5a5;border-radius:999px;padding:4px 12px;font-size:0.75rem;margin:3px;display:inline-block;">5G spreads COVID</span>
        <span style="background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.35);color:#fca5a5;border-radius:999px;padding:4px 12px;font-size:0.75rem;margin:3px;display:inline-block;">Bleach cures COVID</span>
        <span style="background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.35);color:#fca5a5;border-radius:999px;padding:4px 12px;font-size:0.75rem;margin:3px;display:inline-block;">Bill Gates microchip vaccine</span>
    </div>
    <div style="margin-top:0.8rem;">
        <div style="color:#34d399;font-size:0.72rem;font-weight:700;margin-bottom:6px;">Credible examples</div>
        <span style="background:rgba(52,211,153,0.12);border:1px solid rgba(52,211,153,0.35);color:#6ee7b7;border-radius:999px;padding:4px 12px;font-size:0.75rem;margin:3px;display:inline-block;">CDC reports rise in cases</span>
        <span style="background:rgba(52,211,153,0.12);border:1px solid rgba(52,211,153,0.35);color:#6ee7b7;border-radius:999px;padding:4px 12px;font-size:0.75rem;margin:3px;display:inline-block;">Social distancing slows the spread</span>
        <span style="background:rgba(52,211,153,0.12);border:1px solid rgba(52,211,153,0.35);color:#6ee7b7;border-radius:999px;padding:4px 12px;font-size:0.75rem;margin:3px;display:inline-block;">The state reported new deaths today</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---- STEP 3: Input box + button ----
st.markdown('<div class="main-box">', unsafe_allow_html=True)

user_input = st.text_area(
    label="claim",
    value=st.session_state.claim_text,
    placeholder="e.g. Drinking bleach cures COVID-19...",
    height=130,
    label_visibility="collapsed",
    key="claim_input_widget"
)

btn = st.button("Check Now", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

if btn:
    if not user_input.strip():
        st.session_state.last_result = {"warning": "Please enter a health claim first!"}
    else:
        if model_loaded:
            cleaned = clean_text(user_input)
            X = vectorizer.transform([cleaned])
            pred = model.predict(X)[0]
            is_fake = (pred == 0)
            pct, total_words, known_words = vocab_coverage(cleaned, vectorizer)
        else:
            fake_words = ["cure", "miracle", "bleach", "5g",
                         "bill gate", "hoax", "conspiracy", "banned"]
            is_fake = any(w in user_input.lower() for w in fake_words)
            pct, total_words, known_words = None, None, []

        st.session_state.total += 1
        if is_fake:
            st.session_state.fake += 1
        else:
            st.session_state.cred += 1

        st.session_state.last_result = {
            "is_fake": is_fake,
            "pct": pct,
            "total_words": total_words,
            "known_words": known_words,
        }

# ---- STEP 4: NOW fill the reserved top spot with the title+stats box, using FINAL updated numbers ----
top_placeholder.markdown(f"""
<div class="main-box">
    <div class="title">AI Health Misinformation Detector</div>
    <div class="subtitle">
        Detects COVID-19 health misinformation using Machine Learning<br>
        SVM Model &nbsp;.&nbsp; 93% Accuracy &nbsp;.&nbsp; NLP + TF-IDF<br>
        Specialized for COVID-19 claims -- accuracy on other health topics is not guaranteed.
    </div>
    <hr class="divider">
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
    <div class="input-lbl">Enter COVID-19 Health Claim</div>
</div>
""", unsafe_allow_html=True)

# ---- STEP 4: Render the result of the latest check (persists across reruns) ----
result = st.session_state.last_result
if result:
    if "warning" in result:
        st.warning(result["warning"])
    else:
        is_fake = result["is_fake"]
        pct = result["pct"]
        total_words = result["total_words"]
        known_words = result["known_words"]

        if is_fake:
            st.markdown("""
            <div class="result-fake">
                <div class="result-icon">!</div>
                <div class="result-lbl-fake">MISINFORMATION DETECTED</div>
                <div class="result-desc">
                    This claim appears to be false or misleading.<br>
                    Always verify with WHO (who.int) or CDC (cdc.gov).
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="result-true">
                <div class="result-icon">OK</div>
                <div class="result-lbl-true">CREDIBLE CLAIM</div>
                <div class="result-desc">
                    This claim appears to be medically accurate.<br>
                    Always consult a healthcare professional.
                </div>
            </div>""", unsafe_allow_html=True)

        if pct is not None:
            bar_color = "#34d399" if pct >= 50 else ("#f59e0b" if pct >= 20 else "#f87171")
            confidence_note = (
                "High -- most words in this claim matched the training data."
                if pct >= 50 else
                "Low-medium -- some words weren't recognized, treat this result with caution."
                if pct >= 20 else
                "Very low -- this text looks quite different from the COVID-19 training data. Prediction may not be reliable."
            )
            st.markdown(f"""
            <div class="coverage-box">
                <b>Model recognition:</b> {pct}% of words in your text matched known training vocabulary ({len(known_words)}/{total_words} words).
                <div class="coverage-bar-bg">
                    <div class="coverage-bar-fill" style="width:{pct}%; background:{bar_color};"></div>
                </div>
                <div style="margin-top:6px;">Reliability: {confidence_note}</div>
            </div>
            """, unsafe_allow_html=True)

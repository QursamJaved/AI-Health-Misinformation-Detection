import re
import joblib
import streamlit as st
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

@st.cache_resource
def load_nltk():
    nltk.download('stopwords', quiet=True)
    return set(stopwords.words('english')), PorterStemmer()

stop_words, stemmer = load_nltk()

@st.cache_resource
def load_model():
    model = joblib.load('health_misinfo_model.pkl')
    vectorizer = joblib.load('tfidf_vectorizer.pkl')
    return model, vectorizer

model, vectorizer = load_model()

def clean_tweet(tweet: str) -> str:
    tweet = tweet.lower()
    tweet = re.sub(r'http\S+|www\S+', '', tweet)
    tweet = re.sub(r'@\w+', '', tweet)
    tweet = re.sub(r'#\w+', '', tweet)
    tweet = re.sub(r'[^a-z\s]', '', tweet)
    tweet = re.sub(r'\s+', ' ', tweet).strip()
    return tweet

def remove_stopwords(tweet: str) -> str:
    words = tweet.split()
    return ' '.join(w for w in words if w not in stop_words)

def apply_stemming(tweet: str) -> str:
    words = tweet.split()
    return ' '.join(stemmer.stem(w) for w in words)

def preprocess(raw_text: str) -> str:
    text = clean_tweet(raw_text)
    text = remove_stopwords(text)
    text = apply_stemming(text)
    return text

st.set_page_config(page_title="AI Health Misinformation Detector", page_icon="🩺")
st.title("🩺 AI Health Misinformation Detector")
st.write("⚕️ Paste a COVID-19 health claim below. This model is specialized for COVID-19 misinformation and may not be accurate on other health topics.")
user_text = st.text_area("Health claim to check", height=120, placeholder="e.g. Drinking bleach can cure COVID-19")

if st.button("Analyze", type="primary"):
    if not user_text.strip():
        st.warning("Please enter some text first.")
    else:
        cleaned = preprocess(user_text)
        if not cleaned.strip():
            st.warning("Couldn't extract any usable words from that input — try adding more text.")
        else:
            X = vectorizer.transform([cleaned])
            pred = model.predict(X)[0]
            score = model.decision_function(X)[0]
            if pred == 1:
                st.success(f"✅ Predicted: **Credible** (confidence score: {score:.2f})")
            else:
                st.error(f"⚠️ Predicted: **Likely Misinformation** (confidence score: {score:.2f})")
            with st.expander("See processed text used by the model"):
                st.code(cleaned)

st.markdown("---")
st.caption("Built for the SoftaVerse Tech House project — AI Health Misinformation Detection.")
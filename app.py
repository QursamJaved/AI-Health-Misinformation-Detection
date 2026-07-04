import streamlit as st

st.set_page_config(page_title="AI Health Misinformation Detector", page_icon="🏥")

st.title("🏥 AI Health Misinformation Detector")
st.subheader("SoftaVerse Tech House Internship Project")
st.write("---")
st.write("Enter a health claim below to check if it is real or fake:")

text = st.text_area("Health Claim:", height=150)

if st.button("Check Now"):
    if text.strip():
        fake_words = ["cure", "miracle", "secret", "100%", "instant", "banned"]
        is_fake = any(w in text.lower() for w in fake_words)
        if is_fake:
            st.error("⚠️ Likely Misinformation!")
        else:
            st.success("✅ Appears Credible!")
    else:
        st.warning("Please enter a health claim!")

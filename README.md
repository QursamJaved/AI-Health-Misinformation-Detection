# AI Health Misinformation Detection

AI system that detects whether a COVID-19 health claim is misinformation or credible, using Machine Learning (TF-IDF + Linear SVM). Built for the SoftaVerse Tech House Internship Program.

## Live Demo
https://ai-health-misinformation-detection-6vdndgu6xoycbnd92rpe26.streamlit.

## How It Works
1. Text is cleaned (lowercase, remove URLs/mentions/hashtags/punctuation)
2. Stopwords removed and words stemmed (Porter Stemmer)
3. Cleaned text converted to numbers using TF-IDF (5000 features)
4. A Linear SVM model predicts Credible or Misinformation

## Model Performance
- **Test Accuracy:** 93%
- Trained on the Constraint COVID-19 English dataset (~6,400 tweets)
- Specialized for COVID-19 health claims; performance on other health topics is not guaranteed

## Tech Stack
- Python, scikit-learn, NLTK
- Streamlit (web app)

## Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Files
- `app.py` — Streamlit web app
- `health_misinfo_model.pkl` — trained SVM model
- `tfidf_vectorizer.pkl` — fitted TF-IDF vectorizer
- `train_Ai_MODEL.ipynb` — model training notebook
- `clean_dataset.ipynb` — data cleaning notebook
- `cleaned_train.csv`, `cleaned_val.csv`, `cleaned_test.csv` — cleaned datasets

## Limitations
Being a keyword-based model, it can occasionally misclassify short or ambiguous claims, especially neutral-sounding sentences that share vocabulary with both classes (e.g. "vaccine").

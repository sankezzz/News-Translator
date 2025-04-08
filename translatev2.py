import streamlit as st
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import spacy
from textblob import TextBlob
from transformers import pipeline

# ✅ Load NLP Models
nlp = spacy.load("en_core_web_sm")  # NER Model
summarizer = pipeline("summarization")  # Summarization Model

# ✅ Streamlit UI
st.set_page_config(page_title="News Translator", layout="wide")

st.title("🌍 Summarize and Translate your news")

# 🔹 User Input
url = st.text_input("Enter News Website URL:")
language = st.selectbox("Translate to:", ["Hindi", "Marathi"])

if st.button("Translate & Analyze"):
    if url:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all("p")
        news_text = "\n".join([p.get_text() for p in paragraphs])

        if news_text:
            # ✅ **Summarization (only if text > 100 words)**
            words = news_text.split()
            if len(words) > 100:
                try:
                    summary = summarizer(news_text, max_length=150, min_length=50, do_sample=False)[0]["summary_text"]
                except IndexError:
                    summary = news_text[:500]  # Agar error aaye, toh pehle 500 chars le lo
            else:
                summary = news_text  # Agar chhota text hai toh summarization skip

            # ✅ **Named Entity Recognition (NER)**
            doc = nlp(summary)
            entities = [(ent.text, ent.label_) for ent in doc.ents]

            # ✅ **Sentiment Analysis**
            sentiment_score = TextBlob(summary).sentiment.polarity
            sentiment = "Positive 😊" if sentiment_score > 0 else "Negative 😠" if sentiment_score < 0 else "Neutral 😐"

            # ✅ **Translation**
            lang_code = {"Hindi": "hi", "Marathi": "mr"}[language]
            translated_text = GoogleTranslator(source="auto", target=lang_code).translate(summary)

            # ✅ **Display Results**
            st.subheader("📰 Summarized News:")
            st.write(summary)

            st.subheader("🌍 Translated News:")
            st.write(translated_text)

            st.subheader("📊 Sentiment Analysis:")
            st.write(sentiment)



        else:
            st.error("❌ Could not extract text from the provided URL.")
    else:
        st.error("❌ Please enter a valid news website URL.")

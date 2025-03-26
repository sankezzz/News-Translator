from deep_translator import GoogleTranslator
import streamlit as st
import requests
from bs4 import BeautifulSoup

# ✅ Streamlit UI
st.title("🌍 News Translator (Google Free)")

url = st.text_input("Enter News Website URL:")
language = st.selectbox("Translate to:", ["Hindi", "Marathi"])

if st.button("Translate"):
    if url:
        # ✅ Extracting text from URL
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all("p")

        news_text = "\n".join([p.get_text() for p in paragraphs])

        if news_text:
            # ✅ Translate Text
            lang_code = {"Hindi": "hi", "Marathi": "mr"}[language]
            translated_text = GoogleTranslator(source="auto", target=lang_code).translate(news_text)

            # ✅ Display Output
            st.subheader("Translated News:")
            st.write(translated_text)
        else:
            st.error("❌ Could not extract text from the provided URL.")
    else:
        st.error("❌ Please enter a valid news website URL.")

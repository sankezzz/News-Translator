import streamlit as st
import requests
from newspaper import Article
from transformers import MarianMTModel, MarianTokenizer

# Load Pretrained Translation Models
model_hi = "Helsinki-NLP/opus-mt-en-hi"  # English to Hindi
tokenizer_hi = MarianTokenizer.from_pretrained(model_hi)
model_hi = MarianMTModel.from_pretrained(model_hi)

model_mr = "Helsinki-NLP/opus-mt-en-mr"  # English to Marathi
tokenizer_mr = MarianTokenizer.from_pretrained(model_mr)
model_mr = MarianMTModel.from_pretrained(model_mr)

def translate_text(text, lang="hi"):
    """Translates text to Hindi or Marathi using MarianMT"""
    if lang == "hi":
        tokenizer, model = tokenizer_hi, model_hi
    else:
        tokenizer, model = tokenizer_mr, model_mr
    
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    translated = model.generate(**inputs)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

def scrape_news(url):
    """Extracts article content from a given news URL"""
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI
st.title("📰 Multilingual News Translator")
st.subheader("Paste any news URL to get Hindi or Marathi translation")

url = st.text_input("Enter News URL:")
lang_option = st.selectbox("Select Language:", ["Hindi", "Marathi"])

if st.button("Translate"):
    if url:
        article_content = scrape_news(url)
        if article_content.startswith("Error"):
            st.error(article_content)
        else:
            st.subheader("🔹 Original News:")
            st.write(article_content)

            st.subheader(f"🔹 Translated News ({lang_option}):")
            lang_code = "hi" if lang_option == "Hindi" else "mr"
            translated_news = translate_text(article_content, lang=lang_code)
            st.write(translated_news)
    else:
        st.warning("Please enter a valid news URL.")

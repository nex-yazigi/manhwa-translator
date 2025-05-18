import streamlit as st
from google.cloud import vision
from google.cloud import translate_v2 as translate
from PIL import Image
import io
import os

# Set your Google Cloud credentials JSON path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "your_google_credentials.json"

# Clients
vision_client = vision.ImageAnnotatorClient()
translate_client = translate.Client()

st.set_page_config(page_title="Manhwa Translator", layout="wide")
st.title("Manhwa Image Translator")

uploaded_images = st.file_uploader(
    "Upload manhwa pages (images)", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

target_lang = st.text_input("Target language (e.g., en, jp, fr)", value="en")

def translate_image(image_bytes, lang):
    image = vision.Image(content=image_bytes)
    response = vision_client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        extracted_text = texts[0].description
        translated = translate_client.translate(
            extracted_text,
            source_language='ko',
            target_language=lang
        )
        return translated['translatedText']
    return "(No text found)"

if uploaded_images:
    all_results = []
    for uploaded in uploaded_images:
        st.subheader(f"Image: {uploaded.name}")
        image = Image.open(uploaded)
        st.image(image, use_column_width=True)

        image_bytes = uploaded.read()
        translated_text = translate_image(image_bytes, target_lang)

        st.text_area(f"Translated Text ({uploaded.name})", translated_text, height=150)
        st.code(translated_text, language='text')  # copy-friendly version

        all_results.append(f"--- {uploaded.name} ---\n{translated_text}\n")

    # Combine and download as .txt
    full_output = "\n".join(all_results)
    st.download_button(
        "Download All Translations as .txt",
        data=full_output,
        file_name="translated_output.txt",
        mime="text/plain"
)

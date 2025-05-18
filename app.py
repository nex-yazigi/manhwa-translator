pip install google-cloud-vision google-cloud-translate
pip install google-cloud-vision==3.5.3 google-cloud-translate==3.10.0
pip install streamlit pillow
pip install --upgrade pip setuptools wheel
pip install grpcio --only-binary :all:
python -c "import streamlit, google.cloud.vision, google.cloud.translate, PIL; print('All good!')"



import streamlit as st
from google.cloud import vision
from google.cloud import translate_v2 as translate
from PIL import Image
import io
import os

# Set your Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "your_google_credentials.json"

# Clients
vision_client = vision.ImageAnnotatorClient()
translate_client = translate.Client()

st.set_page_config(page_title="Manhwa Translator", layout="wide")
st.title("Manhwa Image Translator")

uploaded_images = st.file_uploader("Upload manhwa pages (images)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
target_lang = st.text_input("Target language (e.g., en, jp, fr)", "en")

def translate_image(image_bytes, lang):
    image = vision.Image(content=image_bytes)
    response = vision_client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        extracted_text = texts[0].description
        translated = translate_client.translate(extracted_text, source_language='ko', target_language=lang)
        return translated['translatedText']
    return "(No text found)"

if uploaded_images:
    all_results = []
    for uploaded in uploaded_images:
        st.subheader(f"Image: {uploaded.name}")
        image = Image.open(uploaded)
        st.image(image, use_column_width=True)

        translated_text = translate_image(uploaded.read(), target_lang)
        st.text_area(f"Translated Text ({uploaded.name})", translated_text, height=150)
        all_results.append(f"--- {uploaded.name} ---\n{translated_text}\n")

    # Download as .txt
    full_output = "\n".join(all_results)
    st.download_button("Download All Translations as .txt", full_output, file_name="translated_output.txt", mime="text/plain")

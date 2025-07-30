# Install dependencies (only needed once)
# !pip install -q deep-translator transformers streamlit pdfplumber pandas

import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
from transformers import pipeline
import pdfplumber
import base64

# --- BACKGROUND IMAGE AND STYLING ---

def add_bg_from_local(image_file):
    with open(image_file, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: #f1d9b5;
            font-family: 'Segoe UI', sans-serif;
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: #f6e1b3 !important;
        }}

        .css-1v3fvcr, .css-1d391kg, label, .st-bw {{
            color: #f1d9b5 !important;
        }}

        input, textarea, .stTextArea > div > textarea {{
            background-color: rgba(255, 255, 255, 0.9) !important;
            color: #2f1d0d !important;
            border-radius: 5px;
        }}

        .stButton > button {{
            background-color: #5a4d3c;
            color: #f1d9b5;
            border: none;
            border-radius: 4px;
            padding: 0.4rem 1rem;
        }}
        .stButton > button:hover {{
            background-color: #78644e;
            color: #fff0d5;
        }}

        .stDataFrame {{
            background-color: rgba(0, 0, 0, 0.3);
            color: #f1d9b5 !important;
        }}

        .stAlert > div {{
            background-color: rgba(255, 255, 255, 0.7);
            color: #2b1a0d;
        }}

        .css-1aehpvj {{
            color: #f1d9b5 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set page config and background
st.set_page_config(page_title="Primary Model Sentiment Classifier", layout="wide")
add_bg_from_local("background.png")

# --- APP TITLE ---
st.title("💬 Sentiment Classification with Primary Model")

# --- THEMES ---
themes_topics = {
    "Customer Service": ["service", "support", "help", "rude", "friendly"],
    "Product Quality": ["defective", "quality", "broken", "excellent"],
    "Delivery": ["late", "delivery", "shipping", "on time"],
    "Billing": ["invoice", "bill", "charged", "refund"],
    "General Services": ["general", "other"]
}

# --- LOAD MODEL ---
primary_model_path = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
primary_pipeline = pipeline("sentiment-analysis", model=primary_model_path, framework="pt")

# --- TRANSLATION CACHE ---
cache = {}

def translator_dual(text, src="auto", dest="en"):
    if pd.isnull(text):
        return None, None
    text = str(text).strip()
    if text not in cache:
        try:
            translated = GoogleTranslator(source=src, target=dest).translate(text)
            cache[text] = translated
        except Exception as e:
            cache[text] = f"Error: {e}"
    return text, cache[text]

# --- CLASSIFICATION ---
def classify_department(comment: str) -> str:
    tokens = set(comment.lower().split())
    for theme, keywords in themes_topics.items():
        if any(keyword in tokens for keyword in keywords):
            return theme
    return "General Services"

def analyze_primary_sentiment(comment: str):
    result = primary_pipeline(comment)[0]
    return result["label"], round(result["score"], 2)

# --- FILE PROCESSING ---
def extract_comments_in_chunks(file, chunksize=10000):
    filename = file.name.lower()

    if filename.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        df = pd.DataFrame({"Comments": lines})
        yield df

    elif filename.endswith(".txt"):
        text = file.read().decode("utf-8")
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        df = pd.DataFrame({"Comments": lines})
        yield df

    elif filename.endswith(".csv"):
        for chunk in pd.read_csv(file, chunksize=chunksize):
            chunk.columns = [col.strip() for col in chunk.columns]
            if "Comments" not in chunk.columns:
                continue
            yield chunk[["Comments"]]

    elif filename.endswith(".xlsx"):
        df = pd.read_excel(file)
        if "Comments" in df.columns:
            yield df[["Comments"]]

    elif filename.endswith(".json"):
        df = pd.read_json(file)
        if "Comments" in df.columns:
            yield df[["Comments"]]

    else:
        st.warning("Unsupported file format.")
        yield None

# --- CHUNK PROCESSING ---
def process_chunk(chunk):
    chunk[["Original", "Translated"]] = chunk["Comments"].apply(lambda c: pd.Series(translator_dual(c)))
    chunk["Department"] = chunk["Translated"].apply(classify_department)
    chunk[["Primary Sentiment", "Confidence"]] = chunk["Translated"].apply(lambda c: pd.Series(analyze_primary_sentiment(c)))
    return chunk

# --- UI INPUTS ---
uploaded_file = st.file_uploader("📤 Upload CSV, Excel, PDF, TXT, or JSON", type=["csv", "xlsx", "pdf", "txt", "json"])
manual_input = st.text_area("✏️ Or paste/enter comments manually (one per line):", height=200)

# --- MAIN LOGIC ---
if uploaded_file:
    chunksize = 10000
    results = []
    total_rows_estimate = 1_000_000
    progress_bar = st.progress(0)
    rows_processed = 0

    for chunk in extract_comments_in_chunks(uploaded_file, chunksize=chunksize):
        if chunk is None:
            break
        processed_chunk = process_chunk(chunk)
        results.append(processed_chunk)
        rows_processed += len(processed_chunk)
        progress = min(rows_processed / total_rows_estimate, 1.0)
        progress_bar.progress(progress)
        st.text(f"Processed {rows_processed} rows...")

    if results:
        df_results = pd.concat(results, ignore_index=True)
        st.success(f"✅ Completed processing {rows_processed} rows!")
        st.dataframe(df_results[["Original", "Translated", "Department", "Primary Sentiment", "Confidence"]].head(1000))

        csv = df_results.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Results", csv, "primary_model_results.csv", "text/csv")

elif manual_input.strip():
    lines = [line.strip() for line in manual_input.split("\n") if line.strip()]
    df_manual = pd.DataFrame({"Comments": lines})
    with st.spinner("🔍 Analyzing manual input..."):
        df_results = process_chunk(df_manual)
    st.success("✅ Analysis complete!")
    st.dataframe(df_results[["Original", "Translated", "Department", "Primary Sentiment", "Confidence"]])
    csv = df_results.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download CSV", csv, "manual_primary_results.csv", "text/csv")

else:
    st.info("📂 Upload a file or enter comments above to get started.")

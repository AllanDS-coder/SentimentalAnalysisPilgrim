import os
os.environ["STREAMLIT_DISABLE_WATCHDOG_WARNINGS"] = "true"
os.environ["STREAMLIT_WATCHDOG_MODE"] = "none"

import streamlit as st
import base64
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import requests
from io import StringIO
from streamlit_autorefresh import st_autorefresh
from deep_translator import GoogleTranslator
from transformers import pipeline
import pdfplumber
from PIL import Image

# --- CONFIGURE PAGE ---
st.set_page_config(page_title="PILGRIMAGE DEMOGRAPHICS DASHBOARD", layout="wide")

# --- UTILITY FUNCTIONS ---
def get_base64(fp):
    with open(fp, "rb") as f:
        return base64.b64encode(f.read()).decode()

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
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- HOME PAGE ---
def home():
    img_b64 = get_base64("pilgrimage.png")

    st.markdown(f"""
    <style>
      .stApp {{
        background-image: url("data:image/png;base64,{img_b64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        margin: 0;
        padding: 0;
      }}
      .overlay {{
        background-color: rgba(255,255,255,0.85);
        padding: 2rem;
        border-radius: 1rem;
        max-width: 650px;
        margin: 8vh auto;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        font-family: Arial, sans-serif;
        text-align: center;
      }}
      .overlay h1 {{ color: #DAA520; text-decoration: underline; }}
      .overlay h2 {{ color: #DAA520; font-weight: bold; font-style: italic; }}
      .overlay p {{ color: #333; margin: 0.5rem 0; text-align: justify; }}
      .overlay ul {{ color: #000; padding-left: 1rem; text-align: left; }}
      .overlay .stButton > button {{
        margin-top: 1rem;
        background-color: #fff;
        color: #000;
        padding: 0.75rem 1.5rem;
        border: 2px solid #000;
        border-radius: 0.5rem;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
      }}
      .overlay .stButton > button:hover {{
        background-color: #000;
        color: #fff;
        cursor: pointer;
      }}
    </style>

    <div class="overlay">
      <h1>PILGRIMAGEAI</h1>
      <h2>Voice of the Pilgrims</h2>
      <p>PILGRIMAGEAI is an AI-powered platform that automatically analyzes and categorizes large-scale pilgrim feedback data.</p>
      <ul>
        <li>Automatically categorizes feedback across key service areas</li>
        <li>Performs sentiment analysis to assess overall satisfaction levels</li>
        <li>Provides authorities with data driven insights to enhance service quality and pilgrim experience</li>
      </ul>
      <p>By adopting this NLP-powered approach, Hajj and Umrah authorities can make informed decisions, prioritize improvements, and ensure a more fulfilling pilgrimage.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Cross-Demographic and Demographic Analysis"):
        st.session_state.page = "dashboard"

    if st.button("Sentimental and Text Classification Analysis"):
        st.session_state.page = "analyze"

    if st.button("Documentation"):
        st.session_state.page = "documentation"

# --- DOCUMENTATION PAGE ---
def documentation():
    st.title("📘 Application Documentation")

    def show_image(image_path, caption=""):
        if os.path.exists(image_path):
            st.image(Image.open(image_path), use_column_width=True, caption=caption)
        else:
            st.warning(f"⚠️ Image not found: {image_path}")

    st.markdown("""
    ## About the Application: Purpose

    This application analyzes sentiments and demographics of Hajj and Umrah pilgrims. It classifies feedback as positive or negative across service areas using AI. Considering the vast and multilingual feedback (27+ languages, 30M+ records), this tool provides crucial insights for planning and improvement.

    ## User Manual

    Administrators can:
    - Perform sentiment analysis
    - Visualize demographic and cross-demographic data
    - Upload data in CSV/Excel or paste text directly

    ---
    ## A. Demographics and Cross-Demographic Analysis

    Accessible from homepage → **Cross-Demographic and Demographic Analysis**

    Double-click to enter.

    Below is what the user sees before entering:
    """)
    show_image("daspic.png", "Cross-Demographic Entry Point")

    st.markdown("""
    Users can load data via:
    - 📂 Upload file
    - 🌐 API URL
    - 📄 Paste raw CSV text

    **Required columns**: `الجنسية Nationality`, `الجنس Gender`, `العمر Age`  
    Missing any of these will result in an error.

    After loading, the dashboard provides:
    - 📊 Age Distribution Stats
    - 📉 Plotly Line Chart
    - 🧍‍♂️ Gender vs Nationality Histogram
    - 🎯 Bubble Plot: Mean Age by Gender/Nationality
    - 🧮 Histogram of Age by Gender and Nationality

    """)
    show_image("Filterpic.png", "Filter Interface")

    st.markdown("""
    To return to home, double-click the **Back to Home** button:
    """)
    show_image("backhome.png", "Back to Home Button on Dashboard")

    st.markdown("""
    ## B. Sentimental and Text Classification Analysis

    Accessed from homepage → **Sentimental and Text Classification Analysis**

    Click once to enter.
    """)
    show_image("sentimentalpic.png", "Text Classification Entry Button")

    st.markdown("""
    Inside this section:
    - Upload CSV, Excel, PDF, TXT, or JSON
    - Paste comments manually
    - Analysis performed using:
        - Google Translator
        - Transformers from HuggingFace
        - Keyword-matching for classification
    """)

    show_image("outputpic.png", "Sample Output Table")

    st.markdown("""
    ---
    ## Technologies Used

    - **Python**, **Streamlit**, **Pandas**
    - **Plotly**, **Matplotlib**, **Seaborn**
    - **Transformers**, **GoogleTranslator**, **pdfplumber**

    ## Future Improvements

    - Real-time sentiment analysis via API
    - Faster large dataset handling
    """)

    if st.button("Back to Home"):
        st.session_state.page = "home"

# --- YOUR EXISTING PAGES ---
def dashboard():
    # Your full dashboard() implementation here...
    st.title("📊 Dashboard Placeholder")
    if st.button("Back to Home"):
        st.session_state.page = "home"

def analyze():
    # Your full analyze() implementation here...
    st.title("🧠 Analyze Placeholder")
    if st.button("Back to Home"):
        st.session_state.page = "home"

# --- ROUTING ---
def main():
    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        home()
    elif st.session_state.page == "dashboard":
        dashboard()
    elif st.session_state.page == "analyze":
        analyze()
    elif st.session_state.page == "documentation":
        documentation()

if __name__ == "__main__":
    main()


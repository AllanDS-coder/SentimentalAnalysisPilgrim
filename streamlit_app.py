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
# --- SETTING UP THE DASHBOARD PAGE ---
#def dashboard():
def dashboard():
    st.title("Cross-Demographic and Demographic Analysis Dashboard")

    # -- Load image
    img_b64 = get_base64("analysis.png")

    # -- USE THE HTML AND CSS TO ADD IMAGES AND TEXT OVERLAY 
    st.markdown(f"""
    <style>
      .custom-container {{
        background: url("data:image/png;base64,{img_b64}") no-repeat center;
        background-size: cover;
        padding: 2rem;
        border-radius: 1rem;
        max-width: 900px;
        margin: 2rem auto;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        background-attachment: local;
        color: #000;
        font-family: 'Segoe UI', sans-serif;
      }}
      .custom-container h2 {{
        color: #DAA520;
        text-align: center;
        margin-bottom: 1rem;
      }}
      .custom-container p,
      .custom-container ul {{
        background-color: rgba(255, 255, 255, 0.85);
        padding: 1rem;
        border-radius: 0.5rem;
      }}
      .custom-container ul {{
        padding-left: 2rem;
      }}
    </style>

    <div class="custom-container">
      <h2>AI-Driven Cross-Demographic and Demographic Insights</h2>
      <p>This AI-powered dashboard delivers comprehensive insights into the demographics of Hajj and Umrah pilgrims.</p>

      <p>Designed to empower pilgrimage authorities, the dashboard provides:</p>

      <ul>
        <li><strong>Age Distribution</strong>: Interactive visualizations illustrating the range and concentration of pilgrims’ ages.</li>
        <li><strong>Statistical Overview</strong>: Key metrics including minimum, maximum, mean, quartiles, and mode of pilgrim ages.</li>
        <li><strong>Nationality & Gender Breakdown</strong>: Detailed analysis of visitor nationalities segmented by gender.</li>
        <li><strong>Cross-Demographic Insights</strong>: Integrated visualizations combining age, gender, and nationality to highlight deeper demographic trends.</li>
      </ul>

      <p>Built using Plotly for an intuitive and engaging user experience, this platform transforms millions of multilingual feedback entries into actionable intelligence to enhance pilgrimage services.</p>
    </div>
    """, unsafe_allow_html=True)

    st_autorefresh(interval=10 * 1000, limit=None, key="datarefresh")


    
    # --- SOURCES OF DATA: DATA INPUT ---
    data_source = st.radio("Load Data Appropriately by Select the right Data Source ", ['Upload File', 'Enter API URL', 'Paste Raw Text'])

    dataset = None
    if data_source == 'Upload File':
        uploaded_file = st.file_uploader("Upload your data file", type=['csv', 'xlsx', 'xls', 'ods', 'txt', 'pdf'])
        if uploaded_file is not None:
            file_type = uploaded_file.name.split('.')[-1].lower()
            try:
                if file_type in ['csv', 'txt']:
                    dataset = pd.read_csv(uploaded_file, encoding='utf-8', errors='replace')
                elif file_type in ['xls', 'xlsx', 'ods']:
                    dataset = pd.read_excel(uploaded_file)
                elif file_type == 'pdf':
                    st.error("PDF files are currently not supported for data upload. Please upload CSV or Excel files.")
                else:
                    st.error(f"Unsupported file type: {file_type}")
            except Exception as e:
                st.error(f"Error reading file: {e}")

    elif data_source == 'Enter API URL':
        api_url = st.text_input("Enter API URL returning data")
        if api_url:
            try:
                response = requests.get(api_url)
                response.raise_for_status()
                dataset = pd.read_csv(StringIO(response.text))
            except Exception as e:
                st.error(f"Failed to fetch data from API: {e}")
    elif data_source == 'Paste Raw Text':
        raw_csv = st.text_area("Paste your text data here")
        if raw_csv:
            try:
                dataset = pd.read_csv(StringIO(raw_csv))
            except Exception as e:
                st.error(f"Failed to parse CSV text: {e}")
  
    if dataset is None:
        st.info("Please upload or enter data to continue.")
        if st.button("Back to Home"):
            st.session_state.page = "home"
        return


    dataset.columns = dataset.columns.str.strip()
    required_cols = ['العمر Age', 'الجنسية Nationality', 'الجنس Gender']
    if not all(col in dataset.columns for col in required_cols):
        st.error("❌ Required columns not found in uploaded data.")
        if st.button("Back to Home"):
            st.session_state.page = "home"
        return

    # Translate genders
    gender_map = {'أنثى': 'أنثى : Female', 'ذكر': 'ذكر: Male'}
    dataset['Gender_English'] = dataset['الجنس Gender'].map(gender_map)

    # --- ADDING FILTERS TO FILTER DATA ANALYSIS---
    st.markdown("### Filter Data")

    col1, col2, col3 = st.columns(3)

    with col1:
        gender_options = dataset['الجنس Gender'].dropna().unique()
        selected_genders = st.multiselect("Filter by Gender: Female( ذكر) and (ذكر) Male", options=gender_options, default=list(gender_options))

    with col2:
        nationality_options = dataset['الجنسية Nationality'].dropna().unique()
        selected_nationalities = st.multiselect("Filter by Nationality", options=nationality_options, default=list(nationality_options))

    # Detect date column if exists
    date_cols = [c for c in dataset.columns if 'date' in c.lower()]
    date_column = None
    date_range = None

    if date_cols:
        date_column = date_cols[0]
        dataset[date_column] = pd.to_datetime(dataset[date_column], errors='coerce')
        min_date = dataset[date_column].min()
        max_date = dataset[date_column].max()

        with col3:
            date_range = st.date_input(
                "Filter by Date Range",
                [min_date, max_date],
                min_value=min_date,
                max_value=max_date
            )
    else:
        with col3:
            st.write("No date column found for filtering")

    # Apply filters
    filtered_df = dataset[
        dataset['الجنس Gender'].isin(selected_genders) &
        dataset['الجنسية Nationality'].isin(selected_nationalities)
    ]

    if date_column and date_range and len(date_range) == 2:
        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        filtered_df = filtered_df[
            (filtered_df[date_column] >= start_date) &
            (filtered_df[date_column] <= end_date)
        ]

    # --- Preview data ---
    st.markdown("### Data Visualization")
    #st.write(filtered_df.head())

    # ---- 1. Age Distribution Stats (Matplotlib) ----
    df_Age = filtered_df["العمر Age"].value_counts().reset_index()
    df_Age.columns = ['العمر Age', 'count']
    df_Age = df_Age.sort_values('العمر Age')
    df_repeated = df_Age['العمر Age'].repeat(df_Age['count']).astype(float)

    if df_repeated.empty:
        st.warning("No data after applying filters.")
        return

    stats = {
        "max": df_repeated.max(),
        "min": df_repeated.min(),
        "q1": df_repeated.quantile(0.25),
        "median": df_repeated.median(),
        "q3": df_repeated.quantile(0.75),
        "std": df_repeated.std(),
        "mean": df_repeated.mean(),
        "mode": df_repeated.mode().iloc[0]
    }

    plt.figure(figsize=(14,6))
    sns.lineplot(data=df_Age, x='العمر Age', y='count', marker="o", color="blue")
    plt.axvline(stats["mean"], color="red", linestyle=":", label=f"Mean: {stats['mean']:.2f}")
    plt.axvline(stats["median"], color="orange", linestyle="-", label=f"Median: {stats['median']:.2f}")
    plt.axvline(stats["mode"], color="purple", linestyle="--", label=f"Mode: {stats['mode']:.2f}")
    plt.axvline(stats["q1"], color="green", linestyle="--", label=f"Q1: {stats['q1']:.2f}")
    plt.axvline(stats["q3"], color="green", linestyle="--", label=f"Q3: {stats['q3']:.2f}")
    plt.xlabel("Age")
    plt.ylabel("Count")
    plt.title("Age Distribution with Statistical Markers")
    plt.legend()
    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.clf()

    st.markdown("---")  # separator

    # ---- 2. Plotly Line Chart of Age Distribution ----
    fig_age_dist = px.line(df_Age, x='العمر Age', y='count', markers=True,
        title="Age Distribution", labels={'العمر Age': "Age", 'count': "Count"})
    fig_age_dist.update_layout(template="plotly_dark", height=450)
    st.plotly_chart(fig_age_dist, use_container_width=True)

    st.markdown("---")

    # ---- 3. Nationality by Gender (with bilingual gender labels) ----
    fig_hist = px.histogram(
        filtered_df, x='الجنسية Nationality', color='Gender_English',
        barmode="group",
        title="DEMOGRAPHICS OF NATIONALITY BY GENDER",
        labels={'Gender_English': "Gender", 'الجنسية Nationality': "Nationality"}
    )
    fig_hist.update_layout(template="plotly_white", height=450)
    st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("---")

    # ---- 4. Bubble Chart: Nationality & Gender by Mean Age ----
    agg = filtered_df.groupby(['الجنسية Nationality', 'Gender_English']).agg(
        count=('العمر Age', 'count'),
        avg_age=('العمر Age', 'mean')).reset_index()
    agg['avg_age'] = agg['avg_age'].round(1)
    fig_bubble = px.scatter(
        agg, x='الجنسية Nationality', y='count', size='avg_age',
        color='الجنسية Nationality', facet_col='Gender_English',
        title="Nationality and Gender by Mean Age", size_max=30,
        labels={'count': 'Count', 'الجنسية Nationality': 'Nationality'}
    )
    fig_bubble.update_layout(template="plotly_dark", height=500)
    st.plotly_chart(fig_bubble, use_container_width=True)

    st.markdown("---")

    # ---- 5. Full Demographics (Age, Gender, Nationality) ----
    fig_demo = px.histogram(
        filtered_df, x='العمر Age', color='الجنسية Nationality', facet_col='Gender_English',
        barmode="overlay", title="Demographic Characteristics: Age, Gender, Nationality"
    )
    fig_demo.update_layout(template="ggplot2", height=500)
    st.plotly_chart(fig_demo, use_container_width=True)

    st.markdown("---")

    if st.button("Back to Home"):
        st.session_state.page = "home"


# -- ROUTING TO THE MAIN APP
def main():
    if 'page' not in st.session_state:
        st.session_state.page = "home"
    if st.session_state.page == "home":
        home()
    elif st.session_state.page == "dashboard":
        dashboard()

# --- ANALYZE COMMENTS PAGE ---
def analyze():
    add_bg_from_local("background.png")
    st.title("Text Classification and Sentimental Analysis")

    if st.button("Back to Home"):
        st.session_state.page = "home"
        return

    themes_topics = {
        "Transport & Travel": ["bus", "car", "road", "roads", "transport", "transportation", "ride", "route", "driver",
                           "passengers", "commute", "shuttles", "travelling", "departed", "departure", "arrivals",
                           "mobility", "scheduled", "delays", "punctuality", "traffic", "jam", "stops", "rerouted",
                           "infrastructure", "transitions", "retarded", "crowding", "station", "vehicle", "vehicles",
                           "moved", "traveling", "transported", "drivers", "bypass", "walking", "walk", "passenger",
                           "landing", "tracks", "journey", "logistics", "ride", "international", "flights", "flight",
                           "maps", "schedule", "timeline", "clock", "delay", "hurry", "missed", "operations", "travel",
                           "update", "coordination", "timeliness", "planning", "rapid", "stuck", "maps", "taxi", "train",
                           "transporting", "transit", "arrivals", "departures", "schedules", "delays", "rides", "fleet",
                           "highway", "traffic", "transfers", "routes", "passengers", "transportation", "waiting",
                           "luggage", "flights"],
        
        "Accommodation & Facilities": ["accommodation", "facilities", "residences", "housing", "hotels", "hoteling", "rooms",
                                   "house", "homes", "sites", "locations", "residential", "setup", "availability", "space",
                                   "relaxing", "furniture", "utilities", "amenities", "bed", "bedding", "bedroom", "interior",
                                   "carpets", "floor", "equipment", "units", "spacious", "open", "quarters", "water",
                                   "electricity", "surfaces", "ventilation", "pillows", "lobby", "cleanliness", "air conditioning",
                                   "sanitation", "center", "laundry", "sinks", "bathroom", "bathrooms", "baths", "office",
                                   "built", "swimming", "stable", "shower", "resort", "pools", "lodging", "parking", "belongings",
                                   "wall", "windows", "door", "resort", "pool", "usability", "station", "rooms", "linen", "mattress",
                                   "pillows", "beds", "lighting", "air conditioning", "elevator", "washroom", "toiletries", "shampoo",
                                   "soap", "towels", "minibar", "decor", "furniture", "chairs", "tables", "tiles", "carpets", "wallpaper",
                                   "upholstery", "amenities", "signage", "reception", "lobby", "soundproofing", "layout"],
        
        "Hotel Room Conditions & Cleanliness": ["room", "rooms", "cleanliness", "housekeeping", "tidy", "stains", "stained", "unclean",
                                            "dirt", "dusty", "smell", "odor", "bathrooms", "toilet", "bathroom", "bedding", "bed",
                                            "washed", "hygiene", "hygienic", "towels", "garbage", "neat", "windows", "sheets", "cleaning",
                                            "maintained", "spider", "insects", "bath", "pillows", "cleaning", "air", "smell", "ventilation",
                                            "broken", "damaged", "uncleanliness", "dirty", "poorly", "spider", "shower", "wall", "noise",
                                            "silence", "dust", "stains", "floor", "neatness", "sanitation", "clean", "sanitary", "spotless",
                                            "tidy", "unkempt", "dirty", "mold", "dustbin", "contamination", "sticky", "dust", "pests",
                                            "infestation", "mildew", "upkeep", "cleaning", "washing", "garbage", "stains", "laundry", "odors",
                                            "fresh", "polished", "smelly"],
        
        "Staff Attitude & Support": ["staff", "employees", "officials", "officers", "support", "guided", "guiding", "cooperation",
                                 "cooperative", "teamwork", "kindness", "friendly", "friendliness", "warmth", "patient",
                                 "compassion", "courteous", "respectful", "caring", "communicated", "helpful", "attitude", "sincerity",
                                 "dedication", "behaved", "temperament", "humility", "accountability", "willingness", "listening",
                                 "approachable", "respect", "encouragement", "supporter", "assisted", "treatment", "service", "thankfulness",
                                 "support", "interacting", "greeted", "greetings", "counseling", "devotion", "understanding", "cheerful",
                                 "tact", "assisting", "manners", "helping", "helpfulness", "counselor", "training", "trained", "assistant",
                                 "receptionist", "team", "employee", "assisted", "welcomed", "praised", "communicative", "proactive",
                                 "responsive", "helpfulness", "rude", "friendly", "courteous", "supportive", "professional", "caring",
                                 "empathetic", "approachable", "attentive", "knowledgeable", "honest", "respectful", "welcoming", "cooperative",
                                 "polite", "enthusiastic", "trained", "skilled", "motivated"],
        
        "Service Efficiency & Time Management": ["schedule", "scheduling", "timeliness", "timing", "deadlines", "delay", "delays", "waiting",
                                             "waited", "organizing", "management", "handling", "operation", "workflow", "responsiveness",
                                             "immediate", "quickly", "on-time", "execution", "repetition", "slowness", "inconsistency",
                                             "registration", "flow", "disruptions", "interruptions", "missed", "adherence", "smoothly",
                                             "performed", "delays", "chaos", "confusion", "complicated", "organizing", "implementation",
                                             "process", "processes", "timely", "executed", "managing", "managing", "effectiveness",
                                             "efficiency", "deadline", "responses", "immediate", "quick", "prompt", "timely", "stuck",
                                             "coordination", "updated", "systematically", "performance", "task", "clock", "timetable",
                                             "plan", "response", "immediately", "missed", "stuck", "repeated", "completed", "finishing",
                                             "pauses", "backlog", "punctual", "delay", "wait", "rushed", "slow", "efficient", "organized",
                                             "coordinated", "interrupted", "postponement", "schedule", "timing", "backlog", "queue",
                                             "continuity", "smooth", "speed", "hiccups", "downtime", "troubleshooting", "deployment",
                                             "responsiveness"],
        "Food Quality & Dining": ["food", "foods", "meal", "meals", "dish", "dishes", "taste", "tasty", "delicious", "flavors",
                              "flavor", "freshness", "fresh", "cooked", "cooking", "breakfast", "dinner", "eating", "restaurant",
                              "salty", "hygiene", "hot", "cold", "presentation", "smells", "ingredients", "baked", "portions",
                              "nutrition", "served", "serving", "snack", "drinks", "seafood", "seasoning", "bland", "tasteless",
                              "spicy", "fat", "diet", "dirty", "frozen", "spices", "meat", "eat", "dining", "tables", "menu",
                              "cuisine", "culinary", "served", "served", "spicy", "salty", "oily", "fresh", "stale", "tasty",
                              "appetizing", "dishes", "ingredients", "cuisine", "buffet", "meals", "snacks", "salads", "soups",
                              "sauces", "garnishes", "desserts", "nutrition", "calories", "diet", "vegan", "gluten", "organic",
                              "freshness", "portions"],
        
        "Event & Program Organization": ["event", "events", "organized", "organizing", "program", "organizers", "setup", "planning",
                                     "preparation", "process", "processes", "execution", "implemented", "schedule", "coordination",
                                     "participation", "register", "registration", "sessions", "teamwork", "performance", "administration",
                                     "conducted", "flow", "success", "management", "timeline", "logistics", "initiative", "implementation",
                                     "session", "structure", "systematic", "pre-planned", "agenda", "leadership", "executed",
                                     "contribution", "teams", "completed", "management", "conducted", "briefing", "rounds", "conferences",
                                     "organizational", "coordinated", "managed", "seminars", "involved", "participant", "participants",
                                     "organizations", "cooperation", "session", "structure", "governance", "leadership", "initiative",
                                     "task", "program", "event", "activities", "scheduling", "coordination", "hosting", "managing",
                                     "visitor", "group", "volunteers", "agenda", "briefing", "setup", "interruptions", "flow", "entertainment",
                                     "session", "workshops", "speakers", "timeline", "agenda"], 
        "Customer Service": ["service", "support", "help", "rude", "friendly"],
        "Product Quality": ["defective", "quality", "broken", "excellent"],
        "Delivery": ["late", "delivery", "shipping", "on time"],
        "Billing": ["invoice", "bill", "charged", "refund"],
        "General Services": ["general", "other"]
    }

    primary_pipeline = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english", framework="pt")
    cache = {}

    def translator_dual(text, src="auto", dest="en"):
        if pd.isnull(text): return None, None
        text = str(text).strip()
        if text not in cache:
            try: cache[text] = GoogleTranslator(source=src, target=dest).translate(text)
            except Exception as e: cache[text] = f"Error: {e}"
        return text, cache[text]

    def classify_department(comment):
        tokens = set(comment.lower().split())
        for theme, keywords in themes_topics.items():
            if any(keyword in tokens for keyword in keywords):
                return theme
        return "General Services"

    def analyze_primary_sentiment(comment):
        result = primary_pipeline(comment)[0]
        return result["label"], round(result["score"], 2)

    def extract_comments_in_chunks(file, chunksize=10000):
        filename = file.name.lower()
        if filename.endswith(".pdf"):
            with pdfplumber.open(file) as pdf:
                text = "\n".join(page.extract_text() or "" for page in pdf.pages)
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            yield pd.DataFrame({"Comments": lines})
        elif filename.endswith(".txt"):
            text = file.read().decode("utf-8")
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            yield pd.DataFrame({"Comments": lines})
        elif filename.endswith(".csv"):
            for chunk in pd.read_csv(file, chunksize=chunksize):
                chunk.columns = [col.strip() for col in chunk.columns]
                if "Comments" in chunk.columns:
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

    def process_chunk(chunk):
        chunk[["Original", "Translated"]] = chunk["Comments"].apply(lambda c: pd.Series(translator_dual(c)))
        chunk["Department"] = chunk["Translated"].apply(classify_department)
        chunk[["Primary Sentiment", "Confidence"]] = chunk["Translated"].apply(lambda c: pd.Series(analyze_primary_sentiment(c)))
        return chunk

    uploaded_file = st.file_uploader("📂Upload CSV, Excel, PDF, TXT, or JSON", type=["csv", "xlsx", "pdf", "txt", "json"])
    manual_input = st.text_area("Type or paste/enter comments manually (one per line):", height=200)

    if uploaded_file:
        results = []
        total_rows_estimate = 1_000_000
        progress_bar = st.progress(0)
        rows_processed = 0
        for chunk in extract_comments_in_chunks(uploaded_file):
            if chunk is None: break
            processed = process_chunk(chunk)
            results.append(processed)
            rows_processed += len(processed)
            progress_bar.progress(min(rows_processed / total_rows_estimate, 1.0))
        if results:
            df_results = pd.concat(results, ignore_index=True)
            st.success(f"✅ Completed processing {rows_processed} rows!")
            st.dataframe(df_results.head(1000))
            csv = df_results.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download Results", csv, "primary_model_results.csv", "text/csv")
    elif manual_input.strip():
        lines = [line.strip() for line in manual_input.split("\n") if line.strip()]
        df_manual = pd.DataFrame({"Comments": lines})
        with st.spinner("Analyzing manual input..."):
            df_results = process_chunk(df_manual)
        st.success("✅ Analysis complete!")
        st.dataframe(df_results)
        csv = df_results.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", csv, "manual_primary_results.csv", "text/csv")
    else:
        st.info("📂 Upload a file or enter comments above to get started.")

# --- BACKGROUND CSS FOR ANALYZE PAGE ---
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

def dashboard():
    # Your full dashboard() implementation here...
    st.title("Dashboard Placeholder")
    if st.button("Back to Home"):
        st.session_state.page = "home"

def analyze():
    # Your full analyze() implementation here...
    st.title("Analyze Placeholder")
    if st.button("Back to Home"):
        st.session_state.page = "home"
        
def documentation():
    # Your full analyze() implementation here...
    st.title("Documentation")
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


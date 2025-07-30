import streamlit as st
import base64
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import requests
from io import StringIO
from streamlit_autorefresh import st_autorefresh

# -- Page config
st.set_page_config(page_title="PILGRIMAGE DEMOGRAPHICS DASHBOARD", layout="wide")

# -- Background setup
def get_base64(fp):
    with open(fp, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_b64 = get_base64("pilgrimage.png")

# -- Home Page
def home():
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
      .overlay h1 {{ 
        color: #DAA520; 
        margin-bottom: 0.3rem; 
        text-decoration: underline;
      }}
      .overlay h2 {{ 
        color: #DAA520; 
        margin-bottom: 1rem;
        font-weight: bold;
        font-style: italic;
      }}
      .overlay p {{ color: #333; margin: 0.5rem 0; text-align: justify; }}
      .overlay ul {{ color: #000; margin: 0.5rem 0 0.5rem 1rem; padding-left: 1rem; text-align: left; }}
      .overlay .stButton > button {{
        margin-top: 1.5rem;
        background-color: #fff;
        color: #000;
        padding: 0.75rem 1.5rem;
        border: 2px solid #000;
        border-radius: 0.5rem;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
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
        <li>Provides authorities with data‑driven insights to enhance service quality and pilgrim experience</li>
      </ul>

      <p>By adopting this NLP-powered approach, Hajj and Umrah authorities can make informed decisions, prioritize improvements, and ensure a more fulfilling pilgrimage. This AI turns vast, diverse feedback into actionable insights to enhance the pilgrim experience.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("View Dashboard"):
        st.session_state.page = "dashboard"

# -- Dashboard Page
def dashboard():
    st.title("Real-Time Demographic Dashboard")

    # -- Load image
    img_b64 = get_base64("analysis.png")

    # -- Inject CSS & HTML for image + overlay text
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
      <h2>AI-Powered Demographic Insights</h2>
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


    
    # --- Data input ---
    data_source = st.radio("Select Data Source", ['Upload CSV', 'Enter API URL', 'Paste Raw CSV Text'])

    dataset = None
    if data_source == 'Upload CSV':
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
        api_url = st.text_input("Enter API URL returning CSV data")
        if api_url:
            try:
                response = requests.get(api_url)
                response.raise_for_status()
                dataset = pd.read_csv(StringIO(response.text))
            except Exception as e:
                st.error(f"Failed to fetch data from API: {e}")
    elif data_source == 'Paste Raw CSV Text':
        raw_csv = st.text_area("Paste your CSV text here")
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

    # --- FILTERS ---
    st.markdown("### Filter Data")

    col1, col2, col3 = st.columns(3)

    with col1:
        gender_options = dataset['الجنس Gender'].dropna().unique()
        selected_genders = st.multiselect("Filter by Gender", options=gender_options, default=list(gender_options))

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

    # --- Preview filtered data ---
    st.markdown("### Data Visualization(Filtered)")
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


# -- Main App Routing
def main():
    if 'page' not in st.session_state:
        st.session_state.page = "home"
    if st.session_state.page == "home":
        home()
    elif st.session_state.page == "dashboard":
        dashboard()

if __name__ == "__main__":
    main()

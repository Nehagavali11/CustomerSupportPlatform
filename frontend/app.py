# =============== Frontend  ========================
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Customer Support Dashboard", layout="wide")

# ==================== COLORS ====================
BG_COLOR = "#F5F5F5"
SIDEBAR_BG = "#E8E8E8"
BOT_COLOR = "#003366"       # Dark Blue
USER_COLOR = "#E0E0E0"      # Light gray
TEXT_COLOR = "#0A0909"

# ==================== CUSTOM CSS ====================
st.markdown(
    f"""
    <style>
    /* Page background */
    .stApp {{
        background-color: {BG_COLOR};
        color: {TEXT_COLOR};
    }}
    /* Sidebar background */
    .css-1d391kg {{
        background-color: {SIDEBAR_BG};
        padding: 10px;
        border-radius: 8px;
    }}
    /* Card containers */
    .card {{
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 1px 1px 4px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }}
    /* Custom Get Insights Button */
    div.stButton > button:first-child {{
        background-color: {BOT_COLOR};
        color: white;
        border-radius: 8px;
        padding: 10px 25px;
        font-size: 16px;
        font-weight: bold;
    }}
    div.stButton > button:first-child:hover {{
        opacity: 0.9;
        color: white;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ==================== BASE URL ====================
BASE_URL = "https://customersupportplatform-3.onrender.com/"

# ==================== SIDEBAR ====================
st.sidebar.header("⚙️ Upload & Filters")
file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])
process_clicked = st.sidebar.button("Process Data", key="process_button")

# Backend check
try:
    res = requests.get(BASE_URL)
    st.sidebar.success("✅ Backend Connected")
except:
    st.sidebar.error("❌ Backend NOT running. Start FastAPI first!")
    st.stop()

# ==================== PROCESS DATA ====================
if file is not None and process_clicked:
    with st.spinner("Processing... Please wait ⏳"):
        try:
            response = requests.post(f"{BASE_URL}/upload", files={"file": file})
            st.sidebar.success("✅ Data Processed Successfully!")
        except Exception as e:
            st.sidebar.error(f"❌ Error: {e}")

# ==================== MAIN PAGE ====================
st.title("Customer Support Insight Platform")

# ---------- SESSION STATE ----------
if "insights_clicked" not in st.session_state:
    st.session_state.insights_clicked = False
if "insights_data" not in st.session_state:
    st.session_state.insights_data = {}

# ---------- GET INSIGHTS BUTTON ----------
if st.button("Get Insights"):
    st.session_state.insights_clicked = True
    try:
        res = requests.get(f"{BASE_URL}/insights")
        st.session_state.insights_data = res.json()
    except Exception as e:
        st.error(f"❌ Could not fetch insights: {e}")

# ---------- SHOW INSIGHTS IF CLICKED ----------
if st.session_state.insights_clicked and st.session_state.insights_data:
    data = st.session_state.insights_data

    # ----- KPI METRICS -----
    insights = data.get("insights", {})
    kpi1 = insights.get('total_tickets', 0)
    kpi2 = insights.get('negative_tickets', 0)
    kpi3 = insights.get('most_common_issue', '-')
    kpi4 = insights.get('negative_percentage', 0)

    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    kpi_col1.markdown(f"<div class='card'><h4>Total Tickets</h4><h2>{kpi1}</h2></div>", unsafe_allow_html=True)
    kpi_col2.markdown(f"<div class='card'><h4>Negative Tickets</h4><h2>{kpi2}</h2></div>", unsafe_allow_html=True)
    kpi_col3.markdown(f"<div class='card'><h4>Most Common Issue</h4><h2>{kpi3}</h2></div>", unsafe_allow_html=True)
    kpi_col4.markdown(f"<div class='card'><h4>Negative %</h4><h2>{kpi4}%</h2></div>", unsafe_allow_html=True)

    # ----- CHARTS -----
    chart_col1, chart_col2 = st.columns(2)
    top_categories = data.get("top_categories", {})
    sentiment = data.get("sentiment", {})

    if top_categories:
        df_top = pd.DataFrame(list(top_categories.items()), columns=['Category', 'Count'])
        fig1 = px.bar(df_top, x='Category', y='Count', color='Category', color_discrete_sequence=px.colors.qualitative.Safe)
        fig1.update_layout(plot_bgcolor=BG_COLOR, paper_bgcolor=BG_COLOR)
        chart_col1.plotly_chart(fig1, use_container_width=True)
    else:
        chart_col1.info("No top categories data available")

    if sentiment:
        df_sent = pd.DataFrame(list(sentiment.items()), columns=['Sentiment', 'Count'])
        fig2 = px.pie(df_sent, names='Sentiment', values='Count',
                      color_discrete_sequence=[BOT_COLOR, USER_COLOR, "#FFA500"])
        fig2.update_layout(plot_bgcolor=BG_COLOR, paper_bgcolor=BG_COLOR)
        chart_col2.plotly_chart(fig2, use_container_width=True)
    else:
        chart_col2.info("No sentiment data available")

    # ----- BUSINESS INSIGHTS -----
    st.subheader("Business Insights")
    st.markdown(f"<div class='card'><b>🔥 Most Common Issue: </b> {kpi3}<br>"
                f"<b>😡 Negative Tickets: </b> {kpi2}<br>"
                f"<b>📊 Total Tickets: </b> {kpi1}<br>"
                f"<b>⚠️ Negative %: </b> {kpi4}%</div>", unsafe_allow_html=True)

    # ----- RECOMMENDATION -----
    recommendation = data.get("recommendation", "No recommendation available")
    st.subheader("Recommendation")
    st.markdown(f"<div style='background-color:{BOT_COLOR};color:white;padding:10px;border-radius:8px'>{recommendation}</div>", unsafe_allow_html=True)

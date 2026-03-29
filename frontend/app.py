import streamlit as st
import requests

st.set_page_config(page_title="AI Support Dashboard")

st.title("📊 Customer Support Insight Platform")

BASE_URL = "http://127.0.0.1:8000"

# -------- Backend Check --------
try:
    res = requests.get(BASE_URL)
    st.success("✅ Backend Connected")
except Exception as e:
    st.error("❌ Backend NOT running. Start FastAPI first!")
    st.stop()

# -------- Upload Section --------
st.header("📂 Upload Dataset")

file = st.file_uploader("Upload CSV file", type=["csv"])

if file is not None:
    if st.button("Process Data"):
        with st.spinner("Processing... Please wait ⏳"):
            try:
                response = requests.post(
                    f"{BASE_URL}/upload",
                    files={"file": file}
                )
                st.success("✅ Data Processed Successfully!")
            except Exception as e:
                st.error(f"❌ Error: {e}")

# -------- Insights Section --------
st.header("📊 View Insights")

if st.button("Get Insights"):
    try:
        res = requests.get(f"{BASE_URL}/insights")
        data = res.json()

        # ✅ Charts
        st.subheader("🔥 Top Issues")
        st.bar_chart(data["top_categories"])

        st.subheader("📊 Sentiment Analysis")
        st.bar_chart(data["sentiment"])

        # ✅ Business Insights
        st.subheader("📌 Business Insights")
        insights = data["insights"]

        st.write(f"🔥 Most Common Issue: {insights['most_common_issue']}")
        st.write(f"😡 Negative Tickets: {insights['negative_tickets']}")
        st.write(f"📊 Total Tickets: {insights['total_tickets']}")
        st.write(f"⚠️ Negative %: {insights['negative_percentage']}%")

        # ✅ Recommendation
        st.subheader("💡 Recommendation")
        st.success(data["recommendation"])

    except Exception as e:
        st.error(f"❌ Could not fetch insights: {e}")
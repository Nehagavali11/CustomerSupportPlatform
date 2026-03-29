from fastapi import FastAPI, UploadFile
import pandas as pd
import sqlite3
from fastapi.middleware.cors import CORSMiddleware
from backend.db import insert_ticket

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- HOME --------
@app.get("/")
def home():
    return {"message": "AI Support Insight API Running"}


# -------- SIMPLE FUNCTIONS (NO LLM) --------

def clean_text(text):
    return str(text).lower().strip()

def get_sentiment(text):
    text = text.lower()

    negative_words = ["bad", "worst", "delay", "late", "not", "poor", "damaged", "wrong", "frustrating"]
    positive_words = ["good", "happy", "great"]

    if any(word in text for word in negative_words):
        return "Negative"
    elif any(word in text for word in positive_words):
        return "Positive"
    else:
        return "Neutral"

def categorize_ticket(text):
    text = text.lower()

    if any(word in text for word in ["delivery", "deliver", "delayed"]):
        return "Delivery"
    elif any(word in text for word in ["payment", "pay"]):
        return "Payment"
    elif any(word in text for word in ["refund"]):
        return "Refund"
    elif any(word in text for word in ["product", "item", "quality"]):
        return "Product"
    else:
        return "Other"


# -------- UPLOAD API --------
@app.post("/upload")
async def upload(file: UploadFile):
    df = pd.read_csv(file.file)

    df = df.head(20)

    text_column = "text"

    # 🔥 CLEAR OLD DATA (IMPORTANT)
    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tickets")
    conn.commit()

    for _, row in df.iterrows():
        text = clean_text(row[text_column])

        sentiment = get_sentiment(text)
        category = categorize_ticket(text)

        reply = "We will resolve your issue soon."

        insert_ticket(text, category, sentiment, reply)

    return {"status": "Processed Successfully"}


# -------- RECOMMENDATION --------
def generate_business_recommendation(top_issue):
    if top_issue == "Delivery":
        return "Improve delivery system."
    elif top_issue == "Payment":
        return "Fix payment issues."
    elif top_issue == "Product":
        return "Improve product quality."
    elif top_issue == "Refund":
        return "Speed up refund process."
    else:
        return "Check customer complaints manually."


# -------- INSIGHTS API --------
@app.get("/insights")
def insights():
    conn = sqlite3.connect("tickets.db")
    df = pd.read_sql("SELECT * FROM tickets", conn)

    if df.empty:
        return {"message": "No data available"}

    top_categories = df['category'].value_counts()
    sentiment = df['sentiment'].value_counts()

    top_category = top_categories.idxmax()
    negative_count = len(df[df['sentiment'] == "Negative"])

    return {
        "top_categories": top_categories.to_dict(),
        "sentiment": sentiment.to_dict(),

        "insights": {
            "most_common_issue": top_category,
            "negative_tickets": negative_count,
            "total_tickets": len(df),
            "negative_percentage": round((negative_count / len(df)) * 100, 2)
        },

        "recommendation": generate_business_recommendation(top_category)
    }
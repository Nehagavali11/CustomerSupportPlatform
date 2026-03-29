import sqlite3

conn = sqlite3.connect("tickets.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT,
    category TEXT,
    sentiment TEXT,
    reply TEXT
)
""")

# ✅ THIS FUNCTION MUST EXIST
def insert_ticket(message, category, sentiment, reply):
    cursor.execute("""
    INSERT INTO tickets (message, category, sentiment, reply)
    VALUES (?, ?, ?, ?)
    """, (message, category, sentiment, reply))
    conn.commit()
AI Customer Support Insight Platform

An AI-powered dashboard that analyzes customer support tickets using rule-based NLP to generate actionable insights and recommendations. Built with FastAPI (backend) and Streamlit (frontend).

🔗 Live App 
https://custinsight.streamlit.app

🚀 Features
Upload CSV of customer tickets
Automatic categorization & sentiment analysis
Interactive dashboard with:
Total tickets & negative tickets
Most common issues
Negative percentage
Charts for top issues & sentiment distribution
Actionable recommendations for business improvement
Lightweight, no heavy ML or LLM required

🏗️ Architecture

<img width="2526" height="2268" alt="Need_ - visual selection (1)" src="https://github.com/user-attachments/assets/cc291fe8-0ea3-4a46-aca1-ccb402ce76fc" />


🎨 Screenshots

<img width="1920" height="866" alt="Screenshot (815)" src="https://github.com/user-attachments/assets/f83e8f34-3a2a-4157-b953-088f60535c73" />


<img width="1920" height="865" alt="Screenshot (816)" src="https://github.com/user-attachments/assets/33b818a0-a949-423e-8811-212382dfb6e2" />


⚙️ Installation
git clone <repo-url>
cd customer-support-insight
python -m venv venv
# Activate environment
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
pip install -r requirements.txt

# Start backend
uvicorn backend.main:app --reload

# Start frontend
streamlit run frontend/frontend.py

📊 Business Insights
Identify top customer issues quickly
Track negative sentiment percentages
Prioritize problem areas for faster resolution
Improve customer satisfaction & retention

⚖️ Limitations
Rule-based NLP → may miss complex patterns
SQLite → suitable for small datasets, not enterprise scale
Can be extended with ML/LLM and multilingual support

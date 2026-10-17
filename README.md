# 📊 Market Intelligence & Competitor Scraping Tool

An end-to-end Python web application designed for product teams, data engineers, and founders to discover mobile app competitors on the Google Play Store, scrape customer reviews, perform sentiment analysis, store relational data locally, and leverage **Google Gemini AI** to uncover critical market gaps and strategic product insights.

---

## 🚀 Core Features

1. **Dynamic App Discovery:** Search the Google Play Store by niche keyword or category and instantly view matching apps with ratings, developers, and icons.
2. **Targeted Scraping & Pagination:** Select 2 to 4 competitor apps and securely extract recent customer reviews (150–300 reviews per app) without memory bottlenecks or rate-limit crashes.
3. **Data Pipeline & SQLite Storage:** Clean and normalize text data, categorize sentiments (Positive, Neutral, Negative), and persist records in a lightweight relational SQLite database.
4. **AI-Powered Market Gap Analysis:** Feed competitor 1-star and 2-star pain points directly into **Google Gemini API** to generate an executive-level report covering:
   - Top recurring bugs and complaints.
   - Missing features users are demanding.
   - Strategic product recommendations for your upcoming app.
5. **Interactive Streamlit Dashboard:** A user-friendly web interface featuring visual charts (Plotly), exportable multi-sheet Excel reports (`openpyxl`), and seamless AI integration.

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Web Framework & UI:** Streamlit, Plotly
- **Scraping:** `google-play-scraper`
- **Data Processing & Export:** Pandas, OpenPyXL
- **Database:** SQLite3
- **AI Integration:** Google GenAI SDK (`google-genai` / Gemini 2.5 Flash)

---

├── requirements.txt        # Project dependencies
└── README.md               # Project Documentation

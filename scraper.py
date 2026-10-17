import sqlite3
import pandas as pd
from google_play_scraper import search, reviews, Sort
import openpyxl

# 1. تهيئة قاعدة البيانات SQLite
def init_db(db_path="market_intelligence.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_id TEXT,
            app_name TEXT,
            review_text TEXT,
            score INTEGER,
            sentiment TEXT,
            at DATETIME
        )
    ''')
    conn.commit()
    conn.close()

# 2. البحث عن التطبيقات
def search_google_play(keyword, n_hits=10):
    results = search(keyword, lang="en", country="us",  n_hits=n_hits)
    apps = []
    try:
        for app in results:
            apps.append({
                "appId": app.get("appId"),
                "title": app.get("title"),
                "developer": app.get("developer"),
                "score": round(app.get("score", 0), 2),
                "icon": app.get("icon")
            })
        return apps
    except Exception as e:
        print(f"حدث خطأ أثناء البحث: {e}")
        return [] # إرجاع قائمة فارغة بدلاً من إيقاف البرنامج    

# 3. سحب وتنظيف التقييمات وتصنيف المشاعر
def scrape_and_process_reviews(selected_apps, reviews_count=200, db_path="market_intelligence.db"):
    all_processed_reviews = []
    
    conn = sqlite3.connect(db_path)
    
    for app in selected_apps:
        app_id = app['appId']
        app_name = app['title']
        
        result, _ = reviews(
            app_id,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=reviews_count
        )
        
        for r in result:
            text = r.get('content', '').strip()
            score = r.get('score', 0)
            
            # Sentiment Segmentation
            if score >= 4:
                sentiment = 'Positive'
            elif score == 3:
                sentiment = 'Neutral'
            else:
                sentiment = 'Negative'
                
            review_data = {
                'app_id': app_id,
                'app_name': app_name,
                'review_text': text,
                'score': score,
                'sentiment': sentiment,
                'at': r.get('at')
            }
            all_processed_reviews.append(review_data)
            
    df = pd.DataFrame(all_processed_reviews)
    
    # حفظ البيانات في SQLite
    df.to_sql('reviews', conn, if_exists='replace', index=False)
    conn.close()
    
    return df

# 4. توليد تقرير Excel متعدد الأوراق
def export_excel_report(df, filename="Competitor_Analysis_Report.xlsx"):
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # ورقة الملخص
        summary = df.groupby(['app_name', 'sentiment']).size().unstack(fill_value=0)
        summary.to_excel(writer, sheet_name='Summary')
        
        # ورقة المراجعات الكاملة
        df.to_excel(writer, sheet_name='All Reviews', index=False)
        
        # ورقة الشكاوى والسلبية فقط
        negative_df = df[df['score'] <= 2]
        negative_df.to_excel(writer, sheet_name='Pain Points (1-2 Stars)', index=False)
    return filename
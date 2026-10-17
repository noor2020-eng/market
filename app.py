import streamlit as st
import pandas as pd
import plotly.express as px
from scraper import init_db, search_google_play, scrape_and_process_reviews, export_excel_report
from ai_analyzer import generate_market_gap_analysis

# إعدادات الصفحة
st.set_page_config(page_title="Market Intelligence Tool", layout="wide", page_icon="📊")

# تهيئة قاعدة البيانات
init_db()

st.title("📊 Google Play Market Intelligence & Competitor Scraping Tool")
st.write("ابحث عن المنافسين، قارن تقييماتهم، واستخرج الثغرات في السوق باستخدام الذكاء الاصطناعي.")

# الشريط الجانبي لمفتاح API
st.sidebar.header("🔑 إعدادات Gemini API")
api_key = st.sidebar.text_input("أدخل Google Gemini API Key:", type="password")

# الخطوة 1: البحث عن التطبيقات

st.header("1. 🔍 البحث عن التطبيقات المنافسة")
keyword = st.text_input("أدخل الكلمة المفتاحية أو اسم النيش (مثال: food delivery, fitness tracker):", "")

if st.button("بحث في Google Play") and keyword:
    with st.spinner("جاري البحث..."):
        st.session_state['search_results'] = search_google_play(keyword)

if 'search_results' in st.session_state:
    apps = st.session_state['search_results']
    
    st.subheader("اختر من 2 إلى 4 تطبيقات للمقارنة:")
    selected_app_ids = []
    
    cols = st.columns(min(len(apps), 4))
    for idx, app in enumerate(apps):
        col = cols[idx % 4]
        with col:
            st.image(app['icon'], width=64)
            st.write(f"**{app['title']}**")
            st.write(f"⭐ {app['score']} | {app['developer']}")
            if st.checkbox("تحديد", key=app['appId']):
                selected_app_ids.append(app['appId'])
                
    st.session_state['selected_apps'] = [a for a in apps if a['appId'] in selected_app_ids]

# الخطوة 2: السحب والتحليل
if 'selected_apps' in st.session_state and len(st.session_state['selected_apps']) >= 2:
    selected_apps = st.session_state['selected_apps']
    st.success(f"تم تحديد {len(selected_apps)} تطبيقات.")
    
    reviews_count = st.slider("عدد التقييمات لكل تطبيق:", min_value=100, max_value=300, value=150, step=50)
    
    if st.button("🚀 البدء بسحب البيانات وتحليل المشاعر"):
        with st.spinner("جاري سحب التقييمات وتنظيف البيانات..."):
            df_reviews = scrape_and_process_reviews(selected_apps, reviews_count)
            st.session_state['df_reviews'] = df_reviews
            st.success("تم سحب البيانات وتخزينها بنجاح في SQLite!")

# الخطوة 3: عرض البيانات والرسوم البيانية
if 'df_reviews' in st.session_state:
    df = st.session_state['df_reviews']
    
    st.header("2. 📈 المقارنة والتحليل ")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("توزيع التقيمات حسب التطبيق")
        fig = px.histogram(df, x="app_name", color="sentiment", barmode="group",
                           color_discrete_map={'Positive':'#2ecc71', 'Neutral':'#f1c40f', 'Negative':'#e74c3c'})
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("متوسط درجات النجوم")
        avg_scores = df.groupby('app_name')['score'].mean().reset_index()
        fig_bar = px.bar(avg_scores, x='app_name', y='score', color='score', range_y=[0, 5])
        st.plotly_chart(fig_bar, use_container_width=True)
        
    # تصدير التقرير إلى Excel
    excel_file = export_excel_report(df)
    with open(excel_file, "rb") as file:
        st.download_button(
            label="📥 تحميل تقرير Excel الشامل (Multi-sheet)",
            data=file,
            file_name="Competitor_Market_Intelligence.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    # الخطوة 4: تحليل ثغرات السوق بـ Gemini API
    st.header("3. 🧠 تحليل الثغرات وتوصيات الذكاء الاصطناعي")
    if st.button("استخراج تحليل AI لمشاكل المنافسين"):
        if not api_key:
            st.error("يرجى إدخال Gemini API Key في الشريط الجانبي أولاً.")
        else:
            with st.spinner("جاري تحليل التقييمات السلبية (1-2 نجوم) عبر Gemini..."):
                df_negative = df[df['score'] <= 2]
                analysis = generate_market_gap_analysis(df_negative, api_key)
                st.markdown(analysis)
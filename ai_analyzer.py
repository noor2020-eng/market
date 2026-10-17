import os
from google import genai

def generate_market_gap_analysis(df_negative, api_key):
    """
    يستقبل التقييمات السلبية (1-2 نجوم) ويحللها عبر Gemini API
    """
    client = genai.Client(api_key=api_key)
    # تحضير نص الشكاوى للمطالبة (Prompt)
    sample_reviews = ""
    for app_name, group in df_negative.groupby('app_name'):
        sample_reviews += f"\n--- Competitor: {app_name} ---\n"
        reviews_list = group['review_text'].head(40).tolist()
        sample_reviews += "\n".join([f"- {rev}" for rev in reviews_list])
        
    prompt = f"""
    You are an expert Product Manager and Market Intelligence Specialist.
    Analyze the following 1-star and 2-star customer reviews from our top mobile app competitors:

    {sample_reviews}

    Please produce a concise, executive-level Market Gap Report in Markdown with the following sections:
    1. **Top Recurring Bugs & Complaints**: What breaks or frustrates users the most?
    2. **Missing & Highly Requested Features**: What are users explicitly begging for that competitors lack?
    3. **Strategic Product Recommendations**: Actionable advice on how our upcoming app can win these users over.
    """
    
    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=prompt
    )
    
    return response.text


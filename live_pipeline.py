import os
import feedparser
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client
from transformers import pipeline

# 1. Securely load credentials and connect to database
load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# 2. Initialize FinBERT
# (Note: This will download a ~400MB model file to your Codespace on the first run!)
print("🧠 Loading FinBERT NLP Model (this takes a moment on the first run)...")
sentiment_analyzer = pipeline("sentiment-analysis", model="ProsusAI/finbert")

def fetch_score_and_store():
    print("📡 Fetching live financial news from Yahoo Finance...\n")
    rss_url = "https://finance.yahoo.com/news/rss"
    feed = feedparser.parse(rss_url)
    
    new_articles_count = 0
    
    for entry in feed.entries:
        headline = entry.title
        
        try:
            pub_date = datetime(*entry.published_parsed[:6]).isoformat()
        except Exception:
            pub_date = datetime.now().isoformat() 
            
        # 3. Score the headline with FinBERT
        # Returns a dictionary like: {'label': 'positive', 'score': 0.85}
        nlp_result = sentiment_analyzer(headline)[0]
        label = nlp_result['label']  
        score = nlp_result['score']  
        
        # 4. Prepare the row data with the new sentiment metrics
        row_data = {
            "published_at": pub_date,
            "headline": headline,
            "sentiment_label": label,
            "sentiment_score": round(score, 4) # Round to 4 decimal places
        }
        
        try:
            supabase.table("live_news_sentiment").insert(row_data).execute()
            new_articles_count += 1
            
            # Add a visual indicator for the terminal output
            emoji = "🟢" if label == "positive" else "🔴" if label == "negative" else "⚪"
            print(f"{emoji} [{label.upper()} {score:.2f}] Inserted: {headline[:55]}...")
            
        except Exception as e:
            # Duplicate entry caught by UNIQUE constraint
            pass
            
    print(f"\n🚀 Pipeline run complete! Scored and added {new_articles_count} new articles.")

if __name__ == "__main__":
    fetch_score_and_store()
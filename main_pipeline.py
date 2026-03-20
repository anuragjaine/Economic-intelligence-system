import time
from datetime import datetime
from live_pipeline import fetch_score_and_store
from market_macro_scraper import fetch_market_data, fetch_macro_data

def run_heartbeat():
    print(f"🫀 Starting the Economic Intelligence Heartbeat at {datetime.now().strftime('%H:%M:%S')}...\n")
    
    while True:
        print("==================================================")
        print(f"🔄 NEW CYCLE STARTING: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("==================================================")
        
        # 1. Fetch, Score, and Store Financial News
        try:
            fetch_score_and_store()
        except Exception as e:
            print(f"⚠️ Error in News Scraper: {e}")
            
        # 2. Fetch Latest Market Prices
        try:
            fetch_market_data()
        except Exception as e:
            print(f"⚠️ Error in Market Scraper: {e}")
            
        # 3. Fetch Macroeconomic Indicators
        try:
            fetch_macro_data()
        except Exception as e:
            print(f"⚠️ Error in Macro Scraper: {e}")
            
        print("\n✅ CYCLE COMPLETE.")
        print("⏸️ Sleeping for 15 minutes before the next pull...\n")
        
        # Pause the script for 900 seconds (15 minutes)
        time.sleep(900) 

if __name__ == "__main__":
    # If you run this file, it will loop forever until you manually stop it
    run_heartbeat()
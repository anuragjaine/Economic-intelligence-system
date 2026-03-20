import os
import yfinance as yf
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client
from fredapi import Fred

# 1. Securely load credentials
load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
fred_key = os.environ.get("FRED_API_KEY")

supabase: Client = create_client(url, key)
fred = Fred(api_key=fred_key)

def fetch_market_data():
    print("📈 Fetching daily market data (S&P 500, Nifty 50, VIX)...")
    try:
        # Fetch the last available closing price
        sp500 = yf.Ticker("^GSPC").history(period="1d")['Close'].iloc[-1]
        nifty = yf.Ticker("^NSEI").history(period="1d")['Close'].iloc[-1]
        vix = yf.Ticker("^VIX").history(period="1d")['Close'].iloc[-1]
        
        row_data = {
            "timestamp": datetime.now().isoformat(),
            "sp500_close": float(round(sp500, 2)),
            "nifty50_close": float(round(nifty, 2)),
            "vix_close": float(round(vix, 2))
        }
        
        supabase.table("market_data").insert(row_data).execute()
        print(f"✅ Market data inserted successfully!")
    except Exception as e:
        print(f"❌ Error fetching market data: {e}")

def fetch_macro_data():
    print("\n🏛️ Fetching macroeconomic data from FRED...")
    try:
        # Fetch the most recent data point for each indicator
        cpi = fred.get_series('CPIAUCSL').iloc[-1]
        unemp = fred.get_series('UNRATE').iloc[-1]
        fed_funds = fred.get_series('FEDFUNDS').iloc[-1]
        yield_spread = fred.get_series('T10Y2Y').iloc[-1]
        
        row_data = {
            "release_date": datetime.now().isoformat(),
            "cpi_yoy": float(cpi),
            "unemployment_rate": float(unemp),
            "fed_funds_rate": float(fed_funds),
            "yield_spread_10y_2y": float(yield_spread)
        }
        
        supabase.table("macro_data").insert(row_data).execute()
        print(f"✅ Macro data inserted: Unemp={unemp}%, Fed Funds={fed_funds}%")
    except Exception as e:
        print(f"❌ Error fetching macro data: {e}")

if __name__ == "__main__":
    fetch_market_data()
    fetch_macro_data()
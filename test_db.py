import os
from dotenv import load_dotenv
from supabase import create_client, Client

# 1. Load the hidden credentials from your .env file
load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

# 2. Attempt to connect to the cloud database
try:
    supabase: Client = create_client(url, key)
    
    # 3. Ping the macro_data table to see if it responds
    response = supabase.table("macro_data").select("*").limit(1).execute()
    
    print("\n✅ SUCCESS! Your Codespace is securely connected to your Supabase database.")
    print("Ready to start streaming live data.\n")
    
except Exception as e:
    print(f"\n❌ CONNECTION FAILED: {e}\n")
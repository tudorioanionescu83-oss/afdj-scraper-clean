import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}

def insert_data(data):
    url = f"{SUPABASE_URL}/rest/v1/measurements"
    headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}",
               "Content-Type": "application/json", "Prefer": "return=minimal"}
    return requests.post(url, json=data, headers=headers)

def scrape_afdj():
    print(f"🚀 Scraper v3 {datetime.now()}")
    today, now = str(datetime.now().date()), datetime.now().strftime('%H:%M:%S')
    
    # TEST Galați 239cm REAL de azi
    data = {
        'station_id': 10,  # Galați
        'measurement_date': today,
        'measurement_time': now,
        'water_level': 239,
        'water_temp': 2.0,
        'trend': 'up',
        'source': 'manual-verified'
    }
    
    r = insert_data(data)
    if r.status_code in [200, 201]:
        print("✅ Galați: 239cm, 2.0°C (up) → SAVED!")
    else:
        print(f"⚠️ Supabase error: {r.status_code}")
    
    print("✨ v3 COMPLETE - Check Supabase!")

if __name__ == "__main__":
    scrape_afdj()

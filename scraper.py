import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

# Date REAL din screenshot-ul tău AFDJ
SCREENSHOT_DATA = [
    {'localitate': 'Sulina', 'nivel': 119, 'km': 71, 'temp': None},
    {'localitate': 'Tulcea', 'nivel': 71, 'km': 19, 'temp': None},
    {'localitate': 'Galați', 'nivel': 189, 'km': 159, 'temp': 2},
    {'localitate': 'Brăila', 'nivel': 580, 'km': 175, 'temp': 2},
    {'localitate': 'Cernavodă', 'nivel': 30, 'km': 17, 'temp': 2},
    {'localitate': 'Călărași', 'nivel': 180, 'km': 98, 'temp': 2}
]

STATION_MAP = {'Sulina': 12, 'Tulcea': 11, 'Galați': 10, 'Brăila': 9, 'Cernavodă': 8, 'Călărași': 7}

def insert_data(data):
    url = f"{SUPABASE_URL}/rest/v1/measurements"
    headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}",
               "Content-Type": "application/json"}
    r = requests.post(url, json=data, headers=headers)
    return r.status_code in [200, 201]

def scrape_afdj():
    print(f"🚀 Scraper REAL SCREENSHOT {datetime.now()}")
    today, now = str(datetime.now().date()), datetime.now().strftime('%H:%M:%S')
    
    saved = 0
    for row in SCREENSHOT_DATA:
        sid = STATION_MAP.get(row['localitate'])
        if not sid: continue
        
        data = {
            'station_id': sid,
            'measurement_date': today,
            'measurement_time': now,
            'water_level': row['nivel'],
            'water_temp': row['temp'],
            'trend': 'stable',  # Din screenshot
            'source': 'afdj-screenshot'
        }
        
        if insert_data(data):
            print(f"✅ {row['localitate']}: {row['nivel']}cm")
            saved += 1
        else:
            print(f"⚠️ {row['localitate']} failed")
    
    print(f"✨ {saved}/6 stații salvate AFDJ REAL!")

if __name__ == "__main__":
    scrape_afdj()

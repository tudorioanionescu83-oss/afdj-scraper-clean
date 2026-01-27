# scraper.py - FIX 403 + Headers + Site alternativ
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

# URL principal + backup
AFDJ_URL = "https://afdj.ro/ro/cotele-dunarii"
BACKUP_URL = "https://www.cotele-dunarii.ro/Galati"

STATION_MAP = {
    'Orșova': 1, 'Drobeta Turnu Severin': 2, 'Calafat': 3, 'Zimnicea': 4,
    'Giurgiu': 5, 'Oltenița': 6, 'Călărași': 7, 'Cernavodă': 8,
    'Brăila': 9, 'Galați': 10, 'Tulcea': 11, 'Sulina': 12
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def insert_data(data):
    url = f"{SUPABASE_URL}/rest/v1/measurements"
    headers = {
        "apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json", "Prefer": "return=minimal"
    }
    return requests.post(url, json=data, headers=headers)

def scrape_afdj():
    print(f"🚀 AFDJ Scraper v2.0 {datetime.now()}")
    
    urls = [AFDJ_URL, BACKUP_URL]
    today, now = str(datetime.now().date()), datetime.now().time().strftime('%H:%M:%S')
    
    for url in urls:
        try:
            print(f"📡 Trying {url}")
            resp = requests.get(url, timeout=30, headers=HEADERS)
            print(f"📊 Status: {resp.status_code}")
            
            if resp.status_code != 200:
                print(f"❌ Skip {url}")
                continue
            
            soup = BeautifulSoup(resp.content, 'html.parser')
            table = soup.find('table')
            
            if not table:
                print(f"❌ No table in {url}")
                continue
            
            rows = table.find_all('tr')[1:]  # Skip header
            
            count = 0
            for row in rows:
                cols = row.find_all(['td', 'th'])
                if len(cols) < 5: continue
                
                localitate = cols[0].get_text(strip=True)
                if localitate not in STATION_MAP: continue
                
                nivel_str = cols[2].get_text(strip=True)
                nivel = int(nivel_str) if nivel_str.isdigit() else None
                
                temp_str = cols[4].get_text(strip=True) if len(cols) > 4 else ""
                temp = float(temp_str) if temp_str.replace('.', '').replace(',', '').isdigit() else None
                
                variatie_str = cols[3].get_text(strip=True)
                trend = 'stable'
                if '+' in variatie_str or '↑' in variatie_str: trend = 'up'
                elif '-' in variatie_str or '↓' in variatie_str: trend = 'down'
                
                data = {
                    'station_id': STATION_MAP[localitate],
                    'measurement_date': today,
                    'measurement_time': now,
                    'water_level': nivel,
                    'water_temp': temp,
                    'trend': trend,
                    'source': url
                }
                
                r = insert_data(data)
                status = "✅" if r.status_code in [200, 201] else "⚠️"
                print(f"{status} {localitate}: {nivel}cm {temp}°C ({trend})")
                count += 1
            
            if count > 0:
                print(f"✨ SUCCESS {count} stations from {url}")
                return  # Succes, oprește
            
        except Exception as e:
            print(f"❌ Error {url}: {e}")
            continue
    
    print("❌ All URLs failed")

if __name__ == "__main__":
    scrape_afdj()

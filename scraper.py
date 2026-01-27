import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

AFDJ_URL = "https://afdj.ro/ro/cotele-dunarii"

STATION_MAP = {
    'Orșova': 1, 'Drobeta Turnu Severin': 2, 'Calafat': 3, 'Zimnicea': 4,
    'Giurgiu': 5, 'Oltenița': 6, 'Călărași': 7, 'Cernavodă': 8,
    'Brăila': 9, 'Galați': 10, 'Tulcea': 11, 'Sulina': 12
}

def insert_data(data):
    url = f"{SUPABASE_URL}/rest/v1/measurements"
    headers = {
        "apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json", "Prefer": "return=minimal"
    }
    return requests.post(url, json=data, headers=headers)

def scrape_afdj():
    print(f"🚀 AFDJ scraper {datetime.now()}")
    try:
        resp = requests.get(AFDJ_URL, timeout=30)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, 'html.parser')
        table = soup.find('table')
        if not table: print("❌ No table"); return
        
        rows = table.find_all('tr')[1:]
        today, now = str(datetime.now().date()), datetime.now().time().strftime('%H:%M:%S')
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 5: continue
            loc = cols[0].text.strip()
            if loc not in STATION_MAP: continue
            
            nivel = int(cols[2].text.strip()) if cols[2].text.strip().isdigit() else None
            temp = float(cols[4].text.strip()) if cols[4].text.strip() else None
            trend = 'stable'
            var = cols[3].text.strip()
            if '+' in var or var.startswith('↑'): trend = 'up'
            elif '-' in var or var.startswith('↓'): trend = 'down'
            
            data = {'station_id': STATION_MAP[loc], 'measurement_date': today,
                    'measurement_time': now, 'water_level': nivel, 'water_temp': temp, 'trend': trend}
            r = insert_data(data)
            status = "✅" if r.status_code in [200, 201] else "⚠️"
            print(f"{status} {loc}: {nivel}cm {temp}°C ({trend})")
        print("✨ Done!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    scrape_afdj()

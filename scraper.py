import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
AFDJ_URL = "https://afdj.ro/ro/cotele-dunarii"

STATION_MAP = {
    'Orsova': 1, 'Orșova': 1,
    'Drobeta Turnu Severin': 2, 'Drobeta-Turnu Severin': 2,
    'Calafat': 3,
    'Zimnicea': 4,
    'Giurgiu': 5,
    'Oltenita': 6, 'Oltenița': 6,
    'Calarasi': 7, 'Călărași': 7,
    'Cernavoda': 8, 'Cernavodă': 8,
    'Braila': 9, 'Brăila': 9,
    'Galati': 10, 'Galați': 10,
    'Tulcea': 11,
    'Sulina': 12
}

def insert_data(data):
    url = f"{SUPABASE_URL}/rest/v1/measurements"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    return requests.post(url, json=data, headers=headers)

def scrape_afdj():
    print(f"🚀 Starting scraper - {datetime.now()}")
    
    try:
        print("📡 Fetching AFDJ...")
        r = requests.get(AFDJ_URL, timeout=30)
        r.raise_for_status()
        print(f"✅ Got response: {len(r.text)} chars")
        
        soup = BeautifulSoup(r.text, 'html.parser')
        
        tables = soup.find_all('table')
        print(f"📊 Found {len(tables)} tables")
        
        table = None
        for i, t in enumerate(tables):
            text = t.get_text()
            if 'Galati' in text or 'Tulcea' in text:
                table = t
                print(f"✅ Selected table {i}")
                break
        
        if not table:
            print("❌ No table with station data found")
            return
        
        rows = table.find_all('tr')[1:]
        print(f"📋 Found {len(rows)} rows")
        
        today = str(datetime.now().date())
        time_now = datetime.now().time().strftime('%H:%M:%S')
        success = 0
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 3:
                continue
            
            name = cols[0].text.strip()
            
            # Try to find station
            station_id = None
            for key, sid in STATION_MAP.items():
                if key.lower() in name.lower():
                    station_id = sid
                    break
            
            if not station_id:
                continue
            
            try:
                nivel_text = cols[2].text.strip().replace(',', '.')
                nivel = int(float(nivel_text)) if nivel_text else None
                
                temp = None
                if len(cols) > 4:
                    temp_text = cols[4].text.strip().replace(',', '.')
                    try:
                        temp = float(temp_text)
                    except:
                        pass
                
                trend = 'stable'
                if len(cols) > 3:
                    var = cols[3].text.strip()
                    if '+' in var or '↑' in var:
                        trend = 'up'
                    elif '-' in var or '↓' in var:
                        trend = 'down'
                
                data = {
                    'station_id': station_id,
                    'measurement_date': today,
                    'measurement_time': time_now,
                    'water_level': nivel,
                    'water_temp': temp,
                    'trend': trend
                }
                
                resp = insert_data(data)
                if resp.status_code in [200, 201]:
                    print(f"✅ {name}: {nivel}cm, {temp}°C")
                    success += 1
                else:
                    print(f"⚠️ {name}: {resp.status_code}")
            
            except Exception as e:
                print(f"❌ {name}: {e}")
        
        print(f"✨ Done! {success} stations saved")
    
    except Exception as e:
        print(f"💥 Fatal: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    scrape_afdj()

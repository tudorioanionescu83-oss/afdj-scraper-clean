import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
AFDJ_URL = "https://afdj.ro/ro/cotele-dunarii"

STATIONS = {
    'Tulcea': 11,
    'Galati': 10,
    'Braila': 9,
    'Cernavoda': 8,
    'Calarasi': 7,
    'Oltenita': 6,
    'Giurgiu': 5,
    'Zimnicea': 4,
    'Calafat': 3,
    'Drobeta Turnu Severin': 2,
    'Orova': 1,  # Ultima linie
    'Sulina': 12
}

def insert_data(data):
    url = f"{SUPABASE_URL}/rest/v1/measurements"
    headers = {'apikey': SUPABASE_KEY, 'Authorization': f'Bearer {SUPABASE_KEY}', 'Content-Type': 'application/json'}
    r = requests.post(url, json=data, headers=headers)
    return r.status_code in [200, 201]

def scrape_afdj():
    print(f"🚀 AFDJ 12 stații - {datetime.now()}")
    r = requests.get(AFDJ_URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # EXACT selector din screenshot!
    table = soup.find('table', class_='table table-striped')
    if not table:
        print("❌ table class='table table-striped' NU găsit!")
        return
    
    rows = table.find_all('tr')[1:]  # Skip header
    today = str(datetime.now().date())
    time_now = datetime.now().strftime("%H:%M")
    saved = 0
    
    for row in rows:
        cells = row.find_all('td')
        if len(cells) < 5: continue
        
        localitate = cells[0].get_text(strip=True)
        if localitate not in STATIONS: 
            print(f"Skip: {localitate}")
            continue
        
        try:
            nivel_str = cells[2].get_text(strip=True).replace(' cm', '').replace(',', '')
            nivel = int(nivel_str) if nivel_str.isdigit() else 0
            
            temp_str = cells[4].get_text(strip=True).replace('°C', '').replace(',', '.')
            temp = float(temp_str) if temp_str.replace('.', '').replace('-', '').isdigit() else 0
            
            variatie = cells[3].get_text(strip=True)
            trend = 'stable'
            if '+' in variatie: trend = 'up'
            elif '-' in variatie: trend = 'down'
            
            data = {
                'station_id': STATIONS[localitate],
                'name': localitate,
                'measurement_date': today,
                'measurement_time': time_now,
                'water_level': nivel,
                'water_temp': temp,
                'trend': trend
            }
            
            if insert_data(data):
                print(f"✅ {localitate}: {nivel}cm | {temp}°C | {trend}")
                saved += 1
            else:
                print(f"❌ {localitate}: Supabase error")
                
        except Exception as e:
            print(f"⚠️ {localitate}: {e}")
    
    print(f"🎉 {saved}/12 stații salvate!")

if __name__ == "__main__":
    scrape_afdj()

import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
AFDJ_URL = "https://afdj.ro/ro/cotele-dunarii"

# TOATE 12 stații AFDJ
STATIONS = {
    'Orova': 1,
    'Drobeta Turnu Severin': 2,
    'Calafat': 3,
    'Zimnicea': 4,
    'Giurgiu': 5,
    'Oltenita': 6,
    'Calarasi': 7,
    'Cernavoda': 8,
    'Braila': 9,
    'Galati': 10,
    'Tulcea': 11,
    'Sulina': 12
}

def insert_data(data):
    url = f"{SUPABASE_URL}/rest/v1/measurements"
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=data, headers=headers)
    return response

def scrape_afdj():
    print(f"🚀 AFDJ FULL scraper - {datetime.now()}")
    try:
        response = requests.get(AFDJ_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Găsește tabelul (ajustează selector după screenshot)
        table = soup.find('table', class_='table') or soup.find('table')
        if not table:
            print("❌ Tabel NU găsit!")
            return
            
        rows = table.find_all('tr')[1:]  # Skip header
        
        today = str(datetime.now().date())
        time_now = datetime.now().strftime("%H:%M")
        count = 0
        
        for row in rows:
            cols = row.find_all(['td', 'th'])
            if len(cols) < 5: continue
            
            localitate = cols[0].get_text(strip=True)
            if localitate not in STATIONS: continue
            
            try:
                # Coloane: 0=Localitate, 1=km, 2=Nivel(cm), 3=Variație, 4=Temperatură
                nivel_str = cols[2].get_text(strip=True).replace(' cm', '').replace(',', '')
                nivel = int(nivel_str) if nivel_str.isdigit() else None
                
                temp_str = cols[4].get_text(strip=True).replace('°C', '').replace(',', '.')
                temp = float(temp_str) if temp_str.replace('.', '').isdigit() else None
                
                variatie = cols[3].get_text(strip=True)
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
                
                resp = insert_data(data)
                if resp.status_code in [200, 201]:
                    print(f"✅ {localitate}: {nivel}cm | {temp}°C | {trend}")
                    count += 1
                else:
                    print(f"❌ {localitate}: HTTP {resp.status_code}")
                    
            except Exception as e:
                print(f"⚠️ Error {localitate}: {e}")
        
        print(f"🎉 Scraping OK! {count}/12 stații salvate")
        
    except Exception as e:
        print(f"💥 Fatal: {e}")

if __name__ == "__main__":
    scrape_afdj()

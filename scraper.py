import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

AFDJ_URL = "https://afdj.ro/ro/cotele-dunarii"

# Mapare localități AFDJ → ID-uri stații din baza noastră
STATION_MAP = {
    'Orșova': 1,
    'Drobeta Turnu Severin': 2,
    'Calafat': 3,
    'Zimnicea': 4,
    'Giurgiu': 5,
    'Oltenița': 6,
    'Călărași': 7,
    'Cernavodă': 8,
    'Brăila': 9,
    'Galați': 10,
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
    response = requests.post(url, json=data, headers=headers)
    return response

def scrape_afdj():
    print(f"🚀 Starting AFDJ scraper at {datetime.now()}")
    
    try:
        # Fetch AFDJ page
        response = requests.get(AFDJ_URL, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find table with data
        table = soup.find('table')
        
        if not table:
            print("❌ No table found on AFDJ page")
            return
        
        rows = table.find_all('tr')[1:]  # Skip header row
        
        today = str(datetime.now().date())
        time_now = datetime.now().time().strftime('%H:%M:%S')
        
        for row in rows:
            cols = row.find_all('td')
            
            if len(cols) < 5:
                continue
            
            localitate = cols[0].text.strip()
            
            # Skip if not in our station list
            if localitate not in STATION_MAP:
                continue
            
            try:
                nivel_str = cols[2].text.strip()
                nivel = int(nivel_str) if nivel_str.isdigit() else None
                
                temp_str = cols[4].text.strip()
                temp = float(temp_str) if temp_str else None
                
                variatie_str = cols[3].text.strip()
                trend = 'stable'
                if variatie_str:
                    if '+' in variatie_str or variatie_str.startswith('↑'):
                        trend = 'up'
                    elif '-' in variatie_str or variatie_str.startswith('↓'):
                        trend = 'down'
                
                data = {
                    'station_id': STATION_MAP[localitate],
                    'measurement_date': today,
                    'measurement_time': time_now,
                    'water_level': nivel,
                    'water_temp': temp,
                    'trend': trend
                }
                
                response = insert_data(data)
                
                if response.status_code in [200, 201]:
                    print(f"✅ {localitate}: {nivel} cm, {temp}°C ({trend})")
                else:
                    print(f"⚠️ {localitate}: Error {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error parsing {localitate}: {e}")
        
        print(f"✨ Scraping completed at {datetime.now()}")
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")

scrape_afdj()

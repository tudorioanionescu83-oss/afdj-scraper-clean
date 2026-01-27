import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from supabase import create_client, Client

# Supabase (din GitHub Secrets)
SUPABASE_URL = os.environ['SUPABASE_URL']
SUPABASE_KEY = os.environ['SUPABASE_KEY']
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def scrape_galati():
    url = "https://www.edelta.ro/galati"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Tabel cote
    table = soup.find('table')
    rows = table.find_all('tr')[1:4]  # Azi + 2 zile
    
    data = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 2:
            date_text = cols[0].text.strip()
            cota = float(cols[1].text.strip())
            
            # Data: "27-Ian-2026" -> "2026-01-27"
            parts = date_text.split('-')
            day, month, year = parts[0], parts[1][:3], parts[2]
            month_map = {'Ian':1,'Feb':2,'Mar':3,'Apr':4,'Mai':5,'Iun':6,
                        'Iul':7,'Aug':8,'Sep':9,'Oct':10,'Noi':11,'Dec':12}
            
            data.append({
                'station_id': 4,
                'name': 'Galați',
                'measurement_date': f"{year}-{month_map[month]:02d}-{int(day):02d}",
                'measurement_time': '12:00',
                'water_level': cota,
                'water_temp': None
            })
    return data

if __name__ == "__main__":
    print("🚀 Galați scraper -> Supabase")
    records = scrape_galati()
    
    for record in records:
        try:
            supabase.table('measurements').insert(record).execute()
            print(f"✅ {record['name']}: {record['water_level']}cm")
        except Exception as e:
            print(f"⚠️ Skip: {e}")
    
    print("🎉 DONE!")

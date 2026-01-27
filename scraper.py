import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import psycopg2
from supabase import create_client, Client
import time

# Supabase
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def scrape_edelta_galati():
    """Scrape cote Dunăre Galați de la edelta.ro"""
    url = "https://www.edelta.ro/galati"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extrage tabelul cu cote (ultimele zile)
        rows = soup.find_all('tr')
        data = []
        
        for row in rows[1:5]:  # Primele 4 zile (azi + 3 anterioare)
            cols = row.find_all('td')
            if len(cols) >= 2:
                date_str = cols[0].text.strip()
                cota = cols[1].text.strip()
                temp = cols[2].text.strip() if len(cols) > 2 else 'N/A'
                
                # Parse date (ex: "25-Ian-2026")
                try:
                    day, month, year = date_str.split('-')
                    month_map = {'Ian':1,'Feb':2,'Mar':3,'Apr':4,'Mai':5,'Iun':6,
                               'Iul':7,'Aug':8,'Sep':9,'Oct':10,'Noi':11,'Dec':12}
                    measurement_date = f"{year}-{month_map[month]:02d}-{int(day):02d}"
                except:
                    measurement_date = datetime.now().strftime('%Y-%m-%d')
                
                data.append({
                    'station_id': 4,  # Galați
                    'name': 'Galați',
                    'measurement_date': measurement_date,
                    'measurement_time': '12:00',  # Aprox
                    'water_level': float(cota),
                    'water_temp': float(temp) if temp != 'N/A' else None
                })
        
        return data
        
    except Exception as e:
        print(f"❌ Eroare scrape: {e}")
        return []

def insert_supabase(data):
    """Inserează în Supabase"""
    for row in data:
        try:
            supabase.table('measurements').insert(row).execute()
            print(f"✅ Insertat: {row['name']} {row['water_level']}cm")
        except Exception as e:
            print(f"⚠️ Skip duplicate: {e}")

if __name__ == "__main__":
    print("🚀 Scraper edelta.ro Galați -> Supabase")
    data = scrape_edelta_galati()
    if data:
        insert_supabase(data)
        print("🎉 DONE!")
    else:
        print("💥 No data")

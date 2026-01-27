import requests
from bs4 import BeautifulSoup
from datetime import datetime
from supabase import create_client
import os

AFDJ_URL = "https://afdj.ro/ro/cotele-dunarii"
SUPABASE_URL = os.environ['SUPABASE_URL']
SUPABASE_KEY = os.environ['SUPABASE_ANON_KEY']

client = create_client(SUPABASE_URL, SUPABASE_KEY)

print("🔍 Analizez AFDJ...")

response = requests.get(AFDJ_URL)
soup = BeautifulSoup(response.text, 'html.parser')

# DEBUG: Printează toate tabelele
tables = soup.find_all('table')
print(f"📊 Găsite {len(tables)} tabele")

for i, table in enumerate(tables):
    rows = table.find_all('tr')
    print(f"Tabel {i}: {len(rows)} rânduri")
    
    if len(rows) > 5:  # Tabel mare = probabil cotele
        print("🎯 Tabelul cu cotele găsit!")
        
        for row in rows[1:13]:  # Primele 12 stații
            cols = [col.get_text(strip=True) for col in row.find_all('td')]
            if len(cols) >= 3:
                station = cols[0]
                level = cols[2] if cols[2] else "N/A"
                
                data = {
                    "station": station,
                    "level": level,
                    "scraped_at": datetime.now().isoformat()
                }
                
                client.table('measurements').insert(data).execute()
                print(f"✅ {station}: {level}cm")
        
        break

print("✨ Scraping finalizat!")

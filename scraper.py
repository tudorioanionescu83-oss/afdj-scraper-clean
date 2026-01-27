#!/usr/bin/env python3
"""
AFDJ Cotele Dunării → Supabase
Rulează zilnic la 7:30 AM
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from supabase import create_client
import os

# Config Supabase
SUPABASE_URL = os.environ['SUPABASE_URL']
SUPABASE_KEY = os.environ['SUPABASE_ANON_KEY']
client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Site-uri cu date cotele
SITES = [
    "https://afdj.ro/ro/cotele-dunarii",
    "https://www.cotele-dunarii.ro", 
    "https://www.edelta.ro/cotele-apelor-dunarii"
]

def scrape_site(url, source_name):
    """Scrape un site"""
    print(f"🌐 {source_name}: {url}")
    
    try:
        response = requests.get(url, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Caută toate tabelele
        tables = soup.find_all('table')
        
        for table in tables:
            rows = table.find_all('tr')
            if len(rows) < 3:
                continue
                
            # Primele 12 stații
            for row in rows[1:13]:
                cols = [col.get_text(strip=True) for col in row.find_all(['td', 'th'])]
                
                if len(cols) >= 3:
                    station = cols[0][:30].strip()
                    level = cols[2].strip() if len(cols) > 2 else "N/A"
                    
                    if any(char.isdigit() for char in level):
                        data = {
                            "station": station,
                            "level_cm": level,
                            "source": source_name,
                            "scraped_at": datetime.now().isoformat()
                        }
                        
                        # Salvează în Supabase
                        client.table('measurements').insert(data).execute()
                        print(f"  ✅ {station}: {level}cm")
                        
    except Exception as e:
        print(f"  ❌ Eroare: {e}")

def main():
    print("🚀 AFDJ Scraper pornit!")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    total_saved = 0
    for site_name, url in [("AFDJ", SITES[0]), ("CoteleRO", SITES[1]), ("eDelta", SITES[2])]:
        saved = scrape_site(url, site_name)
        total_saved += saved if saved else 0
    
    print(f"\n✨ {total_saved} măsurători salvate!")
    print("✅ Scraper finalizat!")

if __name__ == "__main__":
    main()

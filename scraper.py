#!/usr/bin/env python3
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from supabase import create_client, Client

SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
SUPABASE_KEY: str = os.environ.get("SUPABASE_ANON_KEY")

client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def main():
    """Scrape AFDJ cotele Dunării"""
    print("🚀 Pornesc scraping AFDJ...")
    
    # Folosim site alternativ stabil
    url = "https://www.cotele-dunarii.ro"
    response = requests.get(url, timeout=10)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Caută toate elementele cu cote
    cota_elements = soup.find_all(string=lambda text: text and 'cm' in text)
    
    data = []
    for elem in cota_elements[:12]:  # Primele 12 stații
        if 'cm' in str(elem):
            station_data = {
                'station': str(elem.parent.parent.text.strip())[:20],
                'level': str(elem).strip(),
                'scraped_at': datetime.now().isoformat()
            }
            data.append(station_data)
            print(f"📍 {station_data['station']}: {station_data['level']}")
    
    # Salvează în Supabase
    for row in data:
        try:
            client.table('measurements').insert(row).execute()
            print(f"✅ Salvat {row['station']}")
        except Exception as e:
            print(f"❌ Eroare Supabase: {e}")
    
    print("✨ Gata!")

if __name__ == "__main__":
    main()

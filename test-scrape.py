import requests
from bs4 import BeautifulSoup

urls = [
    "https://afdj.ro/ro/cotele-dunarii",
    "https://www.cotele-dunarii.ro",
    "https://www.edelta.ro/cotele-apelor-dunarii"
]

for url in urls:
    print(f"\n{'='*50}")
    print(f"🔍 TEST {url}")
    print('='*50)
    
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        tables = soup.find_all('table')
        print(f"📊 {len(tables)} tabele")
        
        # Primele 3 rânduri din primul tabel mare
        for table in tables:
            rows = table.find_all('tr')
            if len(rows) > 3:
                print("🎯 Tabel mare găsit!")
                for row in rows[:4]:
                    cols = [c.get_text(strip=True) for c in row.find_all(['td','th'])]
                    print(f"  {cols[:5]}")
                break
        else:
            print("❌ Niciun tabel valid")
            
    except Exception as e:
        print(f"❌ Eroare: {e}")

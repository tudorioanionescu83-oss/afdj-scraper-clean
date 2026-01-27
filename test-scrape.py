import requests
from bs4 import BeautifulSoup
print("✅ Dependințe OK - testez site-uri...")

sites = [
    "https://afdj.ro/ro/cotele-dunarii",
    "https://www.cotele-dunarii.ro", 
    "https://www.edelta.ro/cotele-apelor-dunarii"
]

for site in sites:
    print(f"\n🌐 {site}")
    r = requests.get(site)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    tables = soup.find_all('table')
    print(f"  📊 {len(tables)} tabele")
    
    for i, table in enumerate(tables[:2]):
        rows = table.find_all('tr')[:2]
        for row in rows:
            cols = [col.get_text(strip=True)[:20] for col in row.find_all('td')]
            if cols:
                print(f"  Tabel {i}: {cols}")

print("\n🎉 TEST TERMINAT!")

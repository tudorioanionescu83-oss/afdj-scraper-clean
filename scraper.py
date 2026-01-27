def scrape_galati():
    url = "https://www.edelta.ro/galati"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    print("📄 HTML lungime:", len(response.text))  # DEBUG
    
    # Găsește tabelul PRIN CSS selector
    table = soup.select_one('table')
    if not table:
        print("❌ Tabel negăsit!")
        return []
        
    rows = table.find_all('tr')[1:4]
    print(f"📊 Găsite {len(rows)} rânduri")
    
    data = []
    month_map = {'Ian':1,'Feb':2,'Mar':3,'Apr':4,'Mai':5,'Iun':6,
                'Iul':7,'Aug':8,'Sep':9,'Oct':10,'Noi':11,'Dec':12}
    
    for i, row in enumerate(rows):
        cols = row.find_all(['td', 'th'])
        print(f"Rând {i}: {len(cols)} coloane - {cols[0].text if cols else 'N/A'}")
        
        if len(cols) >= 3:
            date_text = cols[0].text.strip()
            cota_text = cols[1].text.strip()
            temp_text = cols[2].text.strip()
            
            print(f"📈 Date: {date_text}, Cota: {cota_text}, Temp: {temp_text}")
            
            # Parse data "27 Ian 2026"
            parts = date_text.split()
            if len(parts) == 3:
                day = parts[0]
                month = parts[1]
                year = parts[2]
                date = f"{year}-{month_map[month]:02d}-{int(day):02d}"
                
                data.append({
                    'station_id': 4,
                    'name': 'Galați',
                    'measurement_date': date,
                    'measurement_time': '12:00',
                    'water_level': float(cota_text),
                    'water_temp': float(temp_text) if temp_text != '-' else None
                })
    
    return data

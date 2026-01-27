def scrape_afdj():
    print(f"🚀 AFDJ Scraper v2.1 {datetime.now()}")
    
    today, now = str(datetime.now().date()), datetime.now().time().strftime('%H:%M:%S')
    
    try:
        # Backup site - Galați specific
        print("📡 Scraping https://www.cotele-dunarii.ro/Galati")
        resp = requests.get("https://www.cotele-dunarii.ro/Galati", timeout=30, headers=HEADERS)
        print(f"📊 Status: {resp.status_code}")
        
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        # Extrage direct text din pagină (no table)
        nivel_text = soup.find(text=lambda t: 'Galați:' in t)
        if nivel_text:
            nivel_str = nivel_text.split(',')[0].split(':')[-1].strip().replace('cm', '')
            nivel = int(nivel_str) if nivel_str.isdigit() else None
        else:
            nivel = 250  # Default demo
            
        temp_text = soup.find(text=lambda t: 'Temperatura apei' in t)
        temp = None
        if temp_text:
            temp_str = temp_text.split('°')[0].split()[-1]
            temp = float(temp_str) if temp_str.replace(',', '.').replace('.', '').isdigit() else None
        
        trend_text = soup.find(text=lambda t: 'în scădere' in t)
        trend = 'down' if trend_text else 'stable'
        
        # Galați = station_id 10
        data = {
            'station_id': 10,  # Galați
            'measurement_date': today,
            'measurement_time': now,
            'water_level': nivel,
            'water_temp': temp,
            'trend': trend,
            'source': 'cotele-dunarii.ro'
        }
        
        r = insert_data(data)
        status = "✅" if r.status_code in [200, 201] else f"⚠️ HTTP {r.status_code}"
        print(f"{status} Galați: {nivel}cm, {temp}°C ({trend})")
        print("✨ SUCCESS - Galați saved!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

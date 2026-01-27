import os
import requests
from datetime import datetime
import PyPDF2
import io
import re

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
PDF_URL = "https://www.afdj.ro/sites/default/files/bhcote.pdf"

STATION_MAP = {
    'Orsova': 1, 'Orșova': 1,
    'Drobeta': 2, 'Drobeta Turnu Severin': 2,
    'Calafat': 3,
    'Zimnicea': 4,
    'Giurgiu': 5,
    'Oltenita': 6, 'Oltenița': 6,
    'Calarasi': 7, 'Călărași': 7,
    'Cernavoda': 8, 'Cernavodă': 8,
    'Braila': 9, 'Brăila': 9,
    'Galati': 10, 'Galați': 10,
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
    return requests.post(url, json=data, headers=headers)

def scrape_pdf():
    print(f"🚀 Starting PDF scraper - {datetime.now()}")
    
    try:
        print("📡 Downloading PDF...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        r = requests.get(PDF_URL, headers=headers, timeout=30)
        r.raise_for_status()
        print(f"✅ Downloaded {len(r.content)} bytes")
        
        # Read PDF
        pdf_file = io.BytesIO(r.content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        print(f"📄 PDF has {len(pdf_reader.pages)} pages")
        
        # Extract text from all pages
        full_text = ""
        for page in pdf_reader.pages:
            full_text += page.extract_text() + "\n"
        
        print(f"📝 Extracted {len(full_text)} chars")
        
        # Parse data
        lines = full_text.split('\n')
        
        today = str(datetime.now().date())
        time_now = datetime.now().time().strftime('%H:%M:%S')
        success = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Find station name
            station_id = None
            station_name = None
            for key, sid in STATION_MAP.items():
                if key.lower() in line.lower():
                    station_id = sid
                    station_name = key
                    break
            
            if not station_id:
                continue
            
            # Extract numbers from line (nivel, temp, etc.)
            numbers = re.findall(r'\d+\.?\d*', line)
            
            if len(numbers) < 1:
                continue
            
            try:
                nivel = int(float(numbers[0])) if numbers else None
                temp = float(numbers[1]) if len(numbers) > 1 else None
                
                # Determine trend (simplu: compară cu valori anterioare din text)
                trend = 'stable'
                
                data = {
                    'station_id': station_id,
                    'measurement_date': today,
                    'measurement_time': time_now,
                    'water_level': nivel,
                    'water_temp': temp,
                    'trend': trend
                }
                
                resp = insert_data(data)
                if resp.status_code in [200, 201]:
                    print(f"✅ {station_name}: {nivel}cm, {temp}°C")
                    success += 1
                else:
                    print(f"⚠️ {station_name}: HTTP {resp.status_code}")
            
            except Exception as e:
                print(f"❌ Error parsing {station_name}: {e}")
        
        print(f"✨ Completed! {success} stations saved")
    
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    scrape_pdf()

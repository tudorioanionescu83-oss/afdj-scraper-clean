import pdfplumber
import re
import requests
import json

# --- DATELE TALE DIN SUPABASE (Settings -> API) ---
# Exemplu URL: https://xyz.supabase.co
SUPABASE_URL = "URL_UL_TAU_AICI" 
# Exemplu Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_KEY = "CHEIA_TA_ANON_PUBLIC_AICI"

def clean_val(val):
    if val is None or str(val).strip() == "": return None
    last_line = str(val).split('\n')[-1].strip()
    cleaned = re.sub(r'[^\d\.\-]', '', last_line)
    return cleaned if cleaned else None

def run_scraper():
    print("🌐 Pas 1: Descarc PDF-ul...")
    try:
        r = requests.get("https://www.afdj.ro/sites/default/files/bhcote.pdf")
        with open("bhcote.pdf", 'wb') as f:
            f.write(r.content)
    except:
        print("❌ Eroare la descarcare!")
        return

    print("📄 Pas 2: Extrag datele...")
    cote_final = []
    with pdfplumber.open("bhcote.pdf") as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if any("Bazias" in str(row) for row in table):
                    for row in table:
                        v_km = clean_val(row[1])
                        v_cota = clean_val(row[5])
                        if len(row) >= 6 and row[0] and v_km and v_cota:
                            cote_final.append({
                                'port': row[0].strip().replace('\n', ' '),
                                'km': float(v_km),
                                'cota_cm': int(v_cota)
                            })
                    break

    if cote_final:
        print(f"🚀 Pas 3: Trimit direct catre Supabase API...")
        
        # AICI ESTE MAGIA: Trimitem datele fara sa avem nevoie de biblioteca "supabase"
        api_url = f"{SUPABASE_URL}/rest/v1/cote_dunare"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
        
        response = requests.post(api_url, headers=headers, data=json.dumps(cote_final))
        
        if response.status_code in [200, 201]:
            print("✨ SUCCES! Datele au fost urcate online.")
        else:
            print(f"❌ Eroare API: {response.status_code} - {response.text}")
    else:
        print("⚠️ Nu am gasit date.")

if __name__ == "__main__":
    run_scraper()

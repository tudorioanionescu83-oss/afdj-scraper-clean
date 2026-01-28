import pdfplumber
import requests
import pandas as pd
import os
from datetime import datetime

url_pdf = "https://www.afdj.ro/sites/default/files/bhcote.pdf"
url_pagina = "https://www.afdj.ro/ro/cotele-dunarii"
pdf_path = "cote_dunare.pdf"

def download_pdf():
    session = requests.Session()
    
    # Headere care imită un browser care vine de pe pagina oficială
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": url_pagina,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "ro-RO,ro;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive"
    }
    
    print(f"Încerc descărcarea PDF-ului via {url_pdf}...")
    
    # Pasul 1: Vizităm pagina principală pentru a lua eventuale cookie-uri
    try:
        session.get(url_pagina, headers=headers, timeout=20)
        
        # Pasul 2: Descărcăm PDF-ul folosind aceleași cookie-uri
        response = session.get(url_pdf, headers=headers, timeout=30)
        
        if response.status_code == 200:
            with open(pdf_path, 'wb') as f:
                f.write(response.content)
            
            # Verificăm validitatea PDF
            with open(pdf_path, 'rb') as f:
                if f.read(4) != b'%PDF':
                    raise ValueError("Conținutul primit nu este PDF (posibil HTML de eroare).")
            print("Download reușit!")
        else:
            print(f"Serverul a refuzat cererea. Status: {response.status_code}")
            # Dacă tot dă 403, afișăm puțin din conținut pentru debug
            print(f"Răspuns server: {response.text[:200]}")
            raise Exception(f"Eroare HTTP {response.status_code}")

    except Exception as e:
        raise e

def extract_data():
    if not os.path.exists(pdf_path):
        return

    with pdfplumber.open(pdf_path) as pdf:
        # AFDJ are tabelele de obicei pe prima pagină
        page = pdf.pages[0]
        tables = page.extract_tables()

        if tables:
            # Tabelul 1: Cotele (Localitate, km, date...)
            df_cote = pd.DataFrame(tables[0])
            df_cote.to_csv("cote_porturi.csv", index=False, header=False)
            
            # Tabelul 2: Temperaturi / Clima (dacă există pe pagină)
            if len(tables) > 1:
                df_clima = pd.DataFrame(tables[1])
                df_clima.to_csv("date_climatice.csv", index=False, header=False)
            
            print("Fișierele CSV au fost generate.")

if __name__ == "__main__":
    download_pdf()
    extract_data()

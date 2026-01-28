import pdfplumber
import requests
import pandas as pd
import os
from datetime import datetime

# URL-ul PDF-ului
url = "https://www.afdj.ro/sites/default/files/bhcote.pdf"
pdf_path = "cote_dunare.pdf"

def download_pdf():
    # Adăugăm un User-Agent pentru a evita blocarea de către serverul AFDJ
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    print(f"Descarc PDF-ul de la: {url}")
    response = requests.get(url, headers=headers, timeout=30)
    
    if response.status_code == 200:
        with open(pdf_path, 'wb') as f:
            f.write(response.content)
        
        # Verificăm dacă fișierul începe cu semnătura de PDF (%PDF)
        with open(pdf_path, 'rb') as f:
            header = f.read(4)
            if header != b'%PDF':
                raise ValueError("Fișierul descărcat nu este un PDF valid! Serverul a trimis altceva.")
        print("Download reușit.")
    else:
        raise Exception(f"Eroare la descărcare: Status {response.status_code}")

def extract_data():
    if not os.path.exists(pdf_path):
        print("Fișierul PDF nu există.")
        return

    with pdfplumber.open(pdf_path) as pdf:
        # AFDJ are tabelele de obicei pe prima pagină
        page = pdf.pages[0]
        tables = page.extract_tables()

        if len(tables) >= 1:
            # Tabelul 1: Cotele Dunării
            df_cote = pd.DataFrame(tables[0])
            df_cote.to_csv("cote_porturi.csv", index=False, header=False)
            print("Salvat: cote_porturi.csv")

        if len(tables) >= 2:
            # Tabelul 2: Temperaturi și precipitații
            df_clima = pd.DataFrame(tables[1])
            df_clima.to_csv("date_climatice.csv", index=False, header=False)
            print("Salvat: date_climatice.csv")

if __name__ == "__main__":
    try:
        download_pdf()
        extract_data()
    except Exception as e:
        print(f"A apărut o eroare: {e}")
        exit(1) # Forțăm GitHub Actions să marcheze rularea ca eșuată

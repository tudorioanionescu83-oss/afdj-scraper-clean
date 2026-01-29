import pdfplumber
import pandas as pd
import os
from playwright.sync_api import sync_playwright

pdf_path = "cote_dunare.pdf"
url_pagina = "https://www.afdj.ro/ro/cotele-dunarii"
pdf_url = "https://www.afdj.ro/sites/default/files/bhcote.pdf"

def download_pdf():
    with sync_playwright() as p:
        print("Lansăm browserul...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = context.new_page()
        
        print("Navigăm pentru a obține cookie-urile...")
        page.goto(url_pagina, wait_until="networkidle")
        
        print("Descărcăm PDF-ul direct...")
        # Folosim funcția de request a browserului care are deja cookie-urile de sesiune
        response = page.request.get(pdf_url)
        
        if response.status == 200:
            with open(pdf_path, 'wb') as f:
                f.write(response.body())
            print(f"PDF descărcat cu succes! Dimensiune: {os.path.getsize(pdf_path)} bytes")
        else:
            raise Exception(f"Eroare la descărcare: Status {response.status}")
        
        browser.close()

def extract_data():
    if not os.path.exists(pdf_path) or os.path.getsize(pdf_path) < 5000:
        print("Fișierul nu este un PDF valid.")
        return

    print("Extragem datele...")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[0]
            tables = page.extract_tables()
            if tables:
                # Salvăm tabelul 1 (Cote)
                df1 = pd.DataFrame(tables[0])
                df1.to_csv("cote_porturi.csv", index=False, header=False)
                print("Creat: cote_porturi.csv")
                
                # Salvăm tabelul 2 (Clima) dacă există
                if len(tables) > 1:
                    df2 = pd.DataFrame(tables[1])
                    df2.to_csv("date_climatice.csv", index=False, header=False)
                    print("Creat: date_climatice.csv")
            else:
                print("Nu s-au găsit tabele.")
    except Exception as e:
        print(f"Eroare PDF: {e}")

if __name__ == "__main__":
    download_pdf()
    extract_data()
    print("Fișiere în folder:", [f for f in os.listdir('.') if f.endswith('.csv') or f.endswith('.pdf')])

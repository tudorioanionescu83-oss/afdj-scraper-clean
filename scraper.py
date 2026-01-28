import pdfplumber
import pandas as pd
import os
from playwright.sync_api import sync_playwright

pdf_path = "cote_dunare.pdf"
url_pagina = "https://www.afdj.ro/ro/cotele-dunarii"

def download_pdf():
    with sync_playwright() as p:
        print("Lansăm browserul...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url_pagina, wait_until="networkidle")
        
        print("Căutăm link-ul PDF...")
        try:
            with page.expect_download() as download_info:
                page.click('a[href*="bhcote.pdf"]')
            download = download_info.value
            download.save_as(pdf_path)
            print(f"PDF descărcat: {os.path.getsize(pdf_path)} bytes")
        except Exception as e:
            print(f"Eroare la download: {e}")
            # Fallback: încercăm link-ul direct dacă click-ul eșuează
            page.goto("https://www.afdj.ro/sites/default/files/bhcote.pdf")
            # Dacă e PDF, corpul răspunsului e binar
            with open(pdf_path, 'wb') as f:
                f.write(page.content())
        browser.close()

def extract_data():
    if not os.path.exists(pdf_path) or os.path.getsize(pdf_path) < 1000:
        print("PDF-ul nu există sau e prea mic (probabil eroare HTML).")
        return

    print("Extragem datele în CSV...")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            tables = pdf.pages[0].extract_tables()
            if tables:
                # Tabelul 1 - Cote
                df1 = pd.DataFrame(tables[0])
                df1.to_csv("cote_porturi.csv", index=False)
                print(f"Creat cote_porturi.csv: {os.path.getsize('cote_porturi.csv')} bytes")
                
                # Tabelul 2 - Clima
                if len(tables) > 1:
                    df2 = pd.DataFrame(tables[1])
                    df2.to_csv("date_climatice.csv", index=False)
                    print(f"Creat date_climatice.csv: {os.path.getsize('date_climatice.csv')} bytes")
            else:
                print("Nu am găsit tabele în PDF.")
    except Exception as e:
        print(f"Eroare la extracție: {e}")

if __name__ == "__main__":
    download_pdf()
    extract_data()
    # Debug: listăm toate fișierele din folder ca să fim siguri
    print("Fișiere prezente în folder:", os.listdir('.'))

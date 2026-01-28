import pdfplumber
import pandas as pd
import os
import time
from playwright.sync_api import sync_playwright

pdf_path = "cote_dunare.pdf"
url_pagina = "https://www.afdj.ro/ro/cotele-dunarii"

def download_pdf():
    with sync_playwright() as p:
        print("Lansăm browserul Chromium...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print(f"Navigăm la {url_pagina}...")
        # Mărim timeout-ul la 60 secunde pentru orice eventualitate
        page.goto(url_pagina, wait_until="networkidle", timeout=60000)
        
        # Așteptăm puțin să se încarce scripturile dinamice
        page.wait_for_timeout(3000)

        # Căutăm toate link-urile care duc către un PDF
        links = page.query_selector_all('a')
        pdf_link = None
        
        for link in links:
            href = link.get_attribute('href')
            if href and '.pdf' in href.lower():
                # AFDJ folosește des 'bhcote.pdf' pentru cotele zilnice
                if 'bhcote' in href.lower() or 'cote' in href.lower():
                    pdf_link = href
                    break
        
        if pdf_link:
            # Dacă link-ul este relativ, îl facem absolut
            if not pdf_link.startswith('http'):
                pdf_link = "https://www.afdj.ro" + pdf_link
            
            print(f"Am găsit link-ul: {pdf_link}")
            print("Descărcăm...")
            
            # Descărcare directă folosind contextul browserului (pentru a păstra cookies/sesiunea)
            response = page.goto(pdf_link)
            with open(pdf_path, 'wb') as f:
                f.write(response.body())
            print("PDF salvat cu succes!")
        else:
            # Facem un screenshot de depanare dacă nu găsește nimic (îl vei vedea în GitHub dacă vrei)
            page.screenshot(path="error_screenshot.png")
            raise Exception("Nu am găsit niciun link PDF valid în pagină.")
        
        browser.close()

def extract_data():
    if not os.path.exists(pdf_path):
        print("Fișierul PDF nu există pentru extracție.")
        return
    
    print("Extragem datele din PDF...")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[0]
            tables = page.extract_tables()
            if tables:
                # Salvăm tabelul principal
                df1 = pd.DataFrame(tables[0]).dropna(how='all')
                df1.to_csv("cote_porturi.csv", index=False, header=False)
                
                if len(tables) > 1:
                    df2 = pd.DataFrame(tables[1]).dropna(how='all')
                    df2.to_csv("date_climatice.csv", index=False, header=False)
                print("Fișiere CSV create cu succes.")
    except Exception as e:
        print(f"Eroare la citirea PDF-ului: {e}")

if __name__ == "__main__":
    try:
        download_pdf()
        extract_data()
    except Exception as e:
        print(f"Eroare: {e}")
        exit(1)

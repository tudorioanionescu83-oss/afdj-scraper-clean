import pdfplumber
import pandas as pd
import os
from playwright.sync_api import sync_playwright

# Configurații
pdf_path = "cote_dunare.pdf"
url_pagina = "https://www.afdj.ro/ro/cotele-dunarii"
pdf_url = "https://www.afdj.ro/sites/default/files/bhcote.pdf"

def download_pdf():
    with sync_playwright() as p:
        print("Lansăm browserul în mod 'uman'...")
        # Folosim un browser real pentru a evita detectarea
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        
        try:
            # 1. Vizităm pagina principală (ajută la setarea cookie-urilor Cloudflare)
            print(f"Navigăm la pagina: {url_pagina}")
            page.goto(url_pagina, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(3000) # Așteptăm 3 secunde pentru procesele de fundal

            # 2. Încercăm să descărcăm prin click real pe link
            print("Căutăm link-ul către PDF și simulăm click...")
            
            with page.expect_download(timeout=60000) as download_info:
                # Selectorul caută orice link care conține 'bhcote.pdf'
                page.locator('a[href*="bhcote.pdf"]').first.click()
            
            download = download_info.value
            download.save_as(pdf_path)
            
            dimensiune = os.path.getsize(pdf_path)
            print(f"Succes! PDF descărcat. Dimensiune: {dimensiune} bytes")
            
            if dimensiune < 10000:
                print("Atenție: Fișierul este prea mic, s-ar putea să fie o pagină de eroare salvată ca PDF.")

        except Exception as e:
            print(f"Metoda prin click a eșuat: {e}")
            print("Încercăm metoda directă prin browser ca ultimă soluție...")
            
            # Fallback: navigăm direct la URL-ul PDF-ului
            response = page.goto(pdf_url)
            if response and response.status == 200:
                with open(pdf_path, 'wb') as f:
                    f.write(response.body())
                print("PDF salvat prin navigare directă.")
            else:
                status = response.status if response else "N/A"
                raise Exception(f"Blocaj total la descărcare. Status server: {status}")
        
        browser.close()

def extract_data():
    if not os.path.exists(pdf_path) or os.path.getsize(pdf_path) < 10000:
        print("Extracția a fost anulată: Fișierul PDF lipsește sau este invalid.")
        return

    print("Începem extracția datelor din PDF...")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[0]
            tables = page.extract_tables()
            
            if not tables:
                print("Nu s-au găsit tabele în PDF.")
                return

            # Salvăm primul tabel (Cote Porturi)
            df1 = pd.DataFrame(tables[0])
            df1.to_csv("cote_porturi.csv", index=False, header=False)
            print("Fișier generat: cote_porturi.csv")
            
            # Salvăm al doilea tabel (Date Climatice) dacă există
            if len(tables) > 1:
                df2 = pd.DataFrame(tables[1])
                df2.to_csv("date_climatice.csv", index=False, header=False)
                print("Fișier generat: date_climatice.csv")
                
    except Exception as e:
        print(f"Eroare la procesarea PDF-ului: {e}")

if __name__ == "__main__":
    try:
        download_pdf()
        extract_data()
        print("--- Proces finalizat cu succes ---")
    except Exception as e:
        print(f"--- Eroare critică în script: {e} ---")
        exit(1)

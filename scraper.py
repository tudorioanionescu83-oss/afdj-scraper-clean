import pdfplumber
import pandas as pd
import os
import sys
from playwright.sync_api import sync_playwright

pdf_path = "cote_dunare.pdf"
url_pagina = "https://www.afdj.ro/ro/cotele-dunarii"
pdf_url = "https://www.afdj.ro/sites/default/files/bhcote.pdf"

def download_pdf():
    with sync_playwright() as p:
        print("Lansăm browserul...")
        browser = p.chromium.launch(headless=True)
        # Browser context cu User-Agent de om
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            print(f"Navigăm la {url_pagina}...")
            page.goto(url_pagina, wait_until="networkidle", timeout=60000)
            
            print("Încercăm accesarea directă a fișierului...")
            # Navigăm direct la PDF
            response = page.goto(pdf_url, wait_until="networkidle")
            
            if response and response.status == 200:
                body = response.body()
                if len(body) > 10000: # Un PDF real are peste 10KB
                    with open(pdf_path, 'wb') as f:
                        f.write(body)
                    print(f"Succes! Fișier salvat: {len(body)} bytes")
                else:
                    print("Fișierul primit este prea mic. Probabil e un mesaj de eroare.")
                    raise Exception("403 Forbidden sau Blocaj Cloudflare detectat.")
            else:
                status = response.status if response else "Fără răspuns"
                print(f"Eroare status: {status}")
                raise Exception(f"Serverul a returnat status {status}")

        finally:
            browser.close()

def extract_data():
    if not os.path.exists(pdf_path) or os.path.getsize(pdf_path) < 10000:
        return

    print("Extragem datele din PDF...")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            table = pdf.pages[0].extract_table()
            if table:
                df = pd.DataFrame(table)
                df.to_csv("cote_porturi.csv", index=False, header=False)
                print("Fișier CSV generat cu succes!")
    except Exception as e:
        print(f"Eroare la procesarea tabelelor: {e}")

if __name__ == "__main__":
    try:
        download_pdf()
        extract_data()
    except Exception as e:
        print(f"Eroare script: {e}")
        sys.exit(1)

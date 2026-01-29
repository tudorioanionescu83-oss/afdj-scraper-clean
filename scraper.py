import pdfplumber
import pandas as pd
import os
import time
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

pdf_path = "cote_dunare.pdf"
url_pagina = "https://www.afdj.ro/ro/cotele-dunarii"
pdf_url = "https://www.afdj.ro/sites/default/files/bhcote.pdf"

def download_pdf():
    with sync_playwright() as p:
        print("Lansăm browserul în mod Stealth...")
        browser = p.chromium.launch(headless=True)
        # Setăm un profil de browser identic cu unul real
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        
        # Aplicăm masca de invizibilitate
        stealth_sync(page)
        
        print("Navigăm la pagină...")
        page.goto(url_pagina, wait_until="networkidle")
        
        # Așteptăm puțin pentru eventuale provocări Cloudflare invizibile
        time.sleep(5)
        
        print("Încercăm descărcarea directă a buffer-ului...")
        try:
            # Mergem la URL-ul PDF-ului direct în tab-ul deja verificat
            response = page.goto(pdf_url)
            
            if response and response.status == 200:
                with open(pdf_path, 'wb') as f:
                    f.write(response.body())
                print(f"Succes! PDF salvat ({os.path.getsize(pdf_path)} bytes)")
            else:
                print(f"Eroare status: {response.status if response else 'No Response'}")
                # Dacă tot dă 403, încercăm să forțăm un download prin JavaScript
                print("Încercăm forțarea prin JS...")
                content = page.evaluate("async (url) => { const r = await fetch(url); const b = await r.blob(); return await b.arrayBuffer(); }", pdf_url)
                # Aceasta este o metodă extremă de a citi fișierul prin browser
                # (Uneori necesită cod binar mai complex, dar testăm întâi statusul)
                raise Exception("Blocaj persistent.")
        except Exception as e:
            print(f"Eroare: {e}")
            raise
        finally:
            browser.close()

def extract_data():
    if not os.path.exists(pdf_path) or os.path.getsize(pdf_path) < 10000:
        return
    with pdfplumber.open(pdf_path) as pdf:
        tables = pdf.pages[0].extract_tables()
        if tables:
            pd.DataFrame(tables[0]).to_csv("cote_porturi.csv", index=False, header=False)
            print("Date extrase în cote_porturi.csv")

if __name__ == "__main__":
    try:
        download_pdf()
        extract_data()
    except:
        import sys
        sys.exit(1)

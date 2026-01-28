import pdfplumber
import pandas as pd
import os
import time
from playwright.sync_api import sync_playwright

pdf_path = "cote_dunare.pdf"
url_pagina = "https://www.afdj.ro/ro/cotele-dunarii"

def download_pdf():
    with sync_playwright() as p:
        print("Lansăm browserul...")
        browser = p.chromium.launch(headless=True)
        # Setăm un User Agent de browser real
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print(f"Navigăm la {url_pagina}...")
        page.goto(url_pagina, wait_until="networkidle")
        
        # Căutăm link-ul către PDF-ul bhcote.pdf
        link_selector = 'a[href*="bhcote.pdf"]'
        if page.is_visible(link_selector):
            print("Am găsit link-ul PDF. Descărcăm...")
            with page.expect_download() as download_info:
                page.click(link_selector)
            download = download_info.value
            download.save_as(pdf_path)
            print("PDF descărcat cu succes!")
        else:
            raise Exception("Nu am găsit link-ul către PDF în pagină.")
        
        browser.close()

def extract_data():
    if not os.path.exists(pdf_path):
        return
    
    print("Extragem datele din PDF...")
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        tables = page.extract_tables()
        if tables:
            pd.DataFrame(tables[0]).dropna(how='all').to_csv("cote_porturi.csv", index=False, header=False)
            if len(tables) > 1:
                pd.DataFrame(tables[1]).dropna(how='all').to_csv("date_climatice.csv", index=False, header=False)
            print("Fișiere CSV create.")

if __name__ == "__main__":
    try:
        download_pdf()
        extract_data()
    except Exception as e:
        print(f"Eroare: {e}")
        exit(1)

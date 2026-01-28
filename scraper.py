import pdfplumber
import pandas as pd
import os
from playwright.sync_api import sync_playwright

pdf_path = "cote_dunare.pdf"
# Mergem direct la sursa fisierului pe care il cautam
pdf_url = "https://www.afdj.ro/sites/default/files/bhcote.pdf"

def download_pdf_direct():
    with sync_playwright() as p:
        print("Lansăm browserul Chromium...")
        browser = p.chromium.launch(headless=True)
        # Simulam un browser de om normal
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print(f"Accesăm direct PDF-ul: {pdf_url}")
        
        # Incercam sa descarcam fisierul
        try:
            response = page.goto(pdf_url, timeout=60000)
            
            # Verificam daca am primit un PDF sau o eroare
            content_type = response.headers.get("content-type", "")
            
            if "application/pdf" in content_type or response.status_code == 200:
                with open(pdf_path, 'wb') as f:
                    f.write(response.body())
                print("PDF descarcat cu succes direct de la sursă!")
            else:
                print(f"Status primit: {response.status_code}")
                print(f"Content-Type: {content_type}")
                raise Exception("Serverul nu a trimis un PDF.")
                
        except Exception as e:
            # Daca direct nu merge, incercam sa "pacalim" referer-ul
            print("Incercăm metoda cu Referer...")
            page.goto("https://www.afdj.ro/ro/cotele-dunarii")
            page.wait_for_timeout(2000)
            response = page.goto(pdf_url)
            with open(pdf_path, 'wb') as f:
                f.write(response.body())
            print("PDF descarcat prin metoda Referer!")

        browser.close()

def extract_data():
    if not os.path.exists(pdf_path):
        return
    
    print("Extragem datele...")
    with pdfplumber.open(pdf_path) as pdf:
        # AFDJ are datele pe prima pagina
        page = pdf.pages[0]
        tables = page.extract_tables()
        if tables:
            # Tabel 1: Porturi/Cote
            df1 = pd.DataFrame(tables[0]).dropna(how='all')
            df1.to_csv("cote_porturi.csv", index=False, header=False)
            
            # Tabel 2: Clima (daca exista)
            if len(tables) > 1:
                df2 = pd.DataFrame(tables[1]).dropna(how='all')
                df2.to_csv("date_climatice.csv", index=False, header=False)
            print("Tabelele au fost salvate in CSV.")

if __name__ == "__main__":
    try:
        download_pdf_direct()
        extract_data()
    except Exception as e:
        print(f"Eroare: {e}")
        exit(1)

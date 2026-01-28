import pdfplumber
import pandas as pd
import requests
import base64
import os

# URL-ul tău de la Google Apps Script
GOOGLE_PROXY_URL = "https://script.google.com/macros/s/AKfycbzjyG2HOnUIo5IL_6TthlP55bbwWrh9wKj7FZ5zymaHXrnkW6fmAtvh4hMWu8YjpWnGLA/exec"
pdf_path = "cote_dunare.pdf"

def download_via_google():
    print("Cerem PDF-ul de la Google Proxy...")
    # Google face redirect (302), deci avem nevoie de allow_redirects=True (default în requests)
    response = requests.get(GOOGLE_PROXY_URL, timeout=60)
    
    if response.status_code == 200:
        if response.text.startswith("Eroare"):
            raise Exception(f"Google Script a raportat o eroare: {response.text}")
        
        # Decodăm conținutul Base64 primit de la Google înapoi în PDF binar
        try:
            pdf_content = base64.b64decode(response.text)
            with open(pdf_path, 'wb') as f:
                f.write(pdf_content)
            print("PDF descărcat și decodat cu succes!")
        except Exception as e:
            raise Exception(f"Eroare la decodarea Base64: {e}")
    else:
        raise Exception(f"Eroare HTTP la Google Proxy: {response.status_code}")

def extract_data():
    if not os.path.exists(pdf_path):
        print("Fișierul PDF lipsește!")
        return
    
    print("Începem extracția tabelelor...")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[0]
            tables = page.extract_tables()
            
            if not tables:
                print("Nu am găsit niciun tabel în PDF!")
                return

            # Tabelul 1: Cotele apelor Dunării
            df1 = pd.DataFrame(tables[0])
            df1 = df1.dropna(how='all') # Ștergem rândurile complet goale
            df1.to_csv("cote_porturi.csv", index=False, header=False)
            print("Salvat: cote_porturi.csv")
            
            # Tabelul 2: Temperaturi și precipitații
            if len(tables) > 1:
                df2 = pd.DataFrame(tables[1])
                df2 = df2.dropna(how='all')
                df2.to_csv("date_climatice.csv", index=False, header=False)
                print("Salvat: date_climatice.csv")
            else:
                print("Tabelul 2 nu a fost găsit pe prima pagină.")

    except Exception as e:
        print(f"Eroare la procesarea tabelelor: {e}")

if __name__ == "__main__":
    try:
        download_via_google()
        extract_data()
    except Exception as e:
        print(f"Eroare critică: {e}")
        exit(1)

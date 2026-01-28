import pdfplumber
import pandas as pd
import requests
import base64
import os

# URL-ul tau confirmat
GOOGLE_PROXY_URL = "https://script.google.com/macros/s/AKfycbzjyG2HOnUIo5IL_6TthlP55bbwWrh9wKj7FZ5zymaHXrnkW6fmAtvh4hMWu8YjpWnGLA/exec"
pdf_path = "cote_dunare.pdf"

def download_via_google():
    print("Cerem PDF-ul de la Google Proxy...")
    # Uneori Google are nevoie de cateva secunde sa propage schimbarile
    session = requests.Session()
    response = session.get(GOOGLE_PROXY_URL, allow_redirects=True, timeout=60)
    
    if response.status_code == 200:
        # Verificam daca am primit text Base64 sau o pagina de login/eroare
        raw_text = response.text.strip()
        
        if raw_text.startswith("<!DOCTYPE") or "login.google.com" in raw_text:
            raise Exception("Google cere autentificare. Asigura-te ca la 'Who has access' este selectat 'Anyone'.")
            
        if raw_text.startswith("Eroare"):
            raise Exception(f"Eroare in Google Script: {raw_text}")
        
        try:
            pdf_content = base64.b64decode(raw_text)
            with open(pdf_path, 'wb') as f:
                f.write(pdf_content)
            print("PDF descarcat si decodat cu succes!")
        except Exception as e:
            print(f"Eroare la decodare Base64. Primele caractere primite: {raw_text[:50]}")
            raise e
    else:
        print(f"Eroare HTTP {response.status_code}")
        print(f"Raspuns server: {response.text[:200]}")
        raise Exception("Google Proxy a refuzat cererea (403/404).")

def extract_data():
    if not os.path.exists(pdf_path):
        return

    print("Incepem extractia datelor din PDF...")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Luam prima pagina
            page = pdf.pages[0]
            tables = page.extract_tables()

            if not tables:
                print("Nu am gasit tabele.")
                return

            # Tabelul 1: Cote (curatam randurile goale)
            df1 = pd.DataFrame(tables[0]).dropna(how='all')
            df1.to_csv("cote_porturi.csv", index=False, header=False)
            print("Extras: cote_porturi.csv")

            # Tabelul 2: Clima (daca exista pe prima pagina)
            if len(tables) > 1:
                df2 = pd.DataFrame(tables[1]).dropna(how='all')
                df2.to_csv("date_climatice.csv", index=False, header=False)
                print("Extras: date_climatice.csv")
                
    except Exception as e:
        print(f"Eroare la procesarea PDF: {e}")

if __name__ == "__main__":
    try:
        download_via_google()
        extract_data()
    except Exception as e:
        print(f"Eroare critica: {e}")
        exit(1)

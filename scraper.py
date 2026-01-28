import pdfplumber
import pandas as pd
import os

pdf_path = "cote_dunare.pdf"

def extract_data():
    if not os.path.exists(pdf_path):
        print("Eroare: Fișierul PDF nu a fost găsit pe disc!")
        return

    try:
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[0]
            tables = page.extract_tables()

            if not tables:
                print("Nu s-au găsit tabele în PDF.")
                return

            # Tabelul 1: Cotele Dunării
            df_cote = pd.DataFrame(tables[0])
            # Curățăm puțin rândurile goale dacă există
            df_cote = df_cote.dropna(how='all')
            df_cote.to_csv("cote_porturi.csv", index=False, header=False)
            print("Extras Tabel 1 (Cote).")

            # Tabelul 2: Date Climatice
            if len(tables) > 1:
                df_clima = pd.DataFrame(tables[1])
                df_clima = df_clima.dropna(how='all')
                df_clima.to_csv("date_climatice.csv", index=False, header=False)
                print("Extras Tabel 2 (Clima).")

    except Exception as e:
        print(f"Eroare la procesarea PDF: {e}")

if __name__ == "__main__":
    extract_data()

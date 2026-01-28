import pdfplumber
import requests
import pandas as pd
import os
from datetime import datetime

# URL-ul PDF-ului
url = "https://www.afdj.ro/sites/default/files/bhcote.pdf"
pdf_path = "cote_dunare.pdf"

def download_pdf():
    response = requests.get(url)
    with open(pdf_path, 'wb') as f:
        f.write(response.content)

def extract_data():
    with pdfplumber.open(pdf_path) as pdf:
        # Tabelul 1: Cotele apelor (de obicei pe prima pagina)
        page1 = pdf.pages[0]
        table1 = page1.extract_table()
        df_cote = pd.DataFrame(table1[1:], columns=table1[0])
        df_cote.to_csv("cote_porturi.csv", index=False)

        # Tabelul 2: Temperaturi si Presiune
        # Nota: S-ar putea sa fie nevoie sa ajustezi indexul paginii daca tabelul e pe pagina 2
        page2 = pdf.pages[0] # Modifica in pdf.pages[1] daca e pe pagina a doua
        tables = page2.extract_tables()
        if len(tables) > 1:
            df_clima = pd.DataFrame(tables[1])
            df_clima.to_csv("date_climatice.csv", index=False)

if __name__ == "__main__":
    download_pdf()
    extract_data()
    print(f"Date actualizate la: {datetime.now()}")

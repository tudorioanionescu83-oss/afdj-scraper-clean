import pdfplumber
import pandas as pd
import re
import os

# Numele fișierului pe care l-ai descărcat
pdf_path = "bhcote.pdf"

def clean_val(val):
    """Curăță gunoiul de text și păstrează doar ultima valoare numerică din celulă"""
    if val is None or str(val).strip() == "": return None
    # Luăm doar ultimul rând din celulă (pentru valorile de azi) și eliminăm caracterele non-numerice
    last_line = str(val).split('\n')[-1]
    cleaned = re.sub(r'[^\d\.\-]', '', last_line)
    return cleaned if cleaned else None

def get_pdf_date(pdf):
    """Extrage data raportului direct din PDF"""
    first_page_text = pdf.pages[0].extract_text()
    match = re.search(r'DATA:\s*(.*)', first_page_text)
    return match.group(1).strip() if match else "Necunoscuta"

def run_scraper():
    if not os.path.exists(pdf_path):
        print(f"❌ Eroare: Nu gasesc fisierul {pdf_path} in folder!")
        return

    with pdfplumber.open(pdf_path) as pdf:
        raport_date = get_pdf_date(pdf)
        print(f"🚀 Procesez raportul AFDJ din data: {raport_date}")

        # --- 1. COTE PORTURI ROMANESTI (Pagina 1) ---
        p1 = pdf.pages[0]
        tables_p1 = p1.extract_tables()
        cote_data = []
        
        for table in tables_p1:
            # Identificăm tabelul corect după prezența portului "Bazias"
            if any("Bazias" in str(row) for row in table):
                for row in table[1:]:
                    if len(row) >= 6 and row[0]: # Localitate, Km, ..., Cota Azi
                        cote_data.append({
                            'Localitate': row[0].strip(),
                            'Km': clean_val(row[1]),
                            'Cota_cm': clean_val(row[5])
                        })
                break

        # --- 2. DATE METEO & TEMPERATURA APA (Pagina 2) ---
        p2 = pdf.pages[1]
        meteo_table = p2.extract_tables()[0]
        meteo_data = []

        # Sărim peste headere (primele 4 rânduri)
        for row in meteo_table[4:]:
            if len(row) >= 6 and row[0]:
                meteo_data.append({
                    'Localitate': row[0].strip().replace('\n', ' '),
                    'Temp_Min_Atm': clean_val(row[2]),
                    'Temp_Apa': clean_val(row[3]),
                    'Presiune_Hg': clean_val(row[5])
                })

        # --- 3. ADANCIMI MINIME SONDATE (Pagina 1 - Tabel mic) ---
        adancimi_data = []
        for table in tables_p1:
            if any("Bara Sulina" in str(row) for row in table):
                for row in table[1:]:
                    if len(row) >= 3:
                        adancimi_data.append({
                            'Sector': row[0].strip(),
                            'Adancime_m': clean_val(row[2])
                        })
                break

        # --- SALVARE FINALA ---
        pd.DataFrame(cote_data).to_csv("cote_romania.csv", index=False)
        pd.DataFrame(meteo_data).to_csv("meteo_romania.csv", index=False)
        pd.DataFrame(adancimi_data).to_csv("adancimi_minime.csv", index=False)

        print("-" * 50)
        print(f"✅ FINALIZAT!")
        print(f"📁 Salvat {len(cote_data)} porturi în 'cote_romania.csv'")
        print(f"📁 Salvat {len(meteo_data)} stații meteo în 'meteo_romania.csv'")
        print(f"📁 Salvat {len(adancimi_data)} sectoare adâncimi în 'adancimi_minime.csv'")
        print("-" * 50)

if __name__ == "__main__":
    run_scraper()

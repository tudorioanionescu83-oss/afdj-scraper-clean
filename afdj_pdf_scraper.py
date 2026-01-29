import pdfplumber
import pandas as pd
import re

pdf_path = "bhcote.pdf"

def clean_num(val):
    if val is None: return None
    # Elimina orice nu este cifra, punct sau minus [cite: 4, 8]
    cleaned = re.sub(r'[^\d\.\-]', '', str(val).split('\n')[-1])
    return cleaned if cleaned else None

def scrape_afdj_data():
    with pdfplumber.open(pdf_path) as pdf:
        # --- 1. EXTRACȚIE COTE PORTURI ROMÂNEȘTI (PAGINA 1) ---
        p1 = pdf.pages[0]
        tables_p1 = p1.extract_tables()
        cote_final = []

        # Căutăm tabelul care începe cu Bazias (Porturile Românești) 
        for table in tables_p1:
            if any("Bazias" in str(row) for row in table):
                # Header-ul este: Localitate, Km, 25.01, 26.01, 27.01, 28.01 
                for row in table[1:]: # Sărim peste capul de tabel
                    if row[0] and row[1]:
                        cote_final.append({
                            'Port': row[0].strip(),
                            'Km': clean_num(row[1]),
                            'Cota_cm_28_01': clean_num(row[5]) # Ultima coloana 
                        })
                break

        # --- 2. EXTRACȚIE DATE METEO (PAGINA 2) ---
        p2 = pdf.pages[1]
        meteo_table = p2.extract_tables()[0] # Primul tabel de pe pag. 2 
        meteo_final = []

        # Rândurile de date încep de la indexul 4 (după headerele complexe) 
        for row in meteo_table[4:]:
            if len(row) < 6 or not row[0]: continue
            
            # Datele sunt stivuite (26, 27, 28 ian). Luăm mereu ultima valoare 
            temp_atm = clean_num(row[2]) # Temp minima atm 
            temp_apa = clean_num(row[3]) # Temp apa 
            presiune = clean_num(row[5]) # Presiune atm 

            meteo_final.append({
                'Localitate': row[0].strip().replace('\n', ' '),
                'Temp_Atm_28_01': temp_atm,
                'Temp_Apa_28_01': temp_apa,
                'Presiune_Hg_28_01': presiune
            })

        # --- SALVARE REZULTATE ---
        pd.DataFrame(cote_final).to_csv("cote_romania.csv", index=False)
        pd.DataFrame(meteo_final).to_csv("meteo_romania.csv", index=False)
        
        print(f"✅ Extracție finalizată pentru data de {pdf.pages[0].extract_text().split('DATA:')[1].splitlines()[0].strip()}") # 
        print(f"📍 Porturi RO: {len(cote_final)} rânduri salvate în cote_romania.csv")
        print(f"🌡️ Meteo RO: {len(meteo_final)} rânduri salvate în meteo_romania.csv")

if __name__ == "__main__":
    try:
        scrape_afdj_data()
    except Exception as e:
        print(f"❌ Eroare: {e}")

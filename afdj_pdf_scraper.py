import pdfplumber
import pandas as pd
import re

pdf_path = "bhcote.pdf"

def clean_value(val):
    if val is None: return None
    # Curățăm caracterele speciale și spațiile
    val = re.sub(r'[^\d\.\-]', '', str(val).split('\n')[0])
    return val if val else None

def scrape_afdj_pdf():
    with pdfplumber.open(pdf_path) as pdf:
        # 1. Extracție Cote Porturi Românești (Pagina 1)
        p1 = pdf.pages[0]
        # Tabelul porturilor românești este de obicei al treilea pe prima pagină
        tables = p1.extract_tables()
        
        cote_data = []
        # Căutăm tabelul care conține "Bazias"
        for table in tables:
            if any("Bazias" in str(row) for row in table):
                df_cote = pd.DataFrame(table[1:], columns=['Localitate', 'Km', 'Data1', 'Data2', 'Data3', 'Data_Azi'])
                for _, row in df_cote.iterrows():
                    cote_data.append({
                        'Port': row['Localitate'],
                        'Km': row['Km'],
                        'Cota_28_01': clean_value(row['Data_Azi'])
                    })
                break

        # 2. Extracție Date Meteo (Pagina 2)
        p2 = pdf.pages[1]
        meteo_table = p2.extract_tables()[0]
        meteo_data = []

        # Parsăm tabelul meteo (structura complexă cu date multiple per celulă)
        for row in meteo_table[3:]: # Sărim peste headerele multiple
            if len(row) < 5: continue
            
            # Valorile meteo sunt adesea stivuite: 26.01 \n 27.01 \n 28.01
            temp_atm_raw = str(row[2]).split('\n')
            temp_apa_raw = str(row[3]).split('\n')
            presiune_raw = str(row[5]).split('\n')

            meteo_data.append({
                'Localitate': row[0],
                'Temp_Min_Atm_28_01': temp_atm_raw[-1].strip() if temp_atm_raw else None,
                'Temp_Apa_28_01': temp_apa_raw[-1].strip() if temp_apa_raw else None,
                'Presiune_28_01': presiune_raw[-1].strip() if presiune_raw else None
            })

        # Salvăm rezultatele
        df_final_cote = pd.DataFrame(cote_data)
        df_final_meteo = pd.DataFrame(meteo_data)
        
        df_final_cote.to_csv("cote_porturi_RO.csv", index=False)
        df_final_meteo.to_csv("date_meteo_RO.csv", index=False)
        
        print("✅ Extracție reușită!")
        print(f"Porturi procesate: {len(df_final_cote)}")
        print(f"Date meteo procesate: {len(df_final_meteo)}")

if __name__ == "__main__":
    scrape_afdj_pdf()

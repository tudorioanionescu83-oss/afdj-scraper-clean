"""
AFDJ PDF Scraper - Extrage date din buletinul zilnic
====================================================

PDF: https://www.afdj.ro/sites/default/files/bhcote.pdf
Update: Zilnic la 09:00

Extrage:
1. Cotele apelor Dunării în porturile românești (cm)
2. Temperaturi atmosferice, temperatura apei, presiune, precipitații
"""

import requests
import pdfplumber
import pandas as pd
import json
from datetime import datetime
from typing import Dict, List, Optional
import re

class AFDJPDFScraper:
    """Scraper pentru PDF-ul zilnic AFDJ"""
    
    def __init__(self):
        self.pdf_url = "https://www.afdj.ro/sites/default/files/bhcote.pdf"
        self.pdf_filename = "bhcote.pdf"
    
    def download_pdf(self) -> bool:
        """Descarcă PDF-ul zilnic"""
        try:
            print(f"📥 Downloading PDF from: {self.pdf_url}")
            response = requests.get(self.pdf_url, timeout=30)
            
            if response.status_code == 200:
                with open(self.pdf_filename, 'wb') as f:
                    f.write(response.content)
                print(f"✅ PDF downloaded: {len(response.content)} bytes")
                return True
            else:
                print(f"❌ HTTP Error {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error downloading PDF: {e}")
            return False
    
    def extract_cote_table(self, pdf) -> Optional[pd.DataFrame]:
        """
        Extrage tabelul cu cotele apelor
        
        Format:
        Localitate | km | 25.01 | 26.01 | 27.01 | 28.01
        """
        print("\n📊 Extracting: Cotele apelor...")
        
        for page_num, page in enumerate(pdf.pages, 1):
            # Extrage toate tabelele din pagină
            tables = page.extract_tables()
            
            for table_idx, table in enumerate(tables):
                if not table or len(table) < 2:
                    continue
                
                # Verifică dacă e tabelul cu cote (caută "Localitate" și "km" în header)
                header = table[0]
                header_text = ' '.join([str(cell) if cell else '' for cell in header]).lower()
                
                if 'localitate' in header_text and 'km' in header_text:
                    print(f"✅ Found cote table on page {page_num}, table {table_idx + 1}")
                    
                    # Creează DataFrame
                    df = pd.DataFrame(table[1:], columns=table[0])
                    
                    # Curăță datele
                    df = df.dropna(how='all')  # Elimină rânduri goale
                    df = df[df.iloc[:, 0].notna()]  # Păstrează doar rânduri cu localitate
                    
                    print(f"   Rows: {len(df)}, Columns: {len(df.columns)}")
                    return df
        
        print("⚠️  Cote table not found")
        return None
    
    def extract_meteo_table(self, pdf) -> Optional[pd.DataFrame]:
        """
        Extrage tabelul cu date meteorologice
        
        Format:
        Localități | Temp min atmosferică | Temp apei | Presiune atm | Precipitații
        """
        print("\n🌡️ Extracting: Date meteorologice...")
        
        for page_num, page in enumerate(pdf.pages, 1):
            tables = page.extract_tables()
            
            for table_idx, table in enumerate(tables):
                if not table or len(table) < 2:
                    continue
                
                # Verifică dacă e tabelul meteo (caută "temperatura" sau "atmosferica")
                header = table[0]
                header_text = ' '.join([str(cell) if cell else '' for cell in header]).lower()
                
                if 'temperatura' in header_text and 'atmosferica' in header_text:
                    print(f"✅ Found meteo table on page {page_num}, table {table_idx + 1}")
                    
                    # Acest tabel are multi-level headers, trebuie procesat diferit
                    # Pentru simplitate, vom lua primul rând ca header
                    df = pd.DataFrame(table[1:], columns=table[0])
                    df = df.dropna(how='all')
                    df = df[df.iloc[:, 0].notna()]
                    
                    print(f"   Rows: {len(df)}, Columns: {len(df.columns)}")
                    return df
        
        print("⚠️  Meteo table not found")
        return None
    
    def process_cote_data(self, df: pd.DataFrame) -> List[Dict]:
        """Procesează datele despre cote"""
        if df is None or df.empty:
            return []
        
        print("\n🔧 Processing cote data...")
        
        result = []
        
        # Identifică coloanele
        columns = df.columns.tolist()
        print(f"   Columns: {columns}")
        
        # Primul coloană = Localitate, a doua = km, restul = date
        localitate_col = columns[0]
        km_col = columns[1]
        date_cols = columns[2:]  # Toate coloanele cu date
        
        for idx, row in df.iterrows():
            try:
                localitate = str(row[localitate_col]).strip()
                
                # Sari peste rânduri invalide
                if not localitate or localitate == 'nan' or len(localitate) < 2:
                    continue
                
                # Extrage km
                km_raw = str(row[km_col])
                km = int(re.sub(r'[^\d]', '', km_raw)) if km_raw and km_raw != 'nan' else None
                
                # Extrage cotele pentru fiecare dată
                cote = {}
                for date_col in date_cols:
                    if date_col and date_col != 'nan':
                        cota_raw = str(row[date_col])
                        # Extrage doar cifrele
                        if cota_raw and cota_raw != 'nan':
                            cota_cleaned = re.sub(r'[^\d-]', '', cota_raw)
                            if cota_cleaned:
                                try:
                                    cote[str(date_col)] = int(cota_cleaned)
                                except ValueError:
                                    cote[str(date_col)] = None
                
                # Ia ultima cotă disponibilă
                ultima_cota = None
                ultima_data = None
                if cote:
                    ultima_data = list(cote.keys())[-1]
                    ultima_cota = cote[ultima_data]
                
                port_data = {
                    'localitate': localitate,
                    'km': km,
                    'cota_cm': ultima_cota,
                    'data_cota': ultima_data,
                    'istoric_cote': cote,
                    'timestamp_scraping': datetime.now().isoformat()
                }
                
                result.append(port_data)
                print(f"  ✓ {localitate}: {ultima_cota} cm (la {ultima_data})")
                
            except Exception as e:
                print(f"  ⚠️  Error processing row {idx}: {e}")
                continue
        
        return result
    
    def save_to_json(self, data: Dict, filename: str = "cote_pdf.json"):
        """Salvează datele în JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Saved: {filename}")
    
    def save_to_csv(self, ports: List[Dict], filename: str = "cote_pdf.csv"):
        """Salvează datele în CSV"""
        if not ports:
            return
        
        # Flatten istoricul pentru CSV
        rows = []
        for port in ports:
            row = {
                'localitate': port['localitate'],
                'km': port['km'],
                'cota_cm': port['cota_cm'],
                'data_cota': port['data_cota']
            }
            rows.append(row)
        
        df = pd.DataFrame(rows)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"💾 Saved: {filename}")
    
    def scrape(self) -> Optional[Dict]:
        """Pipeline complet de scraping"""
        print("🚀 Starting AFDJ PDF Scraper\n")
        print("="*80)
        
        # 1. Descarcă PDF
        if not self.download_pdf():
            return None
        
        # 2. Deschide PDF
        try:
            with pdfplumber.open(self.pdf_filename) as pdf:
                print(f"\n📄 PDF opened: {len(pdf.pages)} pages")
                
                # 3. Extrage tabelul cu cote
                cote_df = self.extract_cote_table(pdf)
                
                # 4. Extrage tabelul meteo (opțional)
                meteo_df = self.extract_meteo_table(pdf)
                
                # 5. Procesează datele
                ports_data = []
                if cote_df is not None:
                    ports_data = self.process_cote_data(cote_df)
                
                if not ports_data:
                    print("\n❌ No data extracted!")
                    return None
                
                # 6. Creează structura finală
                result = {
                    'source': 'AFDJ PDF',
                    'pdf_url': self.pdf_url,
                    'timestamp': datetime.now().isoformat(),
                    'count': len(ports_data),
                    'ports': ports_data
                }
                
                if meteo_df is not None:
                    result['meteo_available'] = True
                    result['meteo_rows'] = len(meteo_df)
                
                print("\n" + "="*80)
                print(f"✅ Successfully scraped {len(ports_data)} ports")
                print("="*80)
                
                # 7. Salvează rezultatele
                self.save_to_json(result)
                self.save_to_csv(ports_data)
                
                # 8. Preview
                print("\n" + "="*80)
                print("DATA PREVIEW")
                print("="*80)
                df_preview = pd.DataFrame(ports_data)
                print(df_preview[['localitate', 'km', 'cota_cm', 'data_cota']].head(10))
                
                return result
                
        except Exception as e:
            print(f"\n❌ Error processing PDF: {e}")
            import traceback
            traceback.print_exc()
            return None


def main():
    """Exemplu de utilizare"""
    
    scraper = AFDJPDFScraper()
    data = scraper.scrape()
    
    if data:
        print(f"\n✅ Scraping completed!")
        print(f"📊 Total ports: {data['count']}")
        
        # Găsește cota maximă
        ports = data['ports']
        if ports:
            max_port = max(ports, key=lambda x: x['cota_cm'] or 0)
            print(f"🏆 Highest: {max_port['localitate']} - {max_port['cota_cm']} cm")
            
            min_port = min(ports, key=lambda x: x['cota_cm'] or 999999)
            print(f"📉 Lowest: {min_port['localitate']} - {min_port['cota_cm']} cm")
    else:
        print("\n❌ Scraping failed!")


if __name__ == "__main__":
    main()

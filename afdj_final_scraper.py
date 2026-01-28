"""
AFDJ Custom Scraper - Bazat pe structura reală a tabelului
===========================================================

Structura identificată:
- Localitate (Port): Sulina, Tulcea, etc.
- KM: kilometraj (0, 71, 103, etc.)
- Cotă: nivelul apei în cm
- Variația: schimbarea în cm (-12, +5, etc.)
- Temperatura: temperatura apei în °C
- Data actualizare: când au fost actualizate datele
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime
from typing import Optional, Dict, List

class AFDJCoteScraper:
    """Scraper pentru cotele Dunării de pe AFDJ.ro"""
    
    def __init__(self):
        self.url = "https://www.afdj.ro/ro/cotele-dunarii"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ro-RO,ro;q=0.9,en;q=0.8',
            'Referer': 'https://www.afdj.ro/ro'
        }
    
    def fetch_page(self) -> Optional[str]:
        """Descarcă pagina HTML de la AFDJ"""
        try:
            print(f"📥 Fetching data from: {self.url}")
            response = requests.get(self.url, headers=self.headers, timeout=20)
            
            if response.status_code == 200:
                print(f"✅ Page downloaded successfully ({len(response.content)} bytes)")
                return response.text
            else:
                print(f"❌ HTTP Error {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            return None
    
    def parse_cote_data(self, html: str) -> List[Dict]:
        """
        Parsează HTML-ul și extrage datele despre cote
        
        Structura așteptată:
        <td class="views-field views-field-field-localitatea">Sulina</td>
        <td class="views-field views-field-field-km">0</td>
        <td class="views-field views-field-field-cota">80 cm</td>
        <td class="views-field views-field-field-variatia">-12</td>
        <td class="views-field views-field-field-temperatura-masurata">2,0 °C</td>
        <td class="views-field views-field-field-field-data-actualiz-cote"><time>28/01/2026</time></td>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        cote_data = []
        
        # Găsește toate rândurile din tabel (fiecare rând = un port)
        # Căutăm după td-uri cu class-ul specific pentru localitate
        localitate_cells = soup.find_all('td', class_='views-field-field-localitatea')
        
        print(f"\n📊 Found {len(localitate_cells)} ports in the table")
        
        for cell in localitate_cells:
            try:
                # Găsește rândul părinte (tr)
                row = cell.find_parent('tr')
                
                if not row:
                    continue
                
                # Extrage datele din fiecare coloană
                localitate_td = row.find('td', class_='views-field-field-localitatea')
                km_td = row.find('td', class_='views-field-field-km')
                cota_td = row.find('td', class_='views-field-field-cota')
                variatia_td = row.find('td', class_='views-field-field-variatia')
                temp_td = row.find('td', class_='views-field-field-temperatura-masurata')
                data_td = row.find('td', class_='views-field-field-field-data-actualiz-cote')
                
                # Curăță și extrage textul
                localitate = localitate_td.get_text(strip=True) if localitate_td else None
                km = km_td.get_text(strip=True) if km_td else None
                cota = cota_td.get_text(strip=True) if cota_td else None
                variatia = variatia_td.get_text(strip=True) if variatia_td else None
                temperatura = temp_td.get_text(strip=True) if temp_td else None
                
                # Extrage data din tag-ul <time>
                data_actualizare = None
                if data_td:
                    time_tag = data_td.find('time')
                    if time_tag:
                        data_actualizare = time_tag.get_text(strip=True)
                
                # Extrage prognozele (tendințe 24h-120h)
                tendinta_24h_td = row.find('td', class_='views-field-field-tendinta-24h')
                tendinta_48h_td = row.find('td', class_='views-field-field-tendinta-48h')
                tendinta_72h_td = row.find('td', class_='views-field-field-tendinta-72h')
                tendinta_96h_td = row.find('td', class_='views-field-field-tendinta-96h')
                tendinta_120h_td = row.find('td', class_='views-field-field-tendinta-120h')
                
                tendinta_24h = tendinta_24h_td.get_text(strip=True) if tendinta_24h_td else None
                tendinta_48h = tendinta_48h_td.get_text(strip=True) if tendinta_48h_td else None
                tendinta_72h = tendinta_72h_td.get_text(strip=True) if tendinta_72h_td else None
                tendinta_96h = tendinta_96h_td.get_text(strip=True) if tendinta_96h_td else None
                tendinta_120h = tendinta_120h_td.get_text(strip=True) if tendinta_120h_td else None
                
                # Extrage data actualizării prognozelor
                data_prognoze_td = row.find('td', class_='views-field-field-data-actualizare-prognoze')
                data_actualizare_prognoze = None
                if data_prognoze_td:
                    time_tag = data_prognoze_td.find('time')
                    if time_tag:
                        data_actualizare_prognoze = time_tag.get_text(strip=True)
                
                # Procesează valorile pentru a extrage doar numerele
                cota_cm = None
                if cota:
                    # Extrage numărul din "80 cm"
                    cota_cm = int(''.join(filter(str.isdigit, cota)))
                
                variatia_cm = None
                if variatia:
                    # Extrage numărul din "-12" sau "+5"
                    try:
                        variatia_cm = int(variatia.replace('+', '').strip())
                    except ValueError:
                        variatia_cm = None
                
                km_int = None
                if km:
                    try:
                        km_int = int(km)
                    except ValueError:
                        km_int = None
                
                temp_celsius = None
                if temperatura:
                    # Extrage numărul din "2,0 °C"
                    temp_str = temperatura.replace('°C', '').replace(',', '.').strip()
                    try:
                        temp_celsius = float(temp_str)
                    except ValueError:
                        temp_celsius = None
                
                # Determină tendința
                tendinta = "stabil"
                if variatia_cm:
                    if variatia_cm > 0:
                        tendinta = "creștere"
                    elif variatia_cm < 0:
                        tendinta = "scădere"
                
                # Creează obiectul cu date
                port_data = {
                    'localitate': localitate,
                    'km': km_int,
                    'cota_cm': cota_cm,
                    'cota_text': cota,
                    'variatia_cm': variatia_cm,
                    'tendinta': tendinta,
                    'temperatura_celsius': temp_celsius,
                    'temperatura_text': temperatura,
                    'data_actualizare': data_actualizare,
                    # Prognoze
                    'prognoza_24h': tendinta_24h or '',
                    'prognoza_48h': tendinta_48h or '',
                    'prognoza_72h': tendinta_72h or '',
                    'prognoza_96h': tendinta_96h or '',
                    'prognoza_120h': tendinta_120h or '',
                    'data_actualizare_prognoze': data_actualizare_prognoze,
                    'timestamp_scraping': datetime.now().isoformat()
                }
                
                cote_data.append(port_data)
                
                print(f"  ✓ {localitate}: {cota_cm} cm ({tendinta} {variatia_cm} cm)")
                
            except Exception as e:
                print(f"  ⚠️  Error parsing row: {e}")
                continue
        
        return cote_data
    
    def save_to_json(self, data: List[Dict], filename: str = "cote_dunare.json"):
        """Salvează datele în format JSON"""
        output = {
            'source': 'AFDJ',
            'url': self.url,
            'timestamp': datetime.now().isoformat(),
            'count': len(data),
            'ports': data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Data saved to: {filename}")
    
    def save_to_csv(self, data: List[Dict], filename: str = "cote_dunare.csv"):
        """Salvează datele în format CSV"""
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"💾 Data saved to: {filename}")
    
    def save_to_excel(self, data: List[Dict], filename: str = "cote_dunare.xlsx"):
        """Salvează datele în format Excel"""
        df = pd.DataFrame(data)
        
        # Formatare mai frumoasă pentru Excel
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Cote Dunare', index=False)
            
            # Auto-ajustează lățimea coloanelor
            worksheet = writer.sheets['Cote Dunare']
            for idx, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).apply(len).max(),
                    len(col)
                ) + 2
                worksheet.column_dimensions[chr(65 + idx)].width = max_length
        
        print(f"💾 Data saved to: {filename}")
    
    def scrape(self, export_format: str = 'all') -> Optional[List[Dict]]:
        """
        Pipeline complet de scraping
        
        Args:
            export_format: 'json', 'csv', 'excel', sau 'all'
        
        Returns:
            Lista cu date despre porturi sau None dacă a eșuat
        """
        print("🚀 Starting AFDJ Cote Scraper\n")
        print("="*80)
        
        # 1. Descarcă pagina
        html = self.fetch_page()
        
        if not html:
            print("\n❌ Could not download page!")
            print("\nPossible solutions:")
            print("  1. Check your internet connection")
            print("  2. Try using a VPN if site is blocked")
            print("  3. Use Selenium/Playwright for JavaScript rendering")
            print("  4. Use the PDF scraper as alternative")
            return None
        
        # 2. Parsează datele
        print("\n" + "="*80)
        cote_data = self.parse_cote_data(html)
        
        if not cote_data:
            print("\n❌ No data found in page!")
            print("The HTML structure might have changed.")
            return None
        
        print("\n" + "="*80)
        print(f"✅ Successfully scraped {len(cote_data)} ports")
        print("="*80)
        
        # 3. Exportă datele
        if export_format in ['json', 'all']:
            self.save_to_json(cote_data)
        
        if export_format in ['csv', 'all']:
            self.save_to_csv(cote_data)
        
        if export_format in ['excel', 'all']:
            try:
                self.save_to_excel(cote_data)
            except Exception as e:
                print(f"⚠️  Could not save Excel: {e}")
        
        # 4. Afișează preview
        print("\n" + "="*80)
        print("DATA PREVIEW")
        print("="*80)
        df = pd.DataFrame(cote_data)
        print(df[['localitate', 'cota_cm', 'variatia_cm', 'tendinta', 'temperatura_celsius']])
        
        return cote_data


def main():
    """Exemplu de utilizare"""
    
    # Creează scraper-ul
    scraper = AFDJCoteScraper()
    
    # Rulează scraping-ul și exportă în toate formatele
    data = scraper.scrape(export_format='all')
    
    if data:
        print("\n✅ Scraping completed successfully!")
        print(f"📊 Total ports scraped: {len(data)}")
        
        # Exemplu: găsește portul cu cota cea mai mare
        max_port = max(data, key=lambda x: x['cota_cm'] or 0)
        print(f"\n🏆 Highest water level: {max_port['localitate']} - {max_port['cota_cm']} cm")
        
        # Exemplu: găsește portul cu cota cea mai mică
        min_port = min(data, key=lambda x: x['cota_cm'] or 999999)
        print(f"📉 Lowest water level: {min_port['localitate']} - {min_port['cota_cm']} cm")
        
    else:
        print("\n❌ Scraping failed!")


if __name__ == "__main__":
    main()

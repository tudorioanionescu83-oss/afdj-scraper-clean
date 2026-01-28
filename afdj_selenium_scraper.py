"""
AFDJ Scraper cu Selenium - Pentru bypass Cloudflare
====================================================

Folosește Selenium cu undetected-chromedriver pentru a bypassa
protecția Cloudflare și a extrage datele din tabel.

Instalare necesară:
pip install selenium undetected-chromedriver
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import pandas as pd
import json
from datetime import datetime
from typing import List, Dict, Optional
import time

class AFDJSeleniumScraper:
    """Scraper cu Selenium pentru AFDJ - bypass Cloudflare"""
    
    def __init__(self, headless: bool = True):
        self.url = "https://www.afdj.ro/ro/cotele-dunarii"
        self.headless = headless
        self.driver = None
    
    def init_driver(self):
        """Inițializează browserul Selenium cu undetected-chromedriver"""
        print("🌐 Initializing browser...")
        
        options = uc.ChromeOptions()
        
        if self.headless:
            options.add_argument('--headless=new')
        
        # Opțiuni pentru a evita detectarea
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # User agent real
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        try:
            self.driver = uc.Chrome(options=options)
            print("✅ Browser initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Error initializing browser: {e}")
            return False
    
    def fetch_page(self) -> bool:
        """Încarcă pagina și așteaptă să se încarce datele"""
        try:
            print(f"\n📥 Loading page: {self.url}")
            self.driver.get(self.url)
            
            # Așteaptă ca pagina să se încarce complet
            print("⏳ Waiting for page to load...")
            time.sleep(3)  # Așteaptă 3 secunde pentru JavaScript
            
            # Verifică dacă am fost blocați de Cloudflare
            if "checking your browser" in self.driver.page_source.lower():
                print("🛡️  Cloudflare detected, waiting...")
                time.sleep(5)
            
            # Așteaptă ca tabelul să apară
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "views-field-field-localitatea"))
                )
                print("✅ Table loaded successfully")
                return True
            except Exception as e:
                print(f"⚠️  Timeout waiting for table: {e}")
                # Încearcă oricum, poate datele sunt încărcate
                return True
                
        except Exception as e:
            print(f"❌ Error loading page: {e}")
            return False
    
    def extract_data(self) -> List[Dict]:
        """Extrage datele din tabelul HTML"""
        print("\n📊 Extracting data from table...")
        
        cote_data = []
        
        try:
            # Găsește toate rândurile din tabel
            rows = self.driver.find_elements(By.CSS_SELECTOR, "tr.views-row")
            
            if not rows:
                # Încearcă alt selector
                rows = self.driver.find_elements(By.TAG_NAME, "tr")
            
            print(f"Found {len(rows)} rows")
            
            for idx, row in enumerate(rows, 1):
                try:
                    # Caută celulele cu datele
                    localitate_elem = row.find_elements(By.CSS_SELECTOR, ".views-field-field-localitatea")
                    km_elem = row.find_elements(By.CSS_SELECTOR, ".views-field-field-km")
                    cota_elem = row.find_elements(By.CSS_SELECTOR, ".views-field-field-cota")
                    variatia_elem = row.find_elements(By.CSS_SELECTOR, ".views-field-field-variatia")
                    temp_elem = row.find_elements(By.CSS_SELECTOR, ".views-field-field-temperatura-masurata")
                    data_elem = row.find_elements(By.CSS_SELECTOR, ".views-field-field-field-data-actualiz-cote")
                    
                    # Prognoze
                    tendinta_24h_elem = row.find_elements(By.CSS_SELECTOR, ".views-field-field-tendinta-24h")
                    tendinta_48h_elem = row.find_elements(By.CSS_SELECTOR, ".views-field-field-tendinta-48h")
                    tendinta_72h_elem = row.find_elements(By.CSS_SELECTOR, ".views-field-field-tendinta-72h")
                    tendinta_96h_elem = row.find_elements(By.CSS_SELECTOR, ".views-field-field-tendinta-96h")
                    tendinta_120h_elem = row.find_elements(By.CSS_SELECTOR, ".views-field-field-tendinta-120h")
                    data_prognoze_elem = row.find_elements(By.CSS_SELECTOR, ".views-field-field-data-actualizare-prognoze")
                    
                    # Verifică dacă am găsit date
                    if not localitate_elem:
                        continue
                    
                    # Extrage textul
                    localitate = localitate_elem[0].text.strip() if localitate_elem else None
                    km = km_elem[0].text.strip() if km_elem else None
                    cota = cota_elem[0].text.strip() if cota_elem else None
                    variatia = variatia_elem[0].text.strip() if variatia_elem else None
                    temperatura = temp_elem[0].text.strip() if temp_elem else None
                    data_actualizare = data_elem[0].text.strip() if data_elem else None
                    
                    # Prognoze
                    tendinta_24h = tendinta_24h_elem[0].text.strip() if tendinta_24h_elem else ''
                    tendinta_48h = tendinta_48h_elem[0].text.strip() if tendinta_48h_elem else ''
                    tendinta_72h = tendinta_72h_elem[0].text.strip() if tendinta_72h_elem else ''
                    tendinta_96h = tendinta_96h_elem[0].text.strip() if tendinta_96h_elem else ''
                    tendinta_120h = tendinta_120h_elem[0].text.strip() if tendinta_120h_elem else ''
                    data_actualizare_prognoze = data_prognoze_elem[0].text.strip() if data_prognoze_elem else None
                    
                    # Sari peste rânduri goale
                    if not localitate or not cota:
                        continue
                    
                    # Procesează valorile
                    cota_cm = int(''.join(filter(str.isdigit, cota))) if cota else None
                    
                    variatia_cm = None
                    if variatia:
                        try:
                            variatia_cm = int(variatia.replace('+', '').strip())
                        except ValueError:
                            pass
                    
                    km_int = int(km) if km and km.isdigit() else None
                    
                    temp_celsius = None
                    if temperatura:
                        temp_str = temperatura.replace('°C', '').replace(',', '.').strip()
                        try:
                            temp_celsius = float(temp_str)
                        except ValueError:
                            pass
                    
                    # Determină tendința
                    tendinta = "stabil"
                    if variatia_cm:
                        tendinta = "creștere" if variatia_cm > 0 else "scădere"
                    
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
                        'prognoza_24h': tendinta_24h,
                        'prognoza_48h': tendinta_48h,
                        'prognoza_72h': tendinta_72h,
                        'prognoza_96h': tendinta_96h,
                        'prognoza_120h': tendinta_120h,
                        'data_actualizare_prognoze': data_actualizare_prognoze,
                        'timestamp_scraping': datetime.now().isoformat()
                    }
                    
                    cote_data.append(port_data)
                    print(f"  ✓ {localitate}: {cota_cm} cm")
                    
                except Exception as e:
                    print(f"  ⚠️  Error parsing row {idx}: {e}")
                    continue
            
            return cote_data
            
        except Exception as e:
            print(f"❌ Error extracting data: {e}")
            return []
    
    def save_screenshot(self, filename: str = "afdj_page.png"):
        """Salvează un screenshot al paginii pentru debugging"""
        try:
            self.driver.save_screenshot(filename)
            print(f"📸 Screenshot saved: {filename}")
        except Exception as e:
            print(f"⚠️  Could not save screenshot: {e}")
    
    def close(self):
        """Închide browserul"""
        if self.driver:
            self.driver.quit()
            print("🔒 Browser closed")
    
    def scrape(self, save_screenshot: bool = False) -> Optional[List[Dict]]:
        """Pipeline complet de scraping"""
        print("🚀 Starting AFDJ Selenium Scraper\n")
        print("="*80)
        
        try:
            # 1. Inițializează browser
            if not self.init_driver():
                return None
            
            # 2. Încarcă pagina
            if not self.fetch_page():
                return None
            
            # 3. Salvează screenshot (opțional)
            if save_screenshot:
                self.save_screenshot()
            
            # 4. Extrage datele
            data = self.extract_data()
            
            if not data:
                print("\n❌ No data extracted!")
                return None
            
            print("\n" + "="*80)
            print(f"✅ Successfully scraped {len(data)} ports")
            print("="*80)
            
            return data
            
        finally:
            # Închide browserul întotdeauna
            self.close()


def main():
    """Exemplu de utilizare"""
    
    # Creează scraper-ul (headless=False pentru debugging)
    scraper = AFDJSeleniumScraper(headless=True)
    
    # Rulează scraping-ul
    data = scraper.scrape(save_screenshot=True)
    
    if data:
        # Salvează datele
        output = {
            'source': 'AFDJ',
            'timestamp': datetime.now().isoformat(),
            'count': len(data),
            'ports': data
        }
        
        # JSON
        with open('cote_selenium.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print("\n💾 Data saved to: cote_selenium.json")
        
        # CSV
        df = pd.DataFrame(data)
        df.to_csv('cote_selenium.csv', index=False, encoding='utf-8')
        print("💾 Data saved to: cote_selenium.csv")
        
        # Preview
        print("\n" + "="*80)
        print("DATA PREVIEW")
        print("="*80)
        print(df[['localitate', 'cota_cm', 'variatia_cm', 'tendinta']].head(10))
        
    else:
        print("\n❌ Scraping failed!")


if __name__ == "__main__":
    main()

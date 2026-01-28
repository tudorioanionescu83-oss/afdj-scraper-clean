# 🌊 AFDJ Dunărea - Scraper Suite Complet

Soluție completă pentru extragerea datelor despre **cotele Dunării** de pe site-ul AFDJ.ro (Administrația Fluvială a Dunării de Jos).

## 📋 Ce date extrage?

Pentru fiecare din cele **23 de porturi** de pe Dunăre:

✅ **Date actuale:**
- Localitate (Sulina, Tulcea, Galați, etc.)
- Kilometraj de la gura Dunării
- **Cota apei** în centimetri
- **Variația** față de ziua precedentă
- **Tendința** (creștere/scădere/stabil)
- **Temperatura apei** în grade Celsius
- Data actualizării

✅ **Prognoze:**
- Prognoza la 24h
- Prognoza la 48h
- Prognoza la 72h
- Prognoza la 96h
- Prognoza la 120h (5 zile)
- Data actualizării prognozelor

---

## 🚀 Quick Start

### Instalare dependințe:

```bash
# Pentru scraper simplu (RECOMAND SĂ ÎNCEPI CU ACESTA)
pip install requests beautifulsoup4 pandas openpyxl lxml

# Pentru Selenium (dacă primul nu funcționează din cauza Cloudflare)
pip install selenium undetected-chromedriver pandas
```

### Rulare:

```bash
# Metoda 1: Scraper simplu (încercă prima dată)
python afdj_final_scraper.py

# Metoda 2: Cu Selenium (dacă Metoda 1 e blocată de Cloudflare)
python afdj_selenium_scraper.py
```

### Output:

```
📂 cote_dunare.json   - Date în format JSON
📂 cote_dunare.csv    - Date în format CSV
📂 cote_dunare.xlsx   - Date în format Excel
```

---

## 📦 Fișiere incluse

### 1. `afdj_final_scraper.py` ⭐ **RECOMAND**

**Scraper simplu cu requests + BeautifulSoup**

✅ Avantaje:
- Rapid și eficient
- Nu necesită browser
- Consum redus de resurse
- Cod simplu de înțeles

❌ Dezavantaje:
- Poate fi blocat de Cloudflare

**Utilizare:**
```python
from afdj_final_scraper import AFDJCoteScraper

scraper = AFDJCoteScraper()
data = scraper.scrape(export_format='all')  # json, csv, excel, sau all
```

---

### 2. `afdj_selenium_scraper.py` 🚀 **PENTRU CLOUDFLARE**

**Scraper cu Selenium pentru bypass Cloudflare**

✅ Avantaje:
- Bypass automat Cloudflare
- Funcționează pentru pagini JavaScript complexe
- Poate face screenshot pentru debugging

❌ Dezavantaje:
- Mai lent (trebuie să încarce browser)
- Necesită Chrome instalat
- Consum mai mare de resurse

**Utilizare:**
```python
from afdj_selenium_scraper import AFDJSeleniumScraper

scraper = AFDJSeleniumScraper(headless=True)
data = scraper.scrape(save_screenshot=True)
```

---

### 3. `data_structure_examples.py` 📚 **DOCUMENTAȚIE**

**Exemple și documentație completă**

Conține:
- Structura detaliată a datelor
- Exemple de analiză
- Exemple de export grafic
- Integrare cu baze de date
- API REST cu Flask
- Notificări Telegram
- Sistem de alertă pentru cote critice

---

## 📊 Structura datelor

### Exemplu JSON output:

```json
{
  "source": "AFDJ",
  "url": "https://www.afdj.ro/ro/cotele-dunarii",
  "timestamp": "2026-01-28T10:30:00",
  "count": 23,
  "ports": [
    {
      "localitate": "Sulina",
      "km": 0,
      "cota_cm": 80,
      "cota_text": "80 cm",
      "variatia_cm": -12,
      "tendinta": "scădere",
      "temperatura_celsius": 2.0,
      "temperatura_text": "2,0 °C",
      "data_actualizare": "28/01/2026",
      "prognoza_24h": "scădere 5-15 cm",
      "prognoza_48h": "scădere 10-20 cm",
      "prognoza_72h": "scădere 5-15 cm",
      "prognoza_96h": "stabilizare",
      "prognoza_120h": "stabilizare",
      "data_actualizare_prognoze": "27/01/2026",
      "timestamp_scraping": "2026-01-28T10:30:00.123456"
    },
    ...
  ]
}
```

---

## 🎯 Cazuri de utilizare

### 1. Monitorizare simplă

```python
from afdj_final_scraper import AFDJCoteScraper

scraper = AFDJCoteScraper()
data = scraper.scrape()

# Găsește cota maximă
max_port = max(data, key=lambda x: x['cota_cm'])
print(f"Cea mai mare cotă: {max_port['localitate']} - {max_port['cota_cm']} cm")
```

### 2. Salvare în bază de date

```python
import sqlite3
import pandas as pd

# Rulează scraper
data = scraper.scrape()
df = pd.DataFrame(data)

# Salvează în SQLite
conn = sqlite3.connect('cote_dunare.db')
df.to_sql('cote', conn, if_exists='append', index=False)
conn.close()
```

### 3. Sistem de alertă

```python
COTE_ATENTIE = {'Sulina': 250, 'Tulcea': 550, 'Galați': 650}

data = scraper.scrape()
for port in data:
    if port['localitate'] in COTE_ATENTIE:
        if port['cota_cm'] >= COTE_ATENTIE[port['localitate']]:
            print(f"🚨 ALERTĂ: {port['localitate']} - Cotă de atenție depășită!")
```

### 4. Grafic cu evoluția cotelor

```python
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('cote_dunare.csv')
df_sorted = df.sort_values('km')

plt.figure(figsize=(15, 6))
plt.plot(df_sorted['km'], df_sorted['cota_cm'], marker='o')
plt.xlabel('Kilometraj (km)')
plt.ylabel('Cota (cm)')
plt.title('Cotele Dunării')
plt.grid(True)
plt.savefig('cote_grafic.png')
```

### 5. API REST cu Flask

```python
from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/api/cote')
def get_cote():
    df = pd.read_csv('cote_dunare.csv')
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/cote/<localitate>')
def get_cota_port(localitate):
    df = pd.read_csv('cote_dunare.csv')
    port = df[df['localitate'] == localitate]
    return jsonify(port.iloc[0].to_dict())

app.run(port=5000)
```

---

## 🔄 Automatizare

### Cron job (Linux/Mac) - rulare zilnică la 06:00

```bash
crontab -e

# Adaugă:
0 6 * * * cd /path/to/scraper && python3 afdj_final_scraper.py
```

### Task Scheduler (Windows)

```powershell
# PowerShell script: run_scraper.ps1
cd C:\path\to\scraper
python afdj_final_scraper.py

# Creează task în Task Scheduler:
# - Trigger: Daily la 06:00
# - Action: Run powershell.exe -File run_scraper.ps1
```

### Python script cu schedule

```python
import schedule
import time
from afdj_final_scraper import AFDJCoteScraper

def job():
    print("Running scraper...")
    scraper = AFDJCoteScraper()
    scraper.scrape()
    print("Done!")

# Rulează în fiecare zi la 06:00
schedule.every().day.at("06:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## 🐛 Troubleshooting

### Problema: "Failed to download page" sau Cloudflare blocking

**Soluție 1:** Folosește Selenium scraper-ul
```bash
python afdj_selenium_scraper.py
```

**Soluție 2:** Adaugă delay între request-uri
```python
import time
time.sleep(5)  # Așteaptă 5 secunde înainte de fiecare request
```

**Soluție 3:** Folosește un VPN sau proxy

### Problema: "No data found in page"

**Cauze posibile:**
1. Structura HTML-ului s-a schimbat
2. Site-ul e offline
3. Cloudflare blocking

**Soluție:** Verifică manual pagina în browser și compară cu codul scraper-ului

### Problema: Selenium - "Chrome not found"

**Soluție:**
```bash
# Instalează Chrome
# Ubuntu/Debian:
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb

# MacOS:
brew install --cask google-chrome

# Windows: Descarcă de pe google.com/chrome
```

---

## 📈 Performance

### afdj_final_scraper.py (requests)
- ⚡ Timp execuție: ~2-5 secunde
- 💾 Memorie: ~50 MB
- 🌐 Network: 1 request HTTP

### afdj_selenium_scraper.py
- ⏱️ Timp execuție: ~10-15 secunde
- 💾 Memorie: ~200-300 MB
- 🌐 Network: Multiple requests + JavaScript

---

## 🔐 Considerații legale

- Datele de pe AFDJ.ro sunt **publice**
- Scraping-ul este permis pentru **uz personal/cercetare**
- **NU** face request-uri prea frecvente (max 1/minut)
- **NU** folosi datele comercial fără permisiune
- Respectă `robots.txt` și Terms of Service

---

## 🤝 Contribuții

Îmbunătățiri sugerate:
- [ ] Adăugare istoricizare date (database time-series)
- [ ] Dashboard web cu Streamlit/Dash
- [ ] Notificări email/SMS pentru alerte
- [ ] Predicții ML pentru evoluția cotelor
- [ ] Comparație cu date meteo

---

## 📞 Support

Dacă întâmpini probleme:

1. **Verifică** că ai toate dependințele instalate
2. **Testează** manual site-ul AFDJ în browser
3. **Încearcă** Selenium scraper-ul dacă primul nu funcționează
4. **Verifică** că ai internet funcțional

---

## 📝 Changelog

### v1.0 - 28.01.2026
- ✅ Scraper initial cu requests + BeautifulSoup
- ✅ Scraper alternativ cu Selenium
- ✅ Extragere date complete (cote + prognoze)
- ✅ Export în JSON, CSV, Excel
- ✅ Documentație completă
- ✅ Exemple de utilizare

---

## ⭐ Quick Reference

```bash
# Instalare
pip install requests beautifulsoup4 pandas openpyxl lxml

# Rulare simplă
python afdj_final_scraper.py

# Rulare cu Selenium (pentru Cloudflare)
pip install selenium undetected-chromedriver
python afdj_selenium_scraper.py

# Verificare output
cat cote_dunare.json
# sau
import pandas as pd
df = pd.read_csv('cote_dunare.csv')
print(df.head())
```

---

**🌊 Succes la monitorizarea Dunării! 🚢**

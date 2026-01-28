[EXAMPLES.md](https://github.com/user-attachments/files/24903803/EXAMPLES.md)
# 📚 Exemple de utilizare AFDJ Scraper

Acest folder conține exemple practice pentru a începe rapid cu scraper-ul AFDJ.

---

## 📋 Fișierele din acest folder

### 1. `simple_usage.py` ⭐ **Începe aici!**

**Exemple simple și rapide pentru început:**

```bash
cd examples
python simple_usage.py
```

**Ce include:**
- ✅ Utilizare de bază
- 🏆 Găsirea cotelor extreme (max/min)
- 📉 Porturi în scădere
- 📈 Porturi în creștere
- 📊 Statistici generale
- 💾 Export în formate diferite
- 🔍 Filtrare după criterii

---

### 2. `alerts_system.py` 🚨 **Sistem de alertă**

**Monitorizare avansată cu alerte pentru cote critice:**

```bash
python alerts_system.py
```

**Funcționalități:**
- 🚨 Detectare automată cote de atenție
- 🔴 Detectare cote de inundație
- 💾 Salvare alerte în JSON
- 📧 Integrare email (template)
- 💬 Integrare Telegram (template)

**Praguri configurate:**
- Sulina, Tulcea, Isaccea
- Galați, Brăila, Hârșova
- Cernavodă, Călărași, Oltenița, Giurgiu

---

### 3. `data_structure_examples.py` 💡 **Exemple avansate**

**Cod complex pentru integrări:**

**Include:**
- 📊 Analiza datelor cu pandas
- 📈 Creare grafice cu matplotlib
- 🗄️ Integrare cu baze de date (SQLite)
- 🌐 API REST cu Flask
- 🤖 Notificări Telegram
- 📧 Notificări email
- 🔄 Comparație date istorice
- 📉 Exemple de vizualizare

---

## 🚀 Quick Start

### Instalare dependințe:

```bash
# Dependințe de bază
pip install requests beautifulsoup4 pandas openpyxl lxml

# Pentru grafice (opțional)
pip install matplotlib seaborn

# Pentru API REST (opțional)
pip install flask

# Pentru Telegram (opțional)
pip install python-telegram-bot
```

---

## 💡 Cazuri de utilizare

### 1️⃣ **Verificare rapidă a cotelor**

```python
import sys
sys.path.append('..')
from afdj_final_scraper import AFDJCoteScraper

scraper = AFDJCoteScraper()
data = scraper.scrape()

# Afișează toate cotele
for port in data:
    print(f"{port['localitate']:20s}: {port['cota_cm']:4d} cm")
```

---

### 2️⃣ **Sistem de alertă personalizat**

```python
from alerts_system import AlertSystem

# Creează sistem
alert = AlertSystem()

# Verifică alerte
alert.check_alerts()
alert.print_alerts()

# Salvează în fișier
alert.save_alerts_to_file('my_alerts.json')
```

---

### 3️⃣ **Analiză cu pandas**

```python
import pandas as pd
from afdj_final_scraper import AFDJCoteScraper

scraper = AFDJCoteScraper()
data = scraper.scrape()

# Creează DataFrame
df = pd.DataFrame(data)

# Statistici
print(df.describe())
print(df[df['tendinta'] == 'creștere'])

# Top 5 cote maxime
print(df.nlargest(5, 'cota_cm')[['localitate', 'cota_cm']])
```

---

### 4️⃣ **Export grafic**

```python
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('../cote_dunare.csv')
df_sorted = df.sort_values('km')

plt.figure(figsize=(15, 6))
plt.plot(df_sorted['km'], df_sorted['cota_cm'], marker='o', linewidth=2)
plt.xlabel('Kilometraj de la Sulina (km)')
plt.ylabel('Cota apei (cm)')
plt.title('Cotele Dunării - Profil longitudinal')
plt.grid(True, alpha=0.3)
plt.savefig('cote_profil.png', dpi=300)
```

---

### 5️⃣ **Salvare în bază de date**

```python
import sqlite3
import pandas as pd

# Scrape date
scraper = AFDJCoteScraper()
data = scraper.scrape()
df = pd.DataFrame(data)

# Salvează în SQLite
conn = sqlite3.connect('cote_dunare.db')
df.to_sql('cote', conn, if_exists='append', index=False)
conn.close()

print("✅ Date salvate în baza de date!")
```

---

## 🔄 Automatizare

### Cron job (Linux/Mac)

Rulează scraper-ul automat în fiecare zi la 06:00:

```bash
crontab -e

# Adaugă:
0 6 * * * cd /path/to/examples && python simple_usage.py
```

### Task Scheduler (Windows)

Creează un task care rulează zilnic:
1. Deschide Task Scheduler
2. Create Basic Task
3. Trigger: Daily at 06:00
4. Action: Start a program → `python.exe`
5. Arguments: `C:\path\to\examples\simple_usage.py`

---

## 📖 Documentație suplimentară

- [README principal](../README.md) - Documentație completă
- [Workflows GitHub Actions](../.github/WORKFLOWS.md) - Automatizare
- [Site AFDJ](https://www.afdj.ro) - Sursa datelor

---

## 🤝 Contribuții

Ai idei pentru exemple noi? 

1. Fork repo-ul
2. Creează un exemplu nou în `examples/`
3. Documentează-l clar
4. Trimite un pull request

---

## 📝 Tips & Tricks

### Tip 1: Filtrare rapidă
```python
# Porturile cu variație mare
df[abs(df['variatia_cm']) > 15]

# Porturile reci
df[df['temperatura_celsius'] < 5]

# Porturile în creștere
df[df['tendinta'] == 'creștere'].sort_values('variatia_cm', ascending=False)
```

### Tip 2: Comparație între zile
```python
df_azi = pd.read_csv('cote_2026_01_28.csv')
df_ieri = pd.read_csv('cote_2026_01_27.csv')

merged = df_azi.merge(df_ieri[['localitate', 'cota_cm']], 
                      on='localitate', 
                      suffixes=('_azi', '_ieri'))
merged['delta_24h'] = merged['cota_cm_azi'] - merged['cota_cm_ieri']
```

### Tip 3: Notificare simplă
```python
if any(p['cota_cm'] > 700 for p in data):
    print("🚨 ALERTĂ: Cotă mare detectată!")
    # Trimite email/SMS/Telegram
```

---

**🌊 Succes cu monitorizarea Dunării! 🚢**

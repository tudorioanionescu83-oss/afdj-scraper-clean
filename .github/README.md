# 🤖 GitHub Actions Workflows

Acest folder conține workflow-uri GitHub Actions pentru automatizarea scraping-ului.

## 📋 Workflow-uri disponibile

### 1. `scrape-daily.yml` - Scraping automat zilnic

**Trigger:** Zilnic la 06:00 UTC (08:00 Romanian time)

**Ce face:**
- Rulează scraper-ul automat în fiecare zi
- Salvează rezultatele ca artifacts (păstrate 90 zile)
- Commit automat rezultatele în folder `data/`
- Organizează datele pe an/lună

**Rulare manuală:**
- Mergi la tab-ul "Actions" pe GitHub
- Selectează "Scrape AFDJ Daily"
- Click "Run workflow"

---

### 2. `scrape-on-demand.yml` - Scraping la cerere

**Trigger:** Manual (prin GitHub UI)

**Ce face:**
- Permite rulare manuală cu opțiuni personalizate
- Alege formatul de export (json, csv, excel, all)
- Salvează rezultatele ca artifacts (păstrate 30 zile)
- Afișează rezumat în GitHub UI

**Cum să rulezi:**
1. Mergi la tab-ul "Actions"
2. Selectează "Scrape AFDJ On-Demand"
3. Click "Run workflow"
4. Alege formatul dorit
5. Click "Run workflow" verde

---

### 3. `test-scraper.yml` - Testare automată

**Trigger:** 
- La fiecare push pe `main` sau `develop`
- La fiecare pull request
- Manual

**Ce face:**
- Testează scraper-ul pe Python 3.9, 3.10, 3.11, 3.12
- Verifică dacă scraper-ul se inițializează corect
- Încearcă să facă scraping (cu timeout)
- Salvează rezultatele pentru debugging

---

## 📊 Cum să vezi rezultatele

### Artifacts (Fișiere generate)

1. Mergi la tab-ul "Actions"
2. Click pe un workflow run
3. Scroll jos la secțiunea "Artifacts"
4. Download ZIP-ul cu rezultatele

### Date istorice (dacă ai activat commit-ul)

Datele sunt salvate în:
```
data/
├── 2026/
│   ├── 01/
│   │   ├── cote_dunare_20260128.json
│   │   └── cote_dunare_20260129.json
│   └── 02/
│       └── ...
```

---

## ⚙️ Configurare

### Activare workflow-uri

Workflow-urile se activează automat când le push-ui pe GitHub.

### Dezactivare workflow

Dacă nu vrei să ruleze automat:
1. Mergi la `.github/workflows/scrape-daily.yml`
2. Șterge sau comentează secțiunea `schedule:`
3. Commit și push

### Modificare orar

Pentru a schimba ora de rulare:
```yaml
schedule:
  # Format: minute hour * * *
  # Exemplu pentru 10:00 UTC:
  - cron: '0 10 * * *'
```

### Modificare frecvență

```yaml
# Rulează la fiecare 6 ore
- cron: '0 */6 * * *'

# Rulează doar Luni-Vineri
- cron: '0 6 * * 1-5'

# Rulează de 2 ori pe zi (06:00 și 18:00)
- cron: '0 6,18 * * *'
```

---

## 🔐 Permissions

Workflow-urile au nevoie de:
- ✅ `contents: write` - pentru commit automat
- ✅ `actions: write` - pentru artifacts

Aceste permisiuni sunt configurate automat de GitHub.

---

## 📝 Notificări

Pentru a primi notificări când workflow-urile eșuează:

1. Mergi la Settings → Notifications
2. Secțiunea "Actions"
3. Bifează "Send notifications for failed workflows"

---

## 🐛 Debugging

Dacă un workflow eșuează:

1. Click pe workflow-ul roșu
2. Click pe job-ul care a eșuat
3. Expandează step-ul cu eroare
4. Vezi log-urile complete

Tips:
- Dacă AFDJ e down, workflow-ul va eșua (normal)
- Cloudflare blocking poate cauza erori
- Verifică artifacts pentru rezultate parțiale

---

## 💡 Use Cases

### 1. Monitorizare continuă
Folosește `scrape-daily.yml` pentru colectare automată de date

### 2. Analiză punctuală
Folosește `scrape-on-demand.yml` când vrei date fresh acum

### 3. Development
Folosește `test-scraper.yml` pentru a testa modificările

---

## 🚀 Workflow avansat (opțional)

Pentru notificări Telegram/Email când sunt cote critice:

```yaml
- name: Check for alerts
  run: |
    python examples/alerts_system.py
    
- name: Send notification
  if: failure()
  # Adaugă aici logica de notificare
```

---

**🌊 Happy Scraping! 🚢**

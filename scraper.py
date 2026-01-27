# ... (păstrează imports + STATIONS + insert_data)

def scrape_afdj():
    print(f"🚀 DEBUG AFDJ - {datetime.now()}")
    r = requests.get(AFDJ_URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # DEBUG: Toate tabelele de pe pagină!
    all_tables = soup.find_all('table')
    print(f"📊 Găsite {len(all_tables)} tabele:")
    for i, table in enumerate(all_tables):
        text_preview = table.get_text()[:200]
        print(f"  Tabel {i}: {text_preview}...")
        if 'Galati' in text_preview or 'Tulcea' in text_preview:
            print(f"  🎯 Tabel {i} CANDIDAT!")
    
    # Ia PRIMUL tabel care conține 'Galati'
    table = None
    for t in all_tables:
        if 'Galati' in t.get_text():
            table = t
            print("✅ Tabel SELECTAT!")
            break
    
    if not table:
        print("❌ NICIUN tabel cu 'Galati'!")
        return
    
    # Restul codului tău (rows, parsing...)
    rows = table.find_all('tr')[1:]
    # ... (păstrează parsing-ul exact)

"""
DOCUMENTAȚIE: Structura Datelor AFDJ
=====================================

Acest fișier documentează structura completă a datelor extrase din site-ul AFDJ.

TABELUL HTML conține următoarele coloane pentru fiecare port:
"""

# Exemplu de date complete pentru un port
exemplu_port = {
    # Date de bază
    'localitate': 'Sulina',                    # Numele portului
    'km': 0,                                   # Kilometrajul de la gura Dunării
    
    # Cota actuală
    'cota_cm': 80,                             # Cota în centimetri (număr)
    'cota_text': '80 cm',                      # Cota ca text original
    
    # Variația față de ziua precedentă
    'variatia_cm': -12,                        # Variația în cm (pozitiv=creștere, negativ=scădere)
    'tendinta': 'scădere',                     # Tendința: "creștere", "scădere", "stabil"
    
    # Temperatura
    'temperatura_celsius': 2.0,                # Temperatura apei în grade Celsius
    'temperatura_text': '2,0 °C',              # Temperatura ca text original
    
    # Date actualizare
    'data_actualizare': '28/01/2026',          # Data măsurării cotei
    
    # PROGNOZE - Tendințe pentru următoarele 5 zile
    'prognoza_24h': 'scădere 5-15 cm',         # Prognoza la 24 ore
    'prognoza_48h': 'scădere 10-20 cm',        # Prognoza la 48 ore
    'prognoza_72h': 'scădere 5-15 cm',         # Prognoza la 72 ore
    'prognoza_96h': 'stabilizare',             # Prognoza la 96 ore
    'prognoza_120h': 'stabilizare',            # Prognoza la 120 ore
    'data_actualizare_prognoze': '27/01/2026', # Data actualizării prognozelor
    
    # Metadata
    'timestamp_scraping': '2026-01-28T10:30:00.123456'  # Când au fost extrase datele
}

# Lista completă a porturilor de pe Dunăre (în ordinea kilometrajului)
porturi_dunare = [
    {'nume': 'Sulina', 'km': 0, 'sector': 'Delta'},
    {'nume': 'Tulcea', 'km': 71, 'sector': 'Delta'},
    {'nume': 'Isaccea', 'km': 103, 'sector': 'Maritim'},
    {'nume': 'Galați', 'km': 150, 'sector': 'Maritim'},
    {'nume': 'Brăila', 'km': 170, 'sector': 'Maritim'},
    {'nume': 'Hârșova', 'km': 253, 'sector': 'Fluvial'},
    {'nume': 'Cernavodă', 'km': 300, 'sector': 'Fluvial'},
    {'nume': 'Călărași', 'km': 370, 'sector': 'Fluvial'},
    {'nume': 'Oltenița', 'km': 430, 'sector': 'Fluvial'},
    {'nume': 'Giurgiu', 'km': 493, 'sector': 'Fluvial'},
    {'nume': 'Zimnicea', 'km': 554, 'sector': 'Fluvial'},
    {'nume': 'Turnu Măgurele', 'km': 597, 'sector': 'Fluvial'},
    {'nume': 'Corabia', 'km': 630, 'sector': 'Fluvial'},
    {'nume': 'Bechet', 'km': 679, 'sector': 'Fluvial'},
    {'nume': 'Rast', 'km': 738, 'sector': 'Fluvial'},
    {'nume': 'Calafat', 'km': 795, 'sector': 'Fluvial'},
    {'nume': 'Cetate', 'km': 811, 'sector': 'Fluvial'},
    {'nume': 'Gruia', 'km': 851, 'sector': 'Fluvial'},
    {'nume': 'Drobeta Turnu Severin', 'km': 931, 'sector': 'Fluvial'},
    {'nume': 'Orșova', 'km': 954, 'sector': 'Defileul Dunării'},
    {'nume': 'Drencova', 'km': 1015, 'sector': 'Defileul Dunării'},
    {'nume': 'Moldova Veche', 'km': 1048, 'sector': 'Defileul Dunării'},
    {'nume': 'Baziaș', 'km': 1072, 'sector': 'Defileul Dunării'},
]

"""
EXEMPLE DE UTILIZARE
====================
"""

import json
import pandas as pd

def exemplu_analiza_date():
    """Exemple de analiză pe datele extrase"""
    
    # Presupunem că am rulat scraper-ul și avem datele
    with open('cote_dunare.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    ports = data['ports']
    df = pd.DataFrame(ports)
    
    # 1. Găsește portul cu cota cea mai mare
    max_port = df.loc[df['cota_cm'].idxmax()]
    print(f"Cota maximă: {max_port['localitate']} - {max_port['cota_cm']} cm")
    
    # 2. Găsește portul cu cota cea mai mică
    min_port = df.loc[df['cota_cm'].idxmin()]
    print(f"Cota minimă: {min_port['localitate']} - {min_port['cota_cm']} cm")
    
    # 3. Găsește porturile în creștere
    in_crestere = df[df['tendinta'] == 'creștere']
    print(f"\nPorturi în creștere: {len(in_crestere)}")
    print(in_crestere[['localitate', 'cota_cm', 'variatia_cm']])
    
    # 4. Găsește porturile în scădere
    in_scadere = df[df['tendinta'] == 'scădere']
    print(f"\nPorturi în scădere: {len(in_scadere)}")
    print(in_scadere[['localitate', 'cota_cm', 'variatia_cm']])
    
    # 5. Calculează media cotelor
    medie = df['cota_cm'].mean()
    print(f"\nCota medie pe Dunăre: {medie:.2f} cm")
    
    # 6. Găsește porturile cu temperatură sub 5°C
    frig = df[df['temperatura_celsius'] < 5]
    print(f"\nPorturi cu apă rece (<5°C): {len(frig)}")
    
    # 7. Porturile cu cea mai mare variație
    df_sorted = df.sort_values('variatia_cm', key=abs, ascending=False)
    print(f"\nTop 5 variații:")
    print(df_sorted[['localitate', 'variatia_cm']].head())

def exemplu_export_grafic():
    """Exemplu de creare grafic cu matplotlib"""
    import matplotlib.pyplot as plt
    
    # Încarcă datele
    df = pd.read_csv('cote_dunare.csv')
    
    # Sortează după kilometraj
    df_sorted = df.sort_values('km')
    
    # Creează grafic
    plt.figure(figsize=(15, 6))
    plt.plot(df_sorted['km'], df_sorted['cota_cm'], marker='o', linewidth=2)
    plt.xlabel('Kilometraj de la Sulina (km)')
    plt.ylabel('Cota apei (cm)')
    plt.title('Cotele Dunării - {}'.format(pd.Timestamp.now().strftime('%d.%m.%Y')))
    plt.grid(True, alpha=0.3)
    
    # Adaugă etichete pentru fiecare port
    for idx, row in df_sorted.iterrows():
        plt.annotate(
            row['localitate'], 
            (row['km'], row['cota_cm']),
            textcoords="offset points",
            xytext=(0,10),
            ha='center',
            fontsize=8,
            rotation=45
        )
    
    plt.tight_layout()
    plt.savefig('cote_dunare_grafic.png', dpi=300)
    print("Grafic salvat: cote_dunare_grafic.png")

def exemplu_comparatie_istorica():
    """Exemplu de comparație între două date"""
    
    # Presupunem că avem date din două zile diferite
    df_azi = pd.read_csv('cote_dunare_2026-01-28.csv')
    df_ieri = pd.read_csv('cote_dunare_2026-01-27.csv')
    
    # Merge pe localitate
    df_comparatie = df_azi.merge(
        df_ieri[['localitate', 'cota_cm']], 
        on='localitate', 
        suffixes=('_azi', '_ieri')
    )
    
    # Calculează schimbarea
    df_comparatie['schimbare_24h'] = df_comparatie['cota_cm_azi'] - df_comparatie['cota_cm_ieri']
    
    # Porturile cu cele mai mari creșteri
    print("Top creșteri în 24h:")
    print(df_comparatie.nlargest(5, 'schimbare_24h')[['localitate', 'schimbare_24h']])
    
    # Porturile cu cele mai mari scăderi
    print("\nTop scăderi în 24h:")
    print(df_comparatie.nsmallest(5, 'schimbare_24h')[['localitate', 'schimbare_24h']])

def exemplu_alerta():
    """Exemplu de sistem de alertă pentru cote critice"""
    
    # Cote de atenție (exemplu - verifică pe site AFDJ pentru valori reale)
    cote_atentie = {
        'Sulina': 250,
        'Tulcea': 550,
        'Galați': 650,
        'Brăila': 650,
        'Călărași': 650,
        'Giurgiu': 650,
    }
    
    # Încarcă datele curente
    df = pd.read_csv('cote_dunare.csv')
    
    # Verifică pentru alerte
    for idx, row in df.iterrows():
        localitate = row['localitate']
        cota = row['cota_cm']
        
        if localitate in cote_atentie:
            cota_atentie_val = cote_atentie[localitate]
            
            if cota >= cota_atentie_val:
                print(f"🚨 ALERTĂ: {localitate} - Cota de atenție depășită!")
                print(f"   Cota curentă: {cota} cm")
                print(f"   Cota de atenție: {cota_atentie_val} cm")
                print(f"   Diferență: +{cota - cota_atentie_val} cm")

"""
INTEGRARE CU ALTE SISTEME
=========================
"""

def exemplu_api_rest():
    """Exemplu de creare API REST cu Flask"""
    from flask import Flask, jsonify
    
    app = Flask(__name__)
    
    @app.route('/api/cote', methods=['GET'])
    def get_all_cote():
        """Returnează toate cotele"""
        df = pd.read_csv('cote_dunare.csv')
        return jsonify(df.to_dict(orient='records'))
    
    @app.route('/api/cote/<localitate>', methods=['GET'])
    def get_cota_port(localitate):
        """Returnează cota pentru un port specific"""
        df = pd.read_csv('cote_dunare.csv')
        port_data = df[df['localitate'] == localitate]
        
        if len(port_data) == 0:
            return jsonify({'error': 'Port not found'}), 404
        
        return jsonify(port_data.iloc[0].to_dict())
    
    # app.run(debug=True, port=5000)

def exemplu_baza_de_date():
    """Exemplu de salvare în bază de date SQLite"""
    import sqlite3
    from datetime import datetime
    
    # Conectare la bază de date
    conn = sqlite3.connect('cote_dunare.db')
    cursor = conn.cursor()
    
    # Creează tabel
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cote (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            localitate TEXT NOT NULL,
            km INTEGER,
            cota_cm INTEGER,
            variatia_cm INTEGER,
            tendinta TEXT,
            temperatura_celsius REAL,
            data_actualizare TEXT,
            prognoza_24h TEXT,
            prognoza_48h TEXT,
            prognoza_72h TEXT,
            prognoza_96h TEXT,
            prognoza_120h TEXT,
            timestamp_scraping TEXT
        )
    ''')
    
    # Încarcă date din CSV
    df = pd.read_csv('cote_dunare.csv')
    
    # Inserează în bază de date
    df.to_sql('cote', conn, if_exists='append', index=False)
    
    conn.commit()
    conn.close()
    
    print("Date salvate în bază de date SQLite")

def exemplu_notificare_telegram():
    """Exemplu de trimitere notificări pe Telegram"""
    import requests
    
    TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN'
    TELEGRAM_CHAT_ID = 'YOUR_CHAT_ID'
    
    def send_telegram_message(message):
        url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
        data = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        requests.post(url, data=data)
    
    # Încarcă datele
    df = pd.read_csv('cote_dunare.csv')
    
    # Găsește porturile cu variații mari
    variatii_mari = df[abs(df['variatia_cm']) > 20]
    
    if len(variatii_mari) > 0:
        message = "🌊 <b>Alerte Cote Dunare</b>\n\n"
        for idx, row in variatii_mari.iterrows():
            emoji = "📈" if row['variatia_cm'] > 0 else "📉"
            message += f"{emoji} <b>{row['localitate']}</b>: "
            message += f"{row['cota_cm']} cm ({row['variatia_cm']:+d} cm)\n"
        
        send_telegram_message(message)

if __name__ == "__main__":
    print(__doc__)
    print("\n" + "="*80)
    print("STRUCTURA EXEMPLU PORT:")
    print("="*80)
    print(json.dumps(exemplu_port, indent=2, ensure_ascii=False))
    
    print("\n" + "="*80)
    print("LISTA PORTURI:")
    print("="*80)
    for port in porturi_dunare:
        print(f"  {port['km']:4d} km - {port['nume']:25s} ({port['sector']})")

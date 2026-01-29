"""
Generează grafice din datele JSON
==================================

Rulează după afdj_pdf_scraper.py pentru a crea grafice
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime

def load_data(filename='cote_pdf.json'):
    """Încarcă datele din JSON"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_profil(df, output_dir='reports'):
    """Generează profilul longitudinal"""
    print("📊 Generating: Profil longitudinal...")
    
    fig, ax = plt.subplots(figsize=(16, 8))
    df_sorted = df.sort_values('km')
    
    ax.plot(df_sorted['km'], df_sorted['cota_cm'], 
            marker='o', linewidth=2.5, markersize=8, 
            color='#2E86AB', label='Cota actuală')
    ax.fill_between(df_sorted['km'], 0, df_sorted['cota_cm'], 
                    alpha=0.3, color='#2E86AB')
    
    # Etichete pentru porturi
    for idx, row in df_sorted.iterrows():
        ax.annotate(row['localitate'], 
                   xy=(row['km'], row['cota_cm']),
                   xytext=(0, 10), textcoords='offset points',
                   ha='center', fontsize=9, rotation=45)
    
    ax.set_xlabel('Kilometraj de la Sulina (km)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Cota apei (cm)', fontsize=12, fontweight='bold')
    ax.set_title(f'Profil Longitudinal Dunărea - {datetime.now().strftime("%d.%m.%Y")}', 
                fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(fontsize=10)
    
    plt.tight_layout()
    output_file = Path(output_dir) / 'profil_longitudinal.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Saved: {output_file}")

def generate_variatii(df, output_dir='reports'):
    """Generează graficul cu variații"""
    print("📊 Generating: Variații...")
    
    # Calculează variația între ultima și penultima zi
    variatii = []
    for idx, row in df.iterrows():
        istoric = row.get('istoric_cote', {})
        if len(istoric) >= 2:
            dates = sorted(istoric.keys())
            ultima = istoric[dates[-1]]
            penultima = istoric[dates[-2]]
            if ultima and penultima:
                variatii.append(ultima - penultima)
            else:
                variatii.append(0)
        else:
            variatii.append(0)
    
    df['variatie'] = variatii
    df_sorted = df.sort_values('km')
    
    fig, ax = plt.subplots(figsize=(14, 8))
    colors = ['#E63946' if v < 0 else '#06D6A0' if v > 0 else '#FFB703' 
             for v in df_sorted['variatie']]
    
    bars = ax.bar(range(len(df_sorted)), df_sorted['variatie'], color=colors)
    ax.set_xticks(range(len(df_sorted)))
    ax.set_xticklabels(df_sorted['localitate'], rotation=45, ha='right')
    ax.set_ylabel('Variație (cm)', fontsize=12, fontweight='bold')
    ax.set_title(f'Variații Cote - {datetime.now().strftime("%d.%m.%Y")}', 
                fontsize=16, fontweight='bold', pad=20)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    
    # Legendă
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#E63946', label='Scădere'),
        Patch(facecolor='#06D6A0', label='Creștere'),
        Patch(facecolor='#FFB703', label='Stabil')
    ]
    ax.legend(handles=legend_elements, loc='best', fontsize=10)
    
    plt.tight_layout()
    output_file = Path(output_dir) / 'variatii.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Saved: {output_file}")

def generate_stats(df, output_dir='reports'):
    """Generează statistici"""
    print("📊 Generating: Statistici...")
    
    stats = {
        'data': datetime.now().strftime("%d.%m.%Y %H:%M"),
        'total_porturi': len(df),
        'cota_maxima': {
            'port': df.loc[df['cota_cm'].idxmax(), 'localitate'],
            'valoare': int(df['cota_cm'].max())
        },
        'cota_minima': {
            'port': df.loc[df['cota_cm'].idxmin(), 'localitate'],
            'valoare': int(df['cota_cm'].min())
        },
        'cota_medie': round(df['cota_cm'].mean(), 1)
    }
    
    output_file = Path(output_dir) / 'statistici.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Saved: {output_file}")
    
    print("\n" + "="*60)
    print("📊 STATISTICI:")
    print("="*60)
    print(f"📅 Data: {stats['data']}")
    print(f"🌊 Total porturi: {stats['total_porturi']}")
    print(f"🏆 Cotă maximă: {stats['cota_maxima']['port']} - {stats['cota_maxima']['valoare']} cm")
    print(f"📉 Cotă minimă: {stats['cota_minima']['port']} - {stats['cota_minima']['valoare']} cm")
    print(f"📊 Cotă medie: {stats['cota_medie']} cm")
    print("="*60)

def main():
    """Generează toate graficele"""
    print("🎨 Starting Chart Generation\n")
    print("="*80)
    
    # Creează folder pentru output
    output_dir = Path('reports')
    output_dir.mkdir(exist_ok=True)
    
    # Încarcă datele
    try:
        data = load_data('cote_pdf.json')
        ports = data.get('ports', [])
        
        if not ports:
            print("❌ No data found in cote_pdf.json")
            print("   Run afdj_pdf_scraper.py first!")
            return
        
        df = pd.DataFrame(ports)
        print(f"✅ Loaded {len(df)} ports\n")
        
        # Generează graficele
        generate_profil(df, output_dir)
        generate_variatii(df, output_dir)
        generate_stats(df, output_dir)
        
        print("\n" + "="*80)
        print("✅ All charts generated successfully!")
        print("="*80)
        print(f"\n📁 Check the '{output_dir}' folder for results")
        
    except FileNotFoundError:
        print("❌ File not found: cote_pdf.json")
        print("   Run afdj_pdf_scraper.py first!")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

"""
Exemple simple de utilizare a scraper-ului AFDJ
==============================================
"""

import sys
sys.path.append('..')

from afdj_final_scraper import AFDJCoteScraper


def exemplu_1_basic():
    """Exemplu 1: Utilizare de bază"""
    print("="*80)
    print("EXEMPLU 1: Utilizare de bază")
    print("="*80)
    
    scraper = AFDJCoteScraper()
    data = scraper.scrape(export_format='all')
    
    if data:
        print(f"\n✅ Scraped {len(data)} ports successfully!")


def exemplu_2_gaseste_cote_extreme():
    """Exemplu 2: Găsește cotele extreme"""
    print("\n" + "="*80)
    print("EXEMPLU 2: Găsește cotele extreme")
    print("="*80)
    
    scraper = AFDJCoteScraper()
    data = scraper.scrape(export_format='json')
    
    if data:
        # Cota maximă
        max_port = max(data, key=lambda x: x['cota_cm'] or 0)
        print(f"\n🏆 Cota maximă:")
        print(f"   Port: {max_port['localitate']}")
        print(f"   Cotă: {max_port['cota_cm']} cm")
        print(f"   Temperatură: {max_port['temperatura_celsius']}°C")
        
        # Cota minimă
        min_port = min(data, key=lambda x: x['cota_cm'] or 999999)
        print(f"\n📉 Cota minimă:")
        print(f"   Port: {min_port['localitate']}")
        print(f"   Cotă: {min_port['cota_cm']} cm")
        print(f"   Temperatură: {min_port['temperatura_celsius']}°C")


def exemplu_3_porturi_in_scadere():
    """Exemplu 3: Porturi în scădere"""
    print("\n" + "="*80)
    print("EXEMPLU 3: Porturi în scădere")
    print("="*80)
    
    scraper = AFDJCoteScraper()
    data = scraper.scrape(export_format='json')
    
    if data:
        porturi_scadere = [p for p in data if p['tendinta'] == 'scădere']
        
        print(f"\n📉 {len(porturi_scadere)} porturi în scădere:")
        for port in porturi_scadere:
            print(f"   • {port['localitate']:20s}: {port['cota_cm']:4d} cm ({port['variatia_cm']:+3d} cm)")


def exemplu_4_porturi_in_crestere():
    """Exemplu 4: Porturi în creștere"""
    print("\n" + "="*80)
    print("EXEMPLU 4: Porturi în creștere")
    print("="*80)
    
    scraper = AFDJCoteScraper()
    data = scraper.scrape(export_format='json')
    
    if data:
        porturi_crestere = [p for p in data if p['tendinta'] == 'creștere']
        
        print(f"\n📈 {len(porturi_crestere)} porturi în creștere:")
        for port in porturi_crestere:
            print(f"   • {port['localitate']:20s}: {port['cota_cm']:4d} cm ({port['variatia_cm']:+3d} cm)")


def exemplu_5_statistici():
    """Exemplu 5: Statistici generale"""
    print("\n" + "="*80)
    print("EXEMPLU 5: Statistici generale")
    print("="*80)
    
    scraper = AFDJCoteScraper()
    data = scraper.scrape(export_format='json')
    
    if data:
        cote = [p['cota_cm'] for p in data if p['cota_cm']]
        temperaturi = [p['temperatura_celsius'] for p in data if p['temperatura_celsius']]
        
        print(f"\n📊 Statistici:")
        print(f"   Total porturi: {len(data)}")
        print(f"   Cotă medie: {sum(cote)/len(cote):.1f} cm")
        print(f"   Cotă maximă: {max(cote)} cm")
        print(f"   Cotă minimă: {min(cote)} cm")
        print(f"   Temperatură medie: {sum(temperaturi)/len(temperaturi):.1f}°C")


def exemplu_6_export_specific():
    """Exemplu 6: Export în format specific"""
    print("\n" + "="*80)
    print("EXEMPLU 6: Export în format specific")
    print("="*80)
    
    scraper = AFDJCoteScraper()
    
    # Doar JSON
    print("\n📄 Export doar JSON...")
    data = scraper.scrape(export_format='json')
    
    # Sau doar CSV
    # data = scraper.scrape(export_format='csv')
    
    # Sau doar Excel
    # data = scraper.scrape(export_format='excel')


def exemplu_7_filtrare_porturi():
    """Exemplu 7: Filtrare porturi după criterii"""
    print("\n" + "="*80)
    print("EXEMPLU 7: Filtrare porturi după criterii")
    print("="*80)
    
    scraper = AFDJCoteScraper()
    data = scraper.scrape(export_format='json')
    
    if data:
        # Porturi cu apă foarte rece (< 3°C)
        porturi_reci = [p for p in data if p['temperatura_celsius'] and p['temperatura_celsius'] < 3]
        print(f"\n❄️  Porturi cu apă foarte rece (< 3°C): {len(porturi_reci)}")
        for port in porturi_reci:
            print(f"   • {port['localitate']:20s}: {port['temperatura_celsius']:.1f}°C")
        
        # Porturi cu variație mare (> 10 cm)
        porturi_variatie_mare = [p for p in data if p['variatia_cm'] and abs(p['variatia_cm']) > 10]
        print(f"\n📊 Porturi cu variație mare (> 10 cm): {len(porturi_variatie_mare)}")
        for port in porturi_variatie_mare:
            print(f"   • {port['localitate']:20s}: {port['variatia_cm']:+3d} cm")


if __name__ == "__main__":
    print("🌊 EXEMPLE DE UTILIZARE AFDJ SCRAPER 🌊\n")
    
    # Rulează toate exemplele
    exemplu_1_basic()
    exemplu_2_gaseste_cote_extreme()
    exemplu_3_porturi_in_scadere()
    exemplu_4_porturi_in_crestere()
    exemplu_5_statistici()
    exemplu_6_export_specific()
    exemplu_7_filtrare_porturi()
    
    print("\n" + "="*80)
    print("✅ TOATE EXEMPLELE AU FOST RULATE CU SUCCES!")
    print("="*80)

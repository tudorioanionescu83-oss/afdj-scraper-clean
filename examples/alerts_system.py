"""
Sistem de alertă pentru cote critice
===================================

Exemplu de sistem care monitorizează cotele și trimite alerte
când sunt depășite pragurile de atenție sau inundație.
"""

import sys
sys.path.append('..')

from afdj_final_scraper import AFDJCoteScraper
import json
from datetime import datetime


# Cote de atenție și inundație pentru principalele porturi
# Sursa: AFDJ (verifică pe site pentru valori actualizate)
COTE_ATENTIE = {
    'Sulina': {'atentie': 250, 'inundatie': 300},
    'Tulcea': {'atentie': 550, 'inundatie': 600},
    'Isaccea': {'atentie': 550, 'inundatie': 600},
    'Galați': {'atentie': 650, 'inundatie': 720},
    'Brăila': {'atentie': 650, 'inundatie': 720},
    'Hârșova': {'atentie': 650, 'inundatie': 720},
    'Cernavodă': {'atentie': 550, 'inundatie': 620},
    'Călărași': {'atentie': 700, 'inundatie': 780},
    'Oltenița': {'atentie': 600, 'inundatie': 680},
    'Giurgiu': {'atentie': 650, 'inundatie': 750},
}


class AlertSystem:
    """Sistem de alertă pentru cote"""
    
    def __init__(self):
        self.scraper = AFDJCoteScraper()
        self.alerts = []
    
    def check_alerts(self):
        """Verifică toate porturile pentru alerte"""
        print("🔍 Verificare cote pentru alerte...\n")
        
        # Obține datele
        data = self.scraper.scrape(export_format='json')
        
        if not data:
            print("❌ Nu s-au putut obține datele!")
            return
        
        # Verifică fiecare port
        for port in data:
            localitate = port['localitate']
            cota_cm = port['cota_cm']
            
            if localitate not in COTE_ATENTIE:
                continue
            
            praguri = COTE_ATENTIE[localitate]
            
            # Verifică dacă e depășită cota de inundație
            if cota_cm >= praguri['inundatie']:
                self.alerts.append({
                    'nivel': 'CRITIC',
                    'tip': 'INUNDAȚIE',
                    'localitate': localitate,
                    'cota_actuala': cota_cm,
                    'cota_prag': praguri['inundatie'],
                    'diferenta': cota_cm - praguri['inundatie'],
                    'variatia': port['variatia_cm'],
                    'tendinta': port['tendinta'],
                    'timestamp': datetime.now().isoformat()
                })
            
            # Verifică dacă e depășită cota de atenție
            elif cota_cm >= praguri['atentie']:
                self.alerts.append({
                    'nivel': 'ATENȚIE',
                    'tip': 'ATENȚIE',
                    'localitate': localitate,
                    'cota_actuala': cota_cm,
                    'cota_prag': praguri['atentie'],
                    'diferenta': cota_cm - praguri['atentie'],
                    'variatia': port['variatia_cm'],
                    'tendinta': port['tendinta'],
                    'timestamp': datetime.now().isoformat()
                })
    
    def print_alerts(self):
        """Afișează alertele în consolă"""
        if not self.alerts:
            print("✅ Nu există alerte! Toate cotele sunt în limite normale.\n")
            return
        
        print("="*80)
        print(f"🚨 ALERTE ACTIVE: {len(self.alerts)}")
        print("="*80)
        
        # Sortează alertele: CRITIC -> ATENȚIE
        sorted_alerts = sorted(self.alerts, key=lambda x: 0 if x['nivel'] == 'CRITIC' else 1)
        
        for alert in sorted_alerts:
            emoji = "🔴" if alert['nivel'] == 'CRITIC' else "🟡"
            tendinta_emoji = "📈" if alert['tendinta'] == 'creștere' else "📉" if alert['tendinta'] == 'scădere' else "➡️"
            
            print(f"\n{emoji} {alert['nivel']}: {alert['localitate']}")
            print(f"   Cotă actuală: {alert['cota_actuala']} cm")
            print(f"   Cotă {alert['tip'].lower()}: {alert['cota_prag']} cm")
            print(f"   Depășire: +{alert['diferenta']} cm")
            print(f"   Variație: {alert['variatia']:+d} cm {tendinta_emoji} ({alert['tendinta']})")
    
    def save_alerts_to_file(self, filename='alerts.json'):
        """Salvează alertele într-un fișier JSON"""
        if not self.alerts:
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'total_alerts': len(self.alerts),
                'alerts': self.alerts
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Alertele au fost salvate în: {filename}")
    
    def send_email_alert(self, email_to):
        """
        Trimite alertele prin email (exemplu - necesită configurare SMTP)
        """
        if not self.alerts:
            return
        
        # Aici ar trebui implementat codul pentru trimitere email
        # Pentru a funcționa, ai nevoie de:
        # - Server SMTP (Gmail, SendGrid, etc.)
        # - Credențiale
        
        print(f"\n📧 [SIMULARE] Alertele ar fi fost trimise la: {email_to}")
        print("   Pentru trimitere reală, configurează SMTP în cod.")
    
    def send_telegram_alert(self, bot_token, chat_id):
        """
        Trimite alertele prin Telegram (exemplu - necesită bot Telegram)
        """
        if not self.alerts:
            return
        
        # Aici ar trebui implementat codul pentru Telegram
        # Pentru a funcționa, ai nevoie de:
        # - Bot Telegram (creat prin @BotFather)
        # - Token bot
        # - Chat ID
        
        print(f"\n💬 [SIMULARE] Alertele ar fi fost trimise pe Telegram")
        print("   Pentru trimitere reală, configurează Telegram Bot în cod.")


def main():
    """Exemplu de utilizare a sistemului de alertă"""
    
    print("🌊 SISTEM DE ALERTĂ PENTRU COTE DUNĂRII 🌊\n")
    
    # Creează sistem de alertă
    alert_system = AlertSystem()
    
    # Verifică alertele
    alert_system.check_alerts()
    
    # Afișează alertele
    alert_system.print_alerts()
    
    # Salvează alertele
    alert_system.save_alerts_to_file()
    
    # Opțional: trimite prin email sau Telegram
    # alert_system.send_email_alert('your@email.com')
    # alert_system.send_telegram_alert('YOUR_BOT_TOKEN', 'YOUR_CHAT_ID')
    
    print("\n" + "="*80)
    print("✅ Verificare completă!")
    print("="*80)


if __name__ == "__main__":
    main()

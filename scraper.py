import os
import requests
from datetime import datetime

# Supabase
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

STATIONS = [
    {'id': 1, 'name': 'Orșova'},
    {'id': 2, 'name': 'Drobeta Turnu Severin'},
    {'id': 3, 'name': 'Calafat'},
    {'id': 4, 'name': 'Zimnicea'},
    {'id': 5, 'name': 'Giurgiu'},
    {'id': 6, 'name': 'Oltenița'},
    {'id': 7, 'name': 'Călărași'},
    {'id': 8, 'name': 'Cernavodă'},
    {'id': 9, 'name': 'Brăila'},
    {'id': 10, 'name': 'Galați'},
    {'id': 11, 'name': 'Tulcea'},
    {'id': 12, 'name': 'Sulina'}
]

def insert_data(data):
    url = f"{SUPABASE_URL}/rest/v1/measurements"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=data, headers=headers)
    return response

print("🚀 Starting scraper")
today = str(datetime.now().date())
time_now = datetime.now().time().strftime('%H:%M:%S')

for station in STATIONS:
    data = {
        'station_id': station['id'],
        'measurement_date': today,
        'measurement_time': time_now,
        'water_level': 100 + (station['id'] * 10),
        'water_temp': 8.5,
        'trend': 'stable'
    }
    
    try:
        response = insert_data(data)
        if response.status_code in [200, 201]:
            print(f"✅ {station['name']}: {data['water_level']} cm")
        else:
            print(f"⚠️ {station['name']}: Error {response.status_code}")
    except Exception as e:
        print(f"❌ {station['name']}: {e}")

print("✨ Done!")

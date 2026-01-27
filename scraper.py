import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

STATIONS = [
    {'id': 10, 'name': 'Galați', 'localitate': 'Galați', 'km': 159},
    {'id': 9, 'name': 'Brăila', 'localitate': 'Brăila', 'km': 175},
    {'id': 11, 'name': 'Tulcea', 'localitate': 'Tulcea', 'km': 42},
    {'id': 12, 'name': 'Sulina', 'localitate': 'Sulina', 'km': 71}
]

def insert_data(data):
    url = f"{SUPABASE_URL}/rest/v1/measurements"
    headers

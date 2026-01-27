import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def create_table():
    """Creează tabelul automat dacă nu există"""
    url = f"{SUPABASE_URL}/rest/v1/rpc/create_measurements_table"
    headers = {
        'apikey': SUPABASE

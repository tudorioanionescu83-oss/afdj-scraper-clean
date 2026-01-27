import requests
from bs4 import BeautifulSoup

print("✅ TEST AFDJ Scraper")

sites = [
    "https://afdj.ro/ro/cotele-dunarii",
    "https://www.cotele-dunarii.ro"
]

for site in sites:
    print(f"\n🌐 {site}")
    r = requests.get(site)
    soup

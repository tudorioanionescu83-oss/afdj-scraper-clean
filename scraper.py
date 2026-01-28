def download_pdf_direct():
    with sync_playwright() as p:
        print("Lansăm browserul Chromium...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        
        # Mergem pe pagina unde e tabelul, nu la PDF direct
        print("Navigăm la pagina de cote...")
        page.goto("https://www.afdj.ro/ro/cotele-dunarii", wait_until="networkidle")
        
        # Așteptăm să apară link-ul
        page.wait_for_selector('a[href*="bhcote.pdf"]')
        
        print("Simulăm click de descărcare...")
        with page.expect_download() as download_info:
            # Click real pe link
            page.click('a[href*="bhcote.pdf"]')
        
        download = download_info.value
        download.save_as(pdf_path)
        print(f"Fișier salvat: {pdf_path}")
        
        # Verificăm mărimea fișierului. Dacă e sub 10KB, e sigur un HTML de eroare
        if os.path.getsize(pdf_path) < 10000:
             with open(pdf_path, 'r', encoding='utf-8', errors='ignore') as f:
                 print("Conținut suspect detectat:")
                 print(f.read(200)) # Vedem primele 200 caractere din 'PDF'
             raise Exception("Fișierul descărcat nu este un PDF valid, ci o eroare.")
        
        browser.close()

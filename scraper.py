import requests
from bs4 import BeautifulSoup
import time
import re

urls = [
    "https://andrewreeves.co.uk/property/property-details-2_10742752/",
    "https://andrewreeves.co.uk/property/property-details-2_7307370/",
    "https://andrewreeves.co.uk/property/property-details-2_l_6328878/",
    "https://andrewreeves.co.uk/property/property-details-2_10310046/",
    "https://andrewreeves.co.uk/property/property-details-2_7309263/",
    "https://andrewreeves.co.uk/property/property-details-2_l_7309238/",
    "https://andrewreeves.co.uk/property/property-details-2_6428826/",
    "https://andrewreeves.co.uk/property/property-details-2_10751798/",
    "https://andrewreeves.co.uk/property/property-details-2_l_6329441/",
    "https://andrewreeves.co.uk/property/property-details-2_10535859/",
    "https://andrewreeves.co.uk/property/property-details-2_l_6329459/",
    "https://andrewreeves.co.uk/property/property-details-2_10602224/",
    "https://andrewreeves.co.uk/property/property-details-2_10602255/",
    "https://andrewreeves.co.uk/property/property-details-2_10602252/"
]

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

for url in urls:
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # --- 1. Basic Info ---
            title = soup.find('h1', class_='property_title').get_text(strip=True) if soup.find('h1', class_='property_title') else "N/A"
            
            raw_price = soup.find('div', class_='price').get_text(strip=True) if soup.find('div', class_='price') else ""
            price_match = re.search(r'£[\d,]+', raw_price)
            price = price_match.group(0) if price_match else "N/A"
            
            status_tag = soup.find('div', class_=lambda x: x and 'flag' in x)
            status = status_tag.get_text(strip=True) if status_tag else "Available"

            # --- 2. Features ---
            features_div = soup.find('div', class_='features')
            features = [li.get_text(strip=True) for li in features_div.find_all('li')] if features_div else []

            # --- 3. Full Details ---
            full_details = [p.get_text(strip=True) for p in soup.find_all('p', class_='room')]

            # --- 4. Images (Filtering out thumbnails to get high-res only) ---
            image_container = soup.find('div', class_='images')
            images = []
            if image_container:
                all_imgs = [img['src'] for img in image_container.find_all('img') if 'src' in img.attrs]
                # Keeps only unique links and removes the small 150x150 versions
                images = list(set([i for i in all_imgs if "150x150" not in i]))

            # --- TERMINAL DISPLAY ---
            print("\n" + "="*80)
            print(f"URL:       {url}")
            print(f"TITLE:     {title}")
            print(f"STATUS:    {status}")
            print(f"PRICE:     {price}")
            
            print("\n--- FEATURES ---")
            if features:
                for f in features: 
                    print(f" * {f}")
            else: 
                print(" No features found.")

            print("\n--- FULL DETAILS ---")
            if full_details:
                for detail in full_details: 
                    print(f" > {detail}")
            else: 
                print(" No room details found.")

            print(f"\n--- ALL IMAGES ({len(images)} total) ---")
            if images:
                for idx, img in enumerate(images, 1):
                    print(f" {idx}. {img}")
            else:
                print(" No images found.")

            print("="*80 + "\n")
            
            time.sleep(1) 
    except Exception as e:
        print(f"Error on {url}: {e}")

print("Scraping complete.")
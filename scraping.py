import requests
from bs4 import BeautifulSoup
import json
import time
import re

# 1. Your list of 14 property URLs
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

all_properties_data = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print(f"Starting scraper for {len(urls)} URLs...\n")

for url in urls:
    print(f"Scraping: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # --- 1. Title/Address ---
            title_tag = soup.find('h1', class_='property_title')
            title = title_tag.get_text(strip=True) if title_tag else "N/A"
            
            # --- 2. Price (Extracts only the £ amount) ---
            price_div = soup.find('div', class_='price')
            price = "N/A"
            if price_div:
                raw_price = price_div.get_text(strip=True)
                price_match = re.search(r'£[\d,]+', raw_price)
                price = price_match.group(0) if price_match else "N/A"
            
            # --- 3. Status (Under Offer / Let Agreed) ---
            status_tag = soup.find('div', class_=lambda x: x and 'flag' in x)
            status = status_tag.get_text(strip=True) if status_tag else "Available"
            
            # --- 4. Summary (Removes "Property Summary" prefix) ---
            summary_div = soup.find('div', class_='summary')
            summary = ""
            if summary_div:
                summary_text = summary_div.get_text(strip=True)
                summary = re.sub(r'^property summary', '', summary_text, flags=re.IGNORECASE).strip()
            
            # --- 5. Full Details (Room descriptions from <p class="room">) ---
            full_details = []
            detail_paragraphs = soup.find_all('p', class_='room')
            for p in detail_paragraphs:
                full_details.append(p.get_text(strip=True))
            
            # --- 6. Available From ---
            avail_div = soup.find('div', class_='available_date')
            available_from = "N/A"
            if avail_div:
                available_from = avail_div.get_text(strip=True).replace("Available From", "").strip()
            
            # --- 7. Features ---
            features_div = soup.find('div', class_='features')
            features = [li.get_text(strip=True) for li in features_div.find_all('li')] if features_div else []
            
            # --- 8. Images ---
            images = []
            image_container = soup.find('div', class_='images')
            if image_container:
                # Find all img tags and get unique sources
                raw_images = [img['src'] for img in image_container.find_all('img') if 'src' in img.attrs]
                images = list(set(raw_images))

            # Store the cleaned data
            property_info = {
                "url": url,
                "title": title,
                "price": price,
                "status": status,
                "available_from": available_from,
                "summary": summary,
                "full_details": full_details,
                "features": features,
                "images": images
            }
            
            all_properties_data.append(property_info)
            print(f"--- Success: {title}")
            
            # Polite delay
            time.sleep(1.5)
            
        else:
            print(f"--- FAILED: Status code {response.status_code}")
            
    except Exception as e:
        print(f"--- ERROR: {e}")

# Save the final structured data
output_filename = 'cleaned_properties.json'
with open(output_filename, 'w', encoding='utf-8') as f:
    json.dump(all_properties_data, f, indent=4, ensure_ascii=False)

# --- DEBUG SECTION: Find the missing URL ---
print("\n" + "="*30)
print(f"RESULTS SUMMARY")
print(f"Total URLs in list: {len(urls)}")
print(f"Total properties saved: {len(all_properties_data)}")

if len(urls) != len(all_properties_data):
    print("\nIDENTIFIED MISSING URLS:")
    scraped_urls = [p['url'] for p in all_properties_data]
    for original_url in urls:
        if original_url not in scraped_urls:
            print(f"-> {original_url}")
else:
    print("\nAll properties scraped successfully!")
print("="*30)
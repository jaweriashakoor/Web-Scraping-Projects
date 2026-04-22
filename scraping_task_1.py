from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# 1. Setup Browser
driver = webdriver.Chrome()
url = "https://andrewreeves.co.uk/search-results/?department=residential-lettings"
driver.get(url)
time.sleep(3)

# --- PHASE 1: Header Contacts ---
try:
    contact_spans = driver.find_elements(By.CLASS_NAME, "InfinityNumber")
    sales_no = contact_spans[0].text if len(contact_spans) > 0 else "N/A"
    lettings_no = contact_spans[1].text if len(contact_spans) > 1 else "N/A"
    
    print("=" * 60)
    print(f"SALES CONTACT:    {sales_no}")
    print(f"LETTINGS CONTACT: {lettings_no}")
    print("=" * 60)
except Exception as e:
    print(f"Contact info not found: {e}")

# This list will hold all our property data dictionaries
master_property_list = []

# --- PHASE 2: Build the List (Search Pages) ---
while True:
    listings = driver.find_elements(By.CLASS_NAME, "property")

    for house in listings:
        property_data = {}
        
        # Basic Details
        property_data['title'] = house.find_element(By.TAG_NAME, "h3").text
        property_data['price'] = house.find_element(By.CLASS_NAME, "price").text
        property_data['url'] = house.find_element(By.TAG_NAME, "a").get_attribute("href")
        
        # Status
        try:
            property_data['status'] = house.find_element(By.CLASS_NAME, "flag").text
        except:
            property_data['status'] = "Available"
        
        # Task: Get FIRST Image from DIV tag and add to list
        try:
            img_div = house.find_element(By.CLASS_NAME, "thumbnail-img")
            style_text = img_div.get_attribute("style")
            first_image = style_text.split('url(')[1].split(')')[0].replace('"', '').replace("'", "")
        except:
            first_image = "No Thumbnail"
        
        # Create the image list inside the dictionary
        property_data['all_images'] = [first_image]
        
        master_property_list.append(property_data)

    # Check for "Next" page
    try:
        next_button = driver.find_element(By.CLASS_NAME, "next")
        if "disabled" in next_button.get_attribute("class"):
            break
        next_button.click()
        time.sleep(3)
    except:
        break

# --- PHASE 3: Loop through list to append OTHER images ---
print(f"\nCollected {len(master_property_list)} properties. Fetching all gallery images...\n")

for item in master_property_list:
    driver.get(item['url'])
    time.sleep(2)
    
    # Find additional images in the property gallery
    gallery_elements = driver.find_elements(By.CLASS_NAME, "propertyhive-main-image")
    
    for element in gallery_elements:
        img_url = element.get_attribute("href")
        # Add to the list until all images for this property are completed
        if img_url and img_url not in item['all_images']:
            item['all_images'].append(img_url)

    # --- PHASE 4: Final Output in your specific order ---
    print(f"URL:    {item['url']}")
    print(f"TITLE:  {item['title']}")
    print(f"STATUS: [{item['status']}]")
    
    # Print the full list of images we appended
    print(f"IMAGES:")
    for i, img in enumerate(item['all_images'], 1):
        print(f"  {i}: {img}")
        
    print(f"PRICE:  {item['price']}")
    print("-" * 60)

# Finish
driver.quit()
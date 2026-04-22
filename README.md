# 🚀 Real Estate Data Miner: The Andrew Reeves Suite

[![Python](https://img.shields.io/badge/Python-3.14+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Scrapy-Style](https://img.shields.io/badge/Library-BeautifulSoup4-green)](https://www.crummy.com/software/BeautifulSoup/)
[![Automation](https://img.shields.io/badge/Automation-Selenium-red?logo=selenium)](https://www.selenium.dev/)
[![Data](https://img.shields.io/badge/Output-JSON-orange)](https://www.json.org/)

An advanced collection of Python scripts designed to extract, clean, and structure property data from the **Andrew Reeves** real estate portal. This repository showcases a professional progression from simple HTML parsing to complex dynamic browser automation.

---

## 🏗️ Project Architecture

This repository contains three specialized tools, each solving a different data extraction challenge:

### 1. 🎯 The Precision Scraper (`scraping_task_1.py`)
* **Tech Stack:** `Requests` + `BeautifulSoup4`
* **Focus:** High-speed extraction of specific property URLs.
* **Key Features:** * Uses **Regex** to clean currency symbols and format prices.
    * Intelligent image filtering to remove low-res thumbnails (150x150).
    * Clean terminal visualization for quick data auditing.

### 2. 🤖 The Browser Automator (`scraper.py`)
* **Tech Stack:** `Selenium WebDriver`
* **Focus:** Handling dynamic content and complex pagination.
* **Key Features:** * Automatically navigates "Next" pages until the entire catalog is indexed.
    * Extracts hidden contact numbers from the header dynamically.
    * Implements a **Master List** logic to visit sub-links and scrape full galleries.

### 3. 💾 The Data Architect (`scraping.py`)
* **Tech Stack:** `JSON` + `BeautifulSoup`
* **Focus:** Production-ready data engineering.
* **Key Features:** * Converts raw HTML into a structured `cleaned_properties.json` file.
    * Integrated **Debug Section** to identify and log failed URLs.
    * Advanced text cleaning: Removes "Property Summary" prefixes and normalizes whitespace.

---

## 📊 Data Schema Example

The scripts generate a clean JSON schema perfect for feeding into Machine Learning models or Databases:

```json
{
    "url": "[https://andrewreeves.co.uk/property/](https://andrewreeves.co.uk/property/)...",
    "title": "Stunning 2 Bed Apartment",
    "price": "£1,500",
    "status": "Available",
    "available_from": "Immediate",
    "features": ["Garden", "Parking", "Modern Kitchen"],
    "images": ["url_high_res_1.jpg", "url_high_res_2.jpg"]
}
🛠️ Installation & Usage
Clone the Repo:

Bash
git clone [https://github.com/jaweriashakoor/Web-Scraping-Projects.git](https://github.com/jaweriashakoor/Web-Scraping-Projects.git)
Activate Environment:

Bash
# Ensure you are in the project folder
.\env\Scripts\activate
Install Requirements:

Bash
pip install requests bs4 selenium
Run a Script:

Bash
python scraping.py
💡 Skills Showcased
Web Scraping: BeautifulSoup, CSS Selectors, and XPATH.

Automation: Handling dynamic page loads and pagination.

Data Cleaning: Regular Expressions (Re) for currency and text normalization.

Error Handling: Robust Try-Except blocks for unstable network conditions.

Serialization: Structured Data export via JSON.

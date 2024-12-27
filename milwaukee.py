from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import csv
import os
import pandas as pd

# Path to ChromeDriver
CHROME_DRIVER_PATH = "./drivers/chromedriver"

# Input file with ZIP codes
ZIP_CODES_FILE = os.path.join("zipcodes", "uszips.csv")

# Output CSV file
OUTPUT_FILE = "milwaukee_tool_dealers.csv"

# Milwaukee Tool URL
URL = "https://www.milwaukeetool.com/Buy-Now"

# Setup Chrome driver
def setup_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment to run headless
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Function to close pop-ups
def close_popup(driver):
    try:
        print("Checking for pop-ups...")
        popup_close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class*='close']"))
        )
        popup_close_button.click()
        print("Pop-up closed.")
        time.sleep(2)
    except TimeoutException:
        print("No pop-up detected.")
    except Exception as e:
        print(f"Error while closing pop-up: {e}")

# Function to initialize the "Find Local" search box
def initialize_search_box(driver):
    try:
        # Click "Find Local" button
        print("Clicking 'Find Local' button...")
        find_local_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Find Local"))
        )
        find_local_btn.click()
        print("'Find Local' button clicked.")
        time.sleep(2)

        # Wait for the search input box to appear
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.ps-search-input"))
        )
        print("Search input box ready.")
        return search_box
    except Exception as e:
        print(f"Error initializing search box: {e}")
        return None

# Function to fetch dealers for a ZIP code
def fetch_dealers(driver, search_box, zip_code):
    dealers_data = []

    try:
        print(f"Searching for ZIP code: {zip_code}")
        # Clear the search box and enter the new ZIP code
        search_box.clear()
        search_box.send_keys(zip_code)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)  # Wait for results to load

        # Scrape dealer results
        dealer_elements = driver.find_elements(By.CLASS_NAME, "ps-local-seller")
        for dealer in dealer_elements:
            try:
                name = dealer.find_element(By.CLASS_NAME, "ps-local-seller-name").text
                address = dealer.find_element(By.CLASS_NAME, "ps-local-seller-address").text
                phone = dealer.find_element(By.CLASS_NAME, "ps-local-seller-phone").text
                dealers_data.append([name, address, phone, zip_code])
            except Exception:
                continue  # Skip incomplete dealer entries
    except Exception as e:
        print(f"Error fetching dealers for ZIP code {zip_code}: {e}")
    
    return dealers_data

# Main function
def main():
    driver = setup_driver()

    # Initialize CSV output
    with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Address", "Phone", "ZIP Code"])

        # Load ZIP codes from the dataset
        zip_data = pd.read_csv(ZIP_CODES_FILE)
        zip_codes = zip_data['zip'].tolist()

        # Open Milwaukee Tool website
        print("Opening Milwaukee Tool website...")
        driver.get(URL)
        time.sleep(3)

        # Close pop-ups and initialize search box
        close_popup(driver)
        search_box = initialize_search_box(driver)

        if not search_box:
            print("Search box could not be initialized. Exiting...")
            driver.quit()
            return

        # Loop through ZIP codes
        for i, zip_code in enumerate(zip_codes):
            print(f"\nProcessing ZIP code: {zip_code} ({i+1}/{len(zip_codes)})")
            dealers = fetch_dealers(driver, search_box, zip_code)
            for dealer in dealers:
                writer.writerow(dealer)

    print(f"\nData saved to {OUTPUT_FILE}")
    driver.quit()

if __name__ == "__main__":
    main()

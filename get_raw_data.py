import json
import logging
import os
import time

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#selenium exception handlers
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    WebDriverException
)

#Logging Configuration to store all errors in a file called scraper.log

logging.basicConfig(
    filename="logs/scraper.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
 
#Data to Scrape 

MONTHS = [
    ("mar", "March"),
    ("apr", "April")
]

DISTRICTS = [
    ("585", "North Goa"),
    ("586", "South Goa")
]
 
#Progress saved every 10 shops and browswe restarted every 40 shops to avoid crashes 
SAVE_EVERY = 10
RESTART_EVERY = 40

BASE_URL = "https://impds.nic.in/sale/"

def create_driver():
    #Set up the chrome browser with custom settings.
    
    options = Options()

    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")

    driver = webdriver.Chrome(options=options)

    driver.set_page_load_timeout(60)

    wait = WebDriverWait(driver,20)

    return driver, wait

def wait_loader(wait):
    #Wait until the loader disappears from the page, indicating that the page has finished loading.
    wait.until(
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, "div.loader")
        )
    )
    
def safe_click(driver, wait, locator):
    #Safely click on an element, ensuring it is clickable and visible in the viewport.
    element = wait.until(
        EC.element_to_be_clickable(locator)
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        element
    )

    driver.execute_script(
        "arguments[0].click();",
        element
    )

    return element

def open_site(driver, wait):
    #Open the base URL and wait for the page to load completely.
    driver.get(BASE_URL)

    wait_loader(wait)
    
def select_month(driver, wait, month_key):
    #Select the desired month from the dropdown menu on the website.
    safe_click(
        driver,
        wait,
        (
            By.CSS_SELECTOR,
            "a[data-bs-target='#myModal10']"
        )
    )

    safe_click(
        driver,
        wait,
        (
            By.CSS_SELECTOR,
            f"a[key='{month_key}']"
        )
    )

    wait_loader(wait)
    
def select_goa(driver, wait):
    #Select the state of Goa from the list of states on the website.
    safe_click(
        driver,
        wait,
        (
            By.CSS_SELECTOR,
            "a[data-bs-target='#myModal11']"
        )
    )

    safe_click(
        driver,
        wait,
        (
            By.LINK_TEXT,
            "GOA"
        )
    )

    wait_loader(wait)
    
def select_district(driver, wait, district_id):

    safe_click(
        driver,
        wait,
        (
            By.XPATH,
            f"//a[contains(@onclick,'{district_id}')]"
        )
    )

    wait_loader(wait)
    
def open_fps_list(driver, wait):
   #Open the list of Fair Price Shops (FPS) on the website after selecting the month and district.
    safe_click(
        driver,
        wait,
        (
            By.CSS_SELECTOR,
            "a[onclick*='liveFpsdata']"
        )
    )

    wait.until(
        EC.presence_of_all_elements_located(
            (
                By.CSS_SELECTOR,
                "li.menu_list"
            )
        )
    )
    
def navigate_to_fps_list(driver, wait, month_key, district_id):
    #Perform all navigation steps to reach the list of Fair Price Shops (FPS) for a specific month and district.
    open_site(driver, wait)

    select_month(
        driver,
        wait,
        month_key
    )

    select_goa(
        driver,
        wait
    )

    select_district(
        driver,
        wait,
        district_id
    )

    open_fps_list(
        driver,
        wait
    )
    
def get_fps_count(driver):
   #To get the total numbers of FPS
    return len(

        driver.find_elements(
            By.CSS_SELECTOR,
            "li.menu_list"
        )

    )
    
def scroll_to_shop(driver, wait, index):
   #Scroll the FPS list to ensure that the shop at the specified index is visible in the viewport.
    container = wait.until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "ul.menu")
    )
)

    while True:

        shops = driver.find_elements(
            By.CSS_SELECTOR,
            "li.menu_list"
        )

        if len(shops) > index:
            return

        driver.execute_script(
            """
            arguments[0].scrollTop =
            arguments[0].scrollHeight;
            """,
            container
        )

        time.sleep(0.4)
        
def open_shop(driver, wait, index):
   #Open the shop at the specified index in the FPS list, ensuring it is visible and clickable, and return the shop's name.
    scroll_to_shop(
        driver,
        wait,
        index
    )

    shops = wait.until(
    EC.presence_of_all_elements_located(
        (
            By.CSS_SELECTOR,
            "li.menu_list"
        )
    )
)

    link = shops[index].find_element(
        By.TAG_NAME,
        "a"
    )

    shop_name = link.text.strip()

    expected_id = shop_name.split(":")[0].strip()

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        link
    )

    driver.execute_script(
        "arguments[0].click();",
        link
    )

    wait_loader(wait)

    wait.until(

        lambda d:

        get_fps_id(d) == expected_id

    )

    return shop_name

def get_fps_id(driver):
   #Get the FPS ID from the shop details page, which is displayed in a specific element on the page.
    return driver.find_element(
        By.CSS_SELECTOR,
        "span.counter1.counter_num4"
    ).text.strip()
    
def get_card_value(driver, key):
   #Get the value of a specific card (e.g., total transactions, Aadhaar authenticated) from the shop details page using its unique key.
    xpath = (
        f"//div[@key='{key}']"
        "/following-sibling::div[contains(@class,'infi_count')]//span"
    )

    return driver.find_element(
        By.XPATH,
        xpath
    ).text.strip()
    
def scrape_table(driver, label):
   #Scrape a table from the shop details page based on its label (e.g., "Number of Transaction", "Distributed Quantity(In Kg)"), and return the data as a dictionary.
    table = driver.find_element(

        By.XPATH,

        f"//table[@aria-label='{label}']"

    )

    rows = table.find_elements(

        By.XPATH,

        ".//tbody/tr"

    )

    data = {}

    for row in rows:

        cols = row.find_elements(
            By.TAG_NAME,
            "td"
        )

        if len(cols) < 5:
            continue

        data[cols[0].text.strip()] = {

            "regular": cols[1].text.strip(),
            "intra_state": cols[2].text.strip(),
            "inter_state": cols[3].text.strip(),
            "total": cols[4].text.strip()

        }

    return data

def scrape_quantity_table(driver):

    return scrape_table(
        driver,
        "Distributed Quantity(In Kg)"
    )
    
def scrape_single_shop(driver, wait):

    # Wait until summary section appears
    wait.until(

        EC.visibility_of_element_located(

            (
                By.XPATH,
                "//div[contains(text(),'Total e-Transaction')]"
            )

        )

    )

    summary = {

        "total_e_transaction":
            get_card_value(driver, "trs"),

        "aadhaar_authenticated":
            get_card_value(driver, "aafioc"),

        "other_mode_authenticated":
            get_card_value(driver, "aom1"),

        "non_authenticated":
            get_card_value(driver, "nat1")

    }

    transaction_table = scrape_table(

        driver,

        "Number of Transaction"

    )

    ration_card_table = scrape_table(

        driver,

        "Number of Transacted Ration Card"

    )

    # Open Coarse Grains section
    coarse_button = wait.until(

        EC.element_to_be_clickable(

            (
                By.XPATH,
                "//button[contains(.,'Coarse Grains')]"
            )

        )

    )
   #scrolling the coarse grain button into visible area of page and clicking it to reveal the coarse grain data.
    driver.execute_script(

        "arguments[0].scrollIntoView({block:'center'});",

        coarse_button

    )
    #Click the button using JavaScript to avoid issues with overlapping 
    driver.execute_script(

        "arguments[0].click();",

        coarse_button

    )

    # Wait until quantity rows actually load
    wait.until(

        lambda d:

        len(

            d.find_elements(

                By.XPATH,

                "//table[@aria-label='Distributed Quantity(In Kg)']//tbody/tr"

            )

        ) > 0

    )

    quantity_table = scrape_quantity_table(driver)

    return {

        "summary": summary,

        "transaction_table": transaction_table,

        "ration_card_table": ration_card_table,

        "quantity_table": quantity_table

    }
    
def save_json(data, month_name, district_name):
    #create the output json filename
    filename = (

        f"data/raw/"

        f"{month_name.lower()}_"

        f"{district_name.lower().replace(' ','_')}.json"

    )
   #save the scraped data as json file
    with open(

        filename,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            data,

            f,

            indent=4,

            ensure_ascii=False

        )

    print(f"Saved {len(data)} shops")
    
def main():

    for month_key, month_name in MONTHS:

        for district_id, district_name in DISTRICTS:

            print(f"\n========== {month_name} | {district_name} ==========")

            scraped_data = []

            driver, wait = create_driver()

            navigate_to_fps_list(
                driver,
                wait,
                month_key,
                district_id
            )

            fps_count = get_fps_count(driver)

            print(f"Total Shops : {fps_count}")
            # start scraping from first shop until all are processed.
            shop_index = 0

            while shop_index < fps_count:

                # Restart Chrome every 40 shops
                if shop_index != 0 and shop_index % RESTART_EVERY == 0:

                    print(
                        f"\nRestarting Chrome after {shop_index} shops..."
                    )

                    driver.quit()

                    driver, wait = create_driver()

                    navigate_to_fps_list(
                        driver,
                        wait,
                        month_key,
                        district_id
                    )

                try:

                    shop_name = open_shop(
                        driver,
                        wait,
                        shop_index
                    )

                    print(
                        f"Processing {shop_index+1}/{fps_count}"
                    )

                    print(shop_name)

                    shop_data = scrape_single_shop(
                        driver,
                        wait
                    )

                    shop_data["shop_name"] = shop_name

                    scraped_data.append(shop_data)

                    shop_index += 1

                    # Save every 10 shops
                    if shop_index % SAVE_EVERY == 0:

                        save_json(
                            scraped_data,
                            month_name,
                            district_name
                        )

                except Exception as e:
                  #display which shop could not be scraped
                    print(
                        f"Shop {shop_index+1} Failed"
                    )

                    print(e)

                    logging.exception(e)

                    # Restart browser

                    driver.quit()
                   #launching a new browser session 
                    driver, wait = create_driver()
                  #navigate back to the month and district
                    navigate_to_fps_list(
                        driver,
                        wait,
                        month_key,
                        district_id
                    )

                    # Continue from same shop
                    continue

            save_json(
                scraped_data,
                month_name,
                district_name
            )

            driver.quit()

    print("\nFinished Everything")
    
if __name__ == "__main__":
    main()
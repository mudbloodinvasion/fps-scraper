import logging

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Setting up logging
logging.basicConfig(
    filename="logs/scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Browser Started")


# Reusable function to get summary card values
def get_card_value(driver, key):
    xpath = f"//div[@key='{key}']/following-sibling::div[contains(@class,'infi_count')]//span"
    value = driver.find_element(By.XPATH, xpath).text
    return value.strip()

#function to scrape transaction table
def scrape_transaction_table(driver):

    transaction_data = {}

    table = driver.find_element(
        By.XPATH,
        "//table[@aria-label='Number of Transaction']"
    )

    rows = table.find_elements(By.XPATH, ".//tbody/tr")

    for row in rows:

        cells = row.find_elements(By.TAG_NAME, "td")

        card_type = cells[0].text.strip()

        transaction_data[card_type] = {
            "regular": cells[1].text.strip(),
            "intra_state": cells[2].text.strip(),
            "inter_state": cells[3].text.strip(),
            "total": cells[4].text.strip()
        }

    return transaction_data




def main():

   
    # Launch Browser
    
    options = webdriver.ChromeOptions()

    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    driver.get("https://impds.nic.in/sale/")

    logging.info("Website opened successfully")

    
    # Select Month (March 2026)
   
    month_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "a[data-bs-target='#myModal10']")
        )
    )
    month_button.click()

    logging.info("Month popup opened")

    march_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "a[key='mar']")
        )
    )
    march_button.click()

    logging.info("March selected")

  
    # Open States Popup
    
    states_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "a[data-bs-target='#myModal11']")
        )
    )

    states_button.click()

    logging.info("States popup opened")

    # Select Goa
  
    goa_button = wait.until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, "GOA")
        )
    )

    goa_button.click()

    logging.info("GOA selected")

    
    # Select North Goa
    
    try:
        north_goa = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@onclick,'585')]")
            )
        )

        north_goa.click()

        logging.info("North Goa selected")

    except Exception as e:
        logging.error(f"Failed to open North Goa: {e}")
        driver.save_screenshot("north_goa_error.png")
        raise

    
    # Open FPS List
   
    fps_card = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "a[onclick*='liveFpsdata']")
        )
    )

    fps_card.click()

    logging.info("FPS list opened")

    
    # Get FPS List
   
    fps_list = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "li.menu_list")
        )
    )

    print(f"Found {len(fps_list)} FPS shops")

    logging.info(f"Found {len(fps_list)} FPS shops")

    
    # Click First FPS
    
    first_fps = fps_list[0]

    print(first_fps.text)

    first_fps.click()

    logging.info("First FPS clicked")

    
    # Wait for panel to refresh
    
    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(text(),'Total e-Transaction')]")
        )
    )

   
    # Scrape Summary Cards
    
    total_transactions = get_card_value(driver, "trs")
    aadhaar = get_card_value(driver, "aafioc")
    other_mode = get_card_value(driver, "aom1")
    non_authenticated = get_card_value(driver, "nat1")

    print("Total Transactions :", total_transactions)
    print("Aadhaar            :", aadhaar)
    print("Other Mode         :", other_mode)
    print("Non Authenticated  :", non_authenticated)

    summary_data = {
        "total_e_transaction": total_transactions,
        "aadhaar_authenticated": aadhaar,
        "other_mode_authenticated": other_mode,
        "non_authenticated": non_authenticated
    }

    print(summary_data)

    transaction_table = scrape_transaction_table(driver)

    print(transaction_table)


    input("Press Enter to close the browser...")

    driver.quit()


if __name__ == "__main__":
    main()
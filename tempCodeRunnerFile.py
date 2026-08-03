    total_transaction = driver.find_element(
    By.XPATH,
    "//div[contains(text(),'Total e-Transaction')]/following-sibling::div[contains(@class,'infi_count')]//span"
 ).text
 
 print(total_transaction)
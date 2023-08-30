# import time
# import csv
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
# from selenium.webdriver.common.action_chains import ActionChains
# from webdriver_manager.chrome import ChromeDriverManager
#
# # Create a Chrome WebDriver instance using webdriver_manager
# driver = webdriver.Chrome(ChromeDriverManager().install())
#
# # Open the main URL
# driver.get('https://dufferinmall.ca/stores/')
# driver.maximize_window()
# # Wait for store elements to load
# wait = WebDriverWait(driver, 10)
#
# # Create a CSV file to write the data
# csv_file_path = 'store_details.csv'
# csv_file = open(csv_file_path, 'w', newline='', encoding='utf-8')
# csv_writer = csv.writer(csv_file)
# csv_writer.writerow(['Store Details'])  # Header
#
#
# # Function to scroll by a certain amount
# def scroll_page():
#     driver.execute_script("window.scrollBy(0, 500);")
#     time.sleep(2)  # Add a short delay to allow content to load
#
#
# # Process store elements
# def process_store_elements(store_elements, index=0):
#     if index >= len(store_elements):
#         return
#
#     store_element = store_elements[index]
#     try:
#         # Extract the store name
#         store_name = store_element.text
#
#         # Click on the store element using ActionChains
#         action = ActionChains(driver)
#         action.move_to_element(store_element).click().perform()
#         time.sleep(3)
#         # Wait for the "store-deets-container" to load
#         wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'store-deets-container')))
#
#         # Extract the phone number from the .info class on the main page
#         try:
#             phone_number_element = driver.find_element(By.CSS_SELECTOR, '.store-detail')
#             phone_number = phone_number_element.text
#         except NoSuchElementException:
#             phone_number = ' '
#
#         # Extract the store details
#         store_details_element = driver.find_element(By.CLASS_NAME, 'store-deets-container')
#         store_details = store_details_element.text
#
#         # Write the combined data to the CSV file (single column)
#         combined_data = f'{store_name}\n{phone_number}\n{store_details}'
#         csv_writer.writerow([combined_data])
#         time.sleep(2)
#         # Go back to the main page
#         driver.back()
#         time.sleep(10)
#
#         # Scroll the page
#         scroll_page()
#
#         # Refresh the store elements to load them again
#         store_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'store-name')))
#
#         # Process the next store element
#         process_store_elements(store_elements, index + 1)
#     except StaleElementReferenceException:
#         # Handle StaleElementReferenceException by re-locating the elements
#         store_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'store-name')))
#         process_store_elements(store_elements, index)
#
#
# # Find all store elements with the class "store-name"
# store_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'store-name')))
#
# # Process each store element
# process_store_elements(store_elements, 0)
#
# # Scroll back to the top after processing all stores
# driver.execute_script("window.scrollTo(0, 0);")
#
# # Close the CSV file
# csv_file.close()
#
# # Close the browser
# driver.quit()
#
# print("Data extraction completed.")




import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# Create a Chrome WebDriver instance using webdriver_manager
driver = webdriver.Chrome(ChromeDriverManager().install())

# Open the main URL
driver.get('https://dufferinmall.ca/stores/')
driver.maximize_window()
# Wait for store elements to load
wait = WebDriverWait(driver, 10)

# Create a CSV file to write the data
csv_file_path = 'store_details.csv'
csv_file = open(csv_file_path, 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Store Details'])  # Header

# Function to scroll by a certain amount
def scroll_page():
    driver.execute_script("window.scrollBy(0, 300);")
    time.sleep(2)  # Add a short delay to allow content to load

# Process store elements
def process_store_elements(store_elements, index=0):
    while index < len(store_elements):
        try:
            store_element = store_elements[index]

            # Extract the store name
            store_name = store_element.text

            # Scroll the element into view using JavaScript
            driver.execute_script("arguments[0].scrollIntoView();", store_element)

            # Click on the store element using JavaScript
            driver.execute_script("arguments[0].click();", store_element)
            time.sleep(1)

            # Wait for the "store-deets-container" to load
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'store-deets-container')))

            # Extract the phone number from the .info class on the main page
            try:
                phone_number_element = driver.find_element(By.CSS_SELECTOR, '.store-detail')
                phone_number = phone_number_element.text
            except NoSuchElementException:
                phone_number = ' '

            # Extract the store details
            store_details_element = driver.find_element(By.CLASS_NAME, 'store-deets-container')
            store_details = store_details_element.text

            # Write the combined data to the CSV file (single column)
            combined_data = f'{store_name}\n{phone_number}\n{store_details}'
            csv_writer.writerow([combined_data])
            time.sleep(1)

            # Go back to the main page
            driver.execute_script("window.history.go(-1);")
            time.sleep(10)

            # Increment the index
            index += 1

            # Scroll the page if necessary
            if index % 10 == 0:
                scroll_page()

            # Refresh the store elements to load them again
            store_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'store-name')))
        except StaleElementReferenceException:
            # Handle StaleElementReferenceException by re-locating the elements
            store_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'store-name')))

# Find all store elements with the class "store-name"
store_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'store-name')))

# Process each store element
process_store_elements(store_elements, 0)

# Close the CSV file
csv_file.close()

# Close the browser


print("Data extraction completed.")

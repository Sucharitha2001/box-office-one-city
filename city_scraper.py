from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def get_all_cities():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get("https://in.bookmyshow.com/")
    time.sleep(5)

    # Click city selector
    selector = driver.find_element(By.CLASS_NAME, "sc-jlZhew")
    selector.click()
    time.sleep(3)

    cities = driver.find_elements(By.CLASS_NAME, "sc-bZQynM")
    city_list = [city.text.lower().replace(" ", "-") for city in cities if city.text]

    driver.quit()
    return city_list

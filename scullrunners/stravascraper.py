from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Browser settings
chrome_options = Options()
chrome_options.add_argument("--headless")

def create_new_driver(url):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(2)
    driver.find_element(By.CLASS_NAME,"btn-deny-cookie-banner").click()
    return driver

def get_this_weeks_total(driver):
    driver.find_element(By.CSS_SELECTOR,"span[class='button this-week selected']").click()
    driver.implicitly_wait(2)
    WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.CSS_SELECTOR, "td[class='distance highlighted-column']").text.strip() != '')
    elements = driver.find_elements(By.CSS_SELECTOR, "td[class='distance highlighted-column']")
    distances = [element.text.split()[0] for element in elements]
    total = sum(map(float,distances))
    return total

def get_last_weeks_total(driver):
    driver.find_element(By.CSS_SELECTOR,"span[class='button last-week']").click()
    driver.implicitly_wait(2)
    WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.CSS_SELECTOR, "td[class='distance highlighted-column']").text.strip() != '')
    elements = driver.find_elements(By.CSS_SELECTOR, "td[class='distance highlighted-column']")
    distances = [element.text.split()[0] for element in elements]
    total = sum(map(float,distances))
    return total
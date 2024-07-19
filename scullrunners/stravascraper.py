from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv

load_dotenv()

# Browser settings
chrome_options = Options()
#chrome_options.add_argument("--headless")

def create_new_driver(url):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(20)
    driver.find_element(By.CSS_SELECTOR,"button[data-cy='deny-cookies']").click()
    return driver

def log_in(driver, url):
    driver.find_element(By.CSS_SELECTOR,"button[data-cy='login_btn']").click()
    username = driver.find_element(By.CSS_SELECTOR,"input[name='email']")
    username.send_keys(os.getenv('EMAIL'))
    password = driver.find_element(By.CSS_SELECTOR,"input[name='password']")
    password.send_keys(os.getenv('PASSWORD'))
    driver.find_element(By.CSS_SELECTOR,"button[id='login-button']").click()
    driver.get(url)

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
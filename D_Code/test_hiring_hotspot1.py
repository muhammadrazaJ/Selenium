#test_hiring_hotspot.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configs
CHROMEDRIVER_PATH = 'C:/Drivers/chromedriver-win64/chromedriver.exe'
BASE_URL = "https://hiring-hotspot.vercel.app"
EMAIL = "k213916@nu.edu.pk"
PASSWORD = "Password123"

@pytest.fixture
def driver():
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()

def login(driver):
    driver.get(f"{BASE_URL}/login")
    time.sleep(3)
    wait = WebDriverWait(driver, 10)

    email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Sign In']]")))

    email_input.send_keys(EMAIL)
    password_input.send_keys(PASSWORD)
    login_button.click()

    # Wait for navbar to confirm login
    wait.until(EC.presence_of_element_located((By.XPATH, "//nav")))
    print("✅ Login successful")

def test_login(driver):
    login(driver)
    # Assert user is redirected to dashboard or nav exists
    assert "login" not in driver.current_url
    print("✅ test_login passed")

def test_send_message(driver):
    login(driver)
    driver.get(f"{BASE_URL}/chat")
    wait = WebDriverWait(driver, 20)

    search_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@placeholder='Search conversations...']")
    ))
    print("✅ Search input found")

    search_input.clear()
    search_input.send_keys("hassan")
    time.sleep(2)

    hassan_user = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//h3[text()='Hassan Haneef']")
    ))
    hassan_user.click()
    print("✅ Clicked on 'Hassan Haneef'")

    message_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@placeholder='Type your message...']")
    ))
    print("✅ Message input found")

    message_input.send_keys("Hello from Selenium!")
    message_input.send_keys(Keys.ENTER)
    print("✅ Message sent")

    time.sleep(3)
    assert "Hello from Selenium!" in driver.page_source
    print("✅ Message verified on screen")

def test_view_contract(driver):
    login(driver)
    driver.get(f"{BASE_URL}/contracts/14")
    wait = WebDriverWait(driver, 10)

    contract_title = wait.until(EC.presence_of_element_located((By.XPATH, "//h2")))
    print("🔍 Found heading text:", contract_title.text)

    # Simply assert the heading is non-empty
    assert contract_title.text.strip() != ""
    print("✅ View contract test passed!")
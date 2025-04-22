# test_hiring_hotspot_pom.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Configs
CHROMEDRIVER_PATH = 'C:/Drivers/chromedriver-win64/chromedriver.exe'
BASE_URL = "https://hiring-hotspot.vercel.app"
EMAIL = "k213916@nu.edu.pk"
PASSWORD = "Password123"
SCREENSHOT_DIR = "screenshots"
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)

# Page Objects
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.email_field = (By.NAME, "email")
        self.password_field = (By.NAME, "password")
        self.login_button = (By.XPATH, "//button[span[text()='Sign In']]")
        self.navbar = (By.XPATH, "//nav")

    def login(self, email, password):
        wait = WebDriverWait(self.driver, 10)
        email_input = wait.until(EC.presence_of_element_located(self.email_field))
        password_input = wait.until(EC.presence_of_element_located(self.password_field))
        login_button = wait.until(EC.element_to_be_clickable(self.login_button))
        
        email_input.send_keys(email)
        password_input.send_keys(password)
        login_button.click()
        
        wait.until(EC.presence_of_element_located(self.navbar))
        print("✅ Login successful")

class ChatPage:
    def __init__(self, driver):
        self.driver = driver
        self.search_input = (By.XPATH, "//input[@placeholder='Search conversations...']")
        self.user_result = (By.XPATH, "//h3[text()='Hassan Haneef']")
        self.message_input = (By.XPATH, "//input[@placeholder='Type your message...']")

    def search_and_select_user(self, search_term):
        wait = WebDriverWait(self.driver, 20)
        search_input = wait.until(EC.presence_of_element_located(self.search_input))
        print("✅ Search input found")
        search_input.clear()
        search_input.send_keys(search_term)
        time.sleep(2)  # Allow search results to load
        user = wait.until(EC.element_to_be_clickable(self.user_result))
        user.click()
        print("✅ Clicked on 'Hassan Haneef'")

    def send_message(self, message):
        wait = WebDriverWait(self.driver, 10)
        message_input = wait.until(EC.presence_of_element_located(self.message_input))
        print("✅ Message input found")
        message_input.send_keys(message)
        message_input.send_keys(Keys.ENTER)
        print("✅ Message sent")
        time.sleep(3)  # Allow message to appear
        assert message in self.driver.page_source
        print("✅ Message verified on screen")

class ContractPage:
    def __init__(self, driver):
        self.driver = driver
        self.contract_title = (By.XPATH, "//h2")

    def view_contract(self):
        wait = WebDriverWait(self.driver, 10)
        contract_title = wait.until(EC.presence_of_element_located(self.contract_title))
        print("🔍 Found heading text:", contract_title.text)
        assert contract_title.text.strip() != ""
        print("✅ View contract test passed!")

# Fixture for driver
@pytest.fixture
def driver():
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()

# Tests
def test_login(driver):
    login_page = LoginPage(driver)
    driver.get(f"{BASE_URL}/login")
    login_page.login(EMAIL, PASSWORD)
    assert "login" not in driver.current_url
    driver.save_screenshot(f"{SCREENSHOT_DIR}/login_success.png")
    print("✅ test_login passed")

def test_send_message(driver):
    login_page = LoginPage(driver)
    chat_page = ChatPage(driver)
    driver.get(f"{BASE_URL}/login")
    login_page.login(EMAIL, PASSWORD)
    driver.get(f"{BASE_URL}/chat")
    chat_page.search_and_select_user("hassan")
    driver.save_screenshot(f"{SCREENSHOT_DIR}/chat_search.png")
    chat_page.send_message("Hello from Selenium!")
    driver.save_screenshot(f"{SCREENSHOT_DIR}/message_sent.png")

def test_view_contract(driver):
    login_page = LoginPage(driver)
    contract_page = ContractPage(driver)
    driver.get(f"{BASE_URL}/login")
    login_page.login(EMAIL, PASSWORD)
    driver.get(f"{BASE_URL}/contracts/14")
    contract_page.view_contract()
    driver.save_screenshot(f"{SCREENSHOT_DIR}/contract_viewed.png")
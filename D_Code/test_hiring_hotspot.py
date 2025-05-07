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
        self.error_message = (By.XPATH, "//div[contains(@class, 'error-message')]")  # Update locator

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

    def login_with_invalid_credentials(self, email, password):
        wait = WebDriverWait(self.driver, 10)
        email_input = wait.until(EC.presence_of_element_located(self.email_field))
        password_input = wait.until(EC.presence_of_element_located(self.password_field))
        login_button = wait.until(EC.element_to_be_clickable(self.login_button))
        
        email_input.send_keys(email)
        password_input.send_keys(password)
        login_button.click()
        
        error = wait.until(EC.presence_of_element_located(self.error_message))
        return error.text

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

class RegisterPage:
    def __init__(self, driver):
        self.driver = driver
        self.first_name_field = (By.ID, "first_name")  # Update locator
        self.last_name_field = (By.ID, "last_name")  # Update locator
        self.email_field = (By.ID, "email")  # Update locator
        self.password_field = (By.ID, "password")  # Update locator
        self.phone_field = (By.ID, "phone_number")  # Update locator
        self.country_field = (By.ID, "country")  # Update locator
        self.role_field = (By.ID, "role")  # Update locator
        self.terms_checkbox = (By.ID, "terms_accepted")  # Update locator
        self.register_button = (By.XPATH, "//button[contains(text(), 'Register')]")  # Update locator
        self.success_message = (By.XPATH, "//div[contains(text(), 'Registration successful')]")  # Update locator

    def register(self, first_name, last_name, email, password, phone, country, role, terms_accepted):
        wait = WebDriverWait(self.driver, 10)
        first_name_input = wait.until(EC.presence_of_element_located(self.first_name_field))
        last_name_input = wait.until(EC.presence_of_element_located(self.last_name_field))
        email_input = wait.until(EC.presence_of_element_located(self.email_field))
        password_input = wait.until(EC.presence_of_element_located(self.password_field))
        phone_input = wait.until(EC.presence_of_element_located(self.phone_field))
        country_input = wait.until(EC.presence_of_element_located(self.country_field))
        role_input = wait.until(EC.presence_of_element_located(self.role_field))
        terms_input = wait.until(EC.presence_of_element_located(self.terms_checkbox))
        register_button = wait.until(EC.element_to_be_clickable(self.register_button))
        
        first_name_input.send_keys(first_name)
        last_name_input.send_keys(last_name)
        email_input.send_keys(email)
        password_input.send_keys(password)
        phone_input.send_keys(phone)
        country_input.send_keys(country)
        role_input.send_keys(role)
        if terms_accepted:
            terms_input.click()
        register_button.click()
        
        success = wait.until(EC.presence_of_element_located(self.success_message))
        assert "Registration successful" in success.text
        print("✅ Registration successful")

class ProposalPage:
    def __init__(self, driver):
        self.driver = driver
        self.bid_field = (By.ID, "bid_amount")  # Update locator
        self.cover_letter_field = (By.ID, "cover_letter")  # Update locator
        self.estimated_days_field = (By.ID, "estimated_days")  # Update locator
        self.submit_button = (By.XPATH, "//button[contains(text(), 'Submit Proposal')]")  # Update locator
        self.success_message = (By.XPATH, "//div[contains(text(), 'Proposal submitted')]")  # Update locator
        self.proposal_list = (By.CLASS_NAME, "proposal-item")  # Update locator

    def submit_proposal(self, bid_amount, cover_letter, estimated_days):
        wait = WebDriverWait(self.driver, 10)
        bid_input = wait.until(EC.presence_of_element_located(self.bid_field))
        cover_letter_input = wait.until(EC.presence_of_element_located(self.cover_letter_field))
        days_input = wait.until(EC.presence_of_element_located(self.estimated_days_field))
        submit_button = wait.until(EC.element_to_be_clickable(self.submit_button))
        
        bid_input.send_keys(bid_amount)
        cover_letter_input.send_keys(cover_letter)
        days_input.send_keys(estimated_days)
        submit_button.click()
        
        success = wait.until(EC.presence_of_element_located(self.success_message))
        assert "Proposal submitted" in success.text
        print("✅ Proposal submitted")

    def view_proposals(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located(self.proposal_list))
        proposals = self.driver.find_elements(*self.proposal_list)
        assert len(proposals) > 0
        print("✅ Proposals displayed")

class JobPostPage:
    def __init__(self, driver):
        self.driver = driver
        self.job_list = (By.CLASS_NAME, "job-post")  # Update locator
        self.title_field = (By.ID, "title")  # Update locator
        self.description_field = (By.ID, "description")  # Update locator
        self.project_type_field = (By.ID, "project_type")  # Update locator
        self.job_type_field = (By.ID, "job_type")  # Update locator
        self.skill_level_field = (By.ID, "skill_level")  # Update locator
        self.duration_field = (By.ID, "estimated_duration")  # Update locator
        self.sub_skills_field = (By.ID, "sub_skills")  # Update locator
        self.create_button = (By.XPATH, "//button[contains(text(), 'Create Job')]")  # Update locator
        self.success_message = (By.XPATH, "//div[contains(text(), 'Job post created')]")  # Update locator

    def view_job_posts(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located(self.job_list))
        jobs = self.driver.find_elements(*self.job_list)
        assert len(jobs) > 0
        print("✅ Job posts displayed")

    def create_job_post(self, title, description, project_type, job_type, skill_level, duration, sub_skills):
        wait = WebDriverWait(self.driver, 10)
        title_input = wait.until(EC.presence_of_element_located(self.title_field))
        description_input = wait.until(EC.presence_of_element_located(self.description_field))
        project_type_input = wait.until(EC.presence_of_element_located(self.project_type_field))
        job_type_input = wait.until(EC.presence_of_element_located(self.job_type_field))
        skill_level_input = wait.until(EC.presence_of_element_located(self.skill_level_field))
        duration_input = wait.until(EC.presence_of_element_located(self.duration_field))
        sub_skills_input = wait.until(EC.presence_of_element_located(self.sub_skills_field))
        create_button = wait.until(EC.element_to_be_clickable(self.create_button))
        
        title_input.send_keys(title)
        description_input.send_keys(description)
        project_type_input.send_keys(project_type)
        job_type_input.send_keys(job_type)
        skill_level_input.send_keys(skill_level)
        duration_input.send_keys(duration)
        sub_skills_input.send_keys(sub_skills)
        create_button.click()
        
        success = wait.until(EC.presence_of_element_located(self.success_message))
        assert "Job post created" in success.text
        print("✅ Job post created")

class PasswordResetPage:
    def __init__(self, driver):
        self.driver = driver
        self.email_field = (By.ID, "email")  # Update locator
        self.reset_button = (By.XPATH, "//button[contains(text(), 'Send Reset Link')]")  # Update locator
        self.success_message = (By.XPATH, "//div[contains(text(), 'Password reset link sent')]")  # Update locator

    def request_password_reset(self, email):
        wait = WebDriverWait(self.driver, 10)
        email_input = wait.until(EC.presence_of_element_located(self.email_field))
        reset_button = wait.until(EC.element_to_be_clickable(self.reset_button))
        
        email_input.send_keys(email)
        reset_button.click()
        
        success = wait.until(EC.presence_of_element_located(self.success_message))
        assert "Password reset link sent" in success.text
        print("✅ Password reset link sent")

# Fixture for driver
@pytest.fixture
def driver():
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()

# Tests (TC341–TC343: Original Tests)
def test_login(driver):  # TC341
    login_page = LoginPage(driver)
    driver.get(f"{BASE_URL}/login")
    login_page.login(EMAIL, PASSWORD)
    assert "login" not in driver.current_url
    driver.save_screenshot(f"{SCREENSHOT_DIR}/tc341_login_success.png")
    print("✅ TC341 passed")

def test_send_message(driver):  # TC342
    login_page = LoginPage(driver)
    chat_page = ChatPage(driver)
    driver.get(f"{BASE_URL}/login")
    login_page.login(EMAIL, PASSWORD)
    driver.get(f"{BASE_URL}/chat")
    chat_page.search_and_select_user("hassan")
    driver.save_screenshot(f"{SCREENSHOT_DIR}/tc342_chat_search.png")
    chat_page.send_message("Hello from Selenium!")
    driver.save_screenshot(f"{SCREENSHOT_DIR}/tc342_message_sent.png")
    print("✅ TC342 passed")

def test_view_contract(driver):  # TC343
    login_page = LoginPage(driver)
    contract_page = ContractPage(driver)
    driver.get(f"{BASE_URL}/login")
    login_page.login(EMAIL, PASSWORD)
    driver.get(f"{BASE_URL}/contracts/14")
    contract_page.view_contract()
    driver.save_screenshot(f"{SCREENSHOT_DIR}/tc343_contract_viewed.png")
    print("✅ TC343 passed")

# Additional Tests (TC344–TC353)
def test_register(driver):  # TC344
    register_page = RegisterPage(driver)
    driver.get(f"{BASE_URL}/register")
    register_page.register(
        first_name="Test",
        last_name="User",
        email="test2@example.com",
        password="Password123",
        phone="+1234567890",
        country="US",
        role="freelancer",
        terms_accepted=True
    )
    driver.save_screenshot(f"{SCREENSHOT_DIR}/tc344_register_success.png")
    print("✅ TC344 passed")

def test_submit_proposal(driver):  # TC345
    login_page = LoginPage(driver)
    proposal_page = ProposalPage(driver)
    driver.get(f"{BASE_URL}/login")
    login_page.login(EMAIL, PASSWORD)
    driver.get(f"{BASE_URL}/jobs/1")
    proposal_page.submit_proposal("1000", "Interested in this job", "30")
    driver.save_screenshot(f"{SCREENSHOT_DIR}/tc345_proposal_submitted.png")
    print("✅ TC345 passed")

def test_view_job_posts(driver):  # TC346
    login_page = LoginPage(driver)
    job_post_page = JobPostPage(driver)
    driver.get(f"{BASE_URL}/login")
    login_page.login(EMAIL, PASSWORD)
    driver.get(f"{BASE_URL}/jobs")
    job_post_page.view_job_posts()
    driver.save_screenshot(f"{SCREENSHOT_DIR}/tc346_job_posts_viewed.png")
    print("✅ TC346 passed")

def test_password_reset(driver):  # TC347
    password_reset_page = PasswordResetPage(driver)
    driver.get(f"{BASE_URL}/forgot-password")
    password_reset_page.request_password_reset(EMAIL)
    driver.save_screenshot(f"{SCREENSHOT_DIR}/tc347_reset_link_sent.png")
    print("✅ TC347 passed")

def test_create_job_post(driver):  # TC348
    login_page = LoginPage(driver)
    job_post_page = JobPostPage(driver)
    driver.get(f"{BASE_URL}/login")
    login_page.login(EMAIL, PASSWORD)
    driver.get(f"{BASE_URL}/jobs/create")
    job_post_page.create_job_post(
        title="New Project",
        description="Test project",
        project_type="small",
        job_type="full-time",
        skill_level="intermediate",
        duration="1_to_3_months",
        sub_skills="1,2"
    )
    driver.save_screenshot(f"{SCREENSHOT_DIR}/tc348_job_post_created.png")
    print("✅ TC348 passed")

def test_logout(driver):  # TC349
    login_page = LoginPage(driver)
    driver.get(f"{BASE_URL}/login")
    login_page.login(EMAIL, PASSWORD)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Logout')]").click()  # Update locator
    wait = WebDriverWait(driver, 10)
    success = wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Successfully logged out"))
    assert success
    driver.save_screenshot(f"{SCREENSHOT_DIR}/tc349_logout_success.png")
    print("✅ TC349 passed")

def test_view_freelancer_proposals(driver):  # TC350
    login_page = LoginPage(driver)
    proposal_page = ProposalPage(driver)
    driver.get(f"{BASE_URL}/login")
    login_page.login(EMAIL, PASSWORD)
    driver.get(f"{BASE_URL}/proposals")
    proposal_page.view_proposals()
    driver.save_screenshot(f"{SCREENSHOT_DIR}/tc350_proposals_viewed.png")
    print("✅ TC350 passed")

def test_view_job_proposals(driver):  # TC351
    login_page = LoginPage(driver)
    proposal_page = ProposalPage(driver)
    driver.get(f"{BASE_URL}/login")
    login_page.login(EMAIL, PASSWORD)  # Assumes client role
    driver.get(f"{BASE_URL}/jobs/1/proposals")
    proposal_page.view_proposals()
    driver.save_screenshot(f"{SCREENSHOT_DIR}/tc351_job_proposals_viewed.png")
    print("✅ TC351 passed")

def test_accept_proposal(driver):  # TC352
    login_page = LoginPage(driver)
    driver.get(f"{BASE_URL}/login")
    login_page.login(EMAIL, PASSWORD)  # Assumes client role
    driver.get(f"{BASE_URL}/proposals/1")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Accept Proposal')]").click()  # Update locator
    wait = WebDriverWait(driver, 10)
    success = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Proposal status updated')]")))
    assert "Proposal status updated" in success.text
    driver.save_screenshot(f"{SCREENSHOT_DIR}/tc352_proposal_accepted.png")
    print("✅ TC352 passed")

def test_invalid_login(driver):  # TC353
    login_page = LoginPage(driver)
    driver.get(f"{BASE_URL}/login")
    error_message = login_page.login_with_invalid_credentials(EMAIL, "WrongPass123")
    assert "Invalid Email or Password" in error_message
    driver.save_screenshot(f"{SCREENSHOT_DIR}/tc353_invalid_login_error.png")
    print("✅ TC353 passed")

# Placeholder for TC354–TC390
# Add similar test functions following the same pattern, e.g.:
# def test_invalid_proposal_submission(driver):  # TC354
#     login_page = LoginPage(driver)
#     proposal_page = ProposalPage(driver)
#     driver.get(f"{BASE_URL}/login")
#     login_page.login(EMAIL, PASSWORD)
#     driver.get(f"{BASE_URL}/jobs/1")
#     # Implement invalid submission logic
#     driver.save_screenshot(f"{SCREENSHOT_DIR}/tc354_invalid_proposal_error.png")
#     print("✅ TC354 passed")
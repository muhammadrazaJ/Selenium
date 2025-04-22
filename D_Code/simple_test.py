import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

service = Service(executable_path='C:/Drivers/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service)

driver.get("https://hiring-hotspot.vercel.app")
print(driver.title)

time.sleep(5)  # Keeps browser open for 5 seconds
driver.quit()

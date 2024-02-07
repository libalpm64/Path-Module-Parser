# Made by libalpm 2024 
# This is a GNU LICENSE this free to use for any purpose
# Instructions:
# 1. Download the chrome driver from https://chromedriver.storage.googleapis.com/index.html
# 2. Download the latest chromium for linux (wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb) this may change in the future
# 3. dpkg -i install the package 
# 4. make sure you chmod the web driver
# 5. It's going to ask you to install a million dependcies as chrome is bloated.
# 6. Recommendation install this first: sudo apt-get install libnss3 then run apt-get --fix-broken install (for debian based distros)
# 7. Enter your paths and enter in your credentials.
# 8. Run the notifications.py
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Your path to the chrome driver you need to download it here https://googlechromelabs.github.io/chrome-for-testing/
service = Service(executable_path='/root/chromedriver')

driver = webdriver.Chrome(service=service, options=chrome_options)

# The login page I was using was spartan host for path module you may have to edit the script for other hosts depending on if they use the same theme or not or if the divs we are trying to retrive is different.
driver.get("https://billing.spartanhost.net/login")


WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'inputEmail')))

email_input = driver.find_element(By.ID, 'inputEmail')
password_input = driver.find_element(By.ID, 'inputPassword') 
login_button = driver.find_element(By.ID, 'login')

# Please put your exact login credentials (email and password)
email_input.send_keys('EMAILGOESHERE')
password_input.send_keys('Password')
login_button.click()

# I added this to 5 seconds because spartan host is unbelievably slow. // Edited so it only waits until the website loads 10 seconds is a timeout.
time.sleep(5)
driver.get("https://billing.spartanhost.net/clientarea.php?action=productdetails&id=55849")

# Yes another wait statement, again, this is spartan host specific. If you're using a different host that isn't the slowest loading site ever set it to 2-5 seconds. // Edited so it only waits until the website loads 10 seconds is a timeout.
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Open Control Panel')))
control_panel_button = driver.find_element(By.LINK_TEXT, 'Open Control Panel')
control_panel_button.click()

# Again, Spartan host specific unfortunately they can't make a site run fast. // Edited so it only waits until the website loads 10 seconds is a timeout.
WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
driver.switch_to.window(driver.window_handles[1])

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))


cookies = driver.get_cookies()
for cookie in cookies:
    print(f"{cookie['name']}={cookie['value']}")

# Properly exit the Chromium Driver instance
driver.quit()

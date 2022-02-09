from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pathlib import Path

import json
import time


from random import choice

path = Path(__file__).resolve().parent / 'config.json'
with open(path, 'r') as config_file:
	config_dict = json.load(config_file)
assert 0 < config_dict['number_of_bots'] < 1000

path = Path(__file__).resolve().parent / 'usernames.txt'
with open(path, 'r') as username_file:
	username_list = username_file.read().split('\n')
	username_file.close()

chrome_options = Options()
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--ignore-certificate-error')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument("log-level=3")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Can opt to remove this if you want, but I find it easier not to have the GUI
chrome_options.add_argument('-headless')

s = Path(__file__).resolve().parent / 'chromedriver.exe'
driver = webdriver.Chrome(executable_path=str(s), options=chrome_options)

print("Spawning bots...")

for i in range(config_dict['number_of_bots']):
	driver.get(config_dict['url'])
	try:
		nck_inp_element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.ID, 'nickname'))
		)
	except:
		driver.quit()

	username = choice(username_list)
	nck_inp_element.send_keys(username + Keys.ENTER)
	time.sleep(0.1)

	# No need to create a new tab if amt is just one
	if i < (len(range(config_dict['number_of_bots'])) - 1):
		driver.execute_script('''window.open("https://www.google.com", "_blank");''')
		driver.switch_to.window(driver.window_handles[i + 1])
print("Spawn complete!")
input("Press enter to start > ")

print("You may start the Kahoot game now.")
time.sleep(5)

# Implement random times to answer so it's not all instant
sec = [0.1, 0.2, 0.5]

try:
	while True:
		print("Waiting for answers...")
		setup = False
		while not setup:
			try:
				WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "sc-")]')))
				setup = True
			except Exception:
				time.sleep(1)

		print("Selecting answers..")
		for i in range(config_dict['number_of_bots']):
			driver.switch_to.window(driver.window_handles[i])
			answer_choices = driver.find_elements(By.XPATH, '//button[contains(@class, "sc-")]')
			try:
				element = choice(answer_choices)
				element.click()
			except Exception as e:
				print("Bots failed to answer! Skipping.")
				print(e)
			time.sleep(choice(sec))

			if i < (len(range(config_dict['number_of_bots'])) - 1):
				driver.switch_to.window(driver.window_handles[i + 1])
		print("Done!")
except KeyboardInterrupt:
	print("Shutting down browser..")
	driver.quit()
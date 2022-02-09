from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from pathlib import Path
from random import choice
from colorama import Fore

import json
import time

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
chrome_options.add_argument('log-level=3')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Can opt to remove this if you want, but I find it easier not to have the GUI
chrome_options.add_argument('-headless')

s = Service(Path(__file__).resolve().parent / 'chromedriver.exe')
driver = webdriver.Chrome(service=s, options=chrome_options)

print(Fore.GREEN + 'Spawning bots...', end='')

for i in range(config_dict['number_of_bots']):
	driver.get(config_dict['url'])
	try:
		nck_inp_element = WebDriverWait(driver, 10).until(
			ec.presence_of_element_located((By.ID, 'nickname'))
		)
	except:
		print('Invalid pin code entered.')
		driver.quit()

	nck_inp_element.send_keys(choice(username_list) + Keys.ENTER)
	time.sleep(0.1)

	print(Fore.GREEN + f'\rSpawned {i + 1} / {config_dict["number_of_bots"]} bots', end='')
	# No need to create a new tab if amt is just one
	if i < (len(range(config_dict['number_of_bots'])) - 1):
		driver.execute_script('''window.open('https://www.google.com', '_blank');''')
		driver.switch_to.window(driver.window_handles[i + 1])

print(Fore.YELLOW + f'\rSuccessfully spawned {config_dict["number_of_bots"]} bots!')
input('Press enter to start > ')

print(Fore.YELLOW + 'You may start the Kahoot game now.')
time.sleep(5)

# Implement random times to answer, so it's not all instant
# Change these time values if you would like, minimum values: 1. Smaller values means less delay in answering questions.
sec = [0.1, 0.2, 0.5]

try:
	while True:
		print(Fore.YELLOW + 'Waiting for answers...')

		setup = False
		while not setup:
			try:
				WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, '//button[contains(@class, "sc-")]')))
				setup = True
			except Exception:
				time.sleep(1)

		print(Fore.GREEN + 'Selecting answers...')
		for i in range(config_dict['number_of_bots']):
			driver.switch_to.window(driver.window_handles[i])
			answer_choices = driver.find_elements(By.XPATH, '//button[contains(@class, "sc-")]')
			try:
				element = choice(answer_choices)
				element.click()
			except Exception as e:
				print(Fore.RED + 'Bots failed to answer! Skipping.')
				print(Fore.RED + str(e))
			time.sleep(choice(sec))

			if i < (len(range(config_dict['number_of_bots'])) - 1):
				driver.switch_to.window(driver.window_handles[i + 1])

		print(Fore.GREEN + 'Done!')

except KeyboardInterrupt:
	print(Fore.RED + 'Shutting down browser...')
	driver.quit()

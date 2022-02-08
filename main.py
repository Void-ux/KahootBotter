from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pathlib import Path

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

firefox_option = Options()
firefox_option.add_argument('--disable-extensions')
s = Service(Path(__file__).resolve().parent / 'geckodriver.exe')
driver = webdriver.Firefox(service=s, options=firefox_option)

for i in range(config_dict['number_of_bots']):
	driver.get(config_dict['url'])
	try:
		nck_inp_element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.ID, 'nickname'))
		)
	except:
		driver.quit()

	nck_inp_element.send_keys(username_list[i] + Keys.ENTER)
	time.sleep(0.1)

	driver.execute_script('''window.open("https://www.google.com", "_blank");''')
	driver.switch_to.window(driver.window_handles[i + 1])

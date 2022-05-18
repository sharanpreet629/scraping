import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

path = r'D:\Scraping\chromedriver.exe'

driver = webdriver.Chrome(path)
driver.maximize_window()


driver.get('https://shopee.in/search?keyword=shoes%20for%20men')
time.sleep(5)

try:
    driver.switch_to.default_content()
    if driver.find_element(by='xpath', value= '//*[@id="modal"]/div[1]/div[1]/div/div[3]/div[2]/button') is not None:
        driver.find_element(by='xpath', value= '//*[@id="modal"]/div[1]/div[1]/div/div[3]/div[2]/button').click()
except NoSuchElementException:
    pass
l=[]
time.sleep(4)
previous_height = driver.execute_script('return document.body.scrollHeight')
while True:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    all_items = driver.find_elements(by='xpath', value= '//div[@class="_1gZS6z _1rL6dF"]')
    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == previous_height:
        break
    previous_height = new_height
    time.sleep(3)

print(len(all_items))
time.sleep(2)
#driver.execute_script('window.scrollTo(0,0);')
for item in all_items:
    names = item.find_elements(by='xpath', value= '//div[@class="_10Wbs- _2STCsK _3IqNCf"]')
for i in names:
    print(i.text)
print(len(names))
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

urls = ['https://www.careerguide.com/career-options', 'https://www.linkedin.com/']


driver.get(urls[0])
Category = driver.find_element(by='xpath', value='//a[@title="Engineering & Technology"]').text
sub_cat = [i.text for i in driver.find_elements(by='xpath', value="//div[5]/div[3]/ul/li")]
print(sub_cat)

time.sleep(5)

driver.get(urls[1])
Input = driver.find_element(by='xpath', value='//input[@autocomplete="username"]').send_keys('sharan1806671@gmail.com')
Password = driver.find_element(by='xpath', value='//input[@autocomplete="current-password"]').send_keys('sharan1806671')
Sign_in = driver.find_element(by= 'xpath', value='//button[@type="submit"]').click()
time.sleep(3)
print(driver.current_url)
jobs_icon = driver.find_element(by='xpath', value='(//span[@class="global-nav__primary-link-text"])[3]').click()
time.sleep(3)
print(driver.current_url)
try:
    if driver.find_element(by='xpath', value= '//div[@class="msg-overlay-bubble-header__controls display-flex"]/button[2]') is not None:
        driver.find_element(by='xpath', value= '//div[@class="msg-overlay-bubble-header__controls display-flex"]/button[2]').click()
except NoSuchElementException:
    pass

# try:
#     message_box = driver.find_element(by='xpath', value='//*[@id="ember243"]/li-icon').click()
# except Exception as e:
#     print('No msg-box')

search = driver.find_element(by= 'xpath', value='(//div[@class="relative"])[1]/input').send_keys(Category)
state = driver.find_element(by= 'xpath', value='//input[@aria-label="City, state, or zip code"]').send_keys('Delhi')
search_click = driver.find_element(by='xpath', value='(//button[@type="button"])[1]').click()

lists = []


time.sleep(2)
container_path = "//div[@class='jobs-search-results display-flex flex-column']/ul/li"
previous_height = driver.execute_script('return document.body.scrollHeight')
while True:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    all_items = driver.find_elements(by='xpath', value= container_path)
    time.sleep(5)
    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == previous_height:
        break
    previous_height = new_height
print(all_items)
driver.execute_script('window.scrollTo(0,0);')

for job in all_items:
    row=[]
    link = job.find_element(by='xpath', value='//a[@class="disabled ember-view job-card-container__link job-card-list__title"]')
    link.click()
    driver.get(link.get_attribute('href'))
    time.sleep(2)
    try:
        Name = job.find_element(by='class', value="t-24 t-bold")
    except Exception as ex:
        Name = 'NaN'
    finally:
        if Name == 'NaN':
            row.append(Name)
        else:
            row.append(Name.text)
    print(row)
    driver.back()
    time.sleep(2)



# for job in container:
#     row = []
#     job_position = job.find_element(by='xpath', value='//a[@class="disabled ember-view job-card-container__link job-card-list__title"]')
#     row.append(job_position.text)
#     print(row)
#     print(driver.current_url)
#     job_position.click()
#     print(driver.current_url)
#     time.sleep(3)
#     company_name= job_position.find_element(by='xpath', value=".//div[@class='ember-view t-black t-normal']").text
#     row.append(company_name)
#     print(row)
#     try:
#         working_location = job_position.find_element(by='class', value='job-card-container__metadata-item job-card-container__metadata-item--workplace-type').text
#         row.append(working_location)
#     except Exception as e:
#         working_location = job_position.find_element(by='class', value='//li[@class="job-card-container__metadata-item"]').text
#         row.append(working_location)
#     print(row)
#     lists.append(row)
#
# print(lists)


import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

path = r'D:\Scraping\chromedriver.exe'

driver = webdriver.Chrome(path)
driver.maximize_window()

A = []
N = []
C = []
Ad = []
P = []
L = []
W = []

container_p = "//div[@class='restaurant_row show ']"
#Name_p = "//a[@class= 'notranslate title_url']"
Name_p = "//div[@class='title']"
Website_p = "//a[@class= 'notranslate title_url']"
phone_p = "//a[@class='call']"
Category_p = "//div[@class='title']/span"
Address_p = "//div[@class='address']//div[2]"
location = "//div[@class= 'info_address']/a"
ads_p = "//div[@class='ads_block ads_item']"

driver.get('https://restaurantguru.com/restaurant-Portugal-t1')
parent_window = driver.current_window_handle

time.sleep(5)
previous_height = driver.execute_script('return document.body.scrollHeight')
while True:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    all_items = driver.find_elements(by='xpath', value= '//div[@class="restaurant_row show "]')
    time.sleep(5)
    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == previous_height:
        break
    elif len(all_items) > 500:
        break
    previous_height = new_height
print(len(all_items))

driver.execute_script('window.scrollTo(0,0);')
for i in all_items:
    try:
        Name = i.find_element(by='xpath', value=".//div[2]/div[2]/div/a")
    except Exception as ex:
        Name = 'NaN'
    finally:
        if Name == 'NaN':
            N.append(Name)
        else:
            N.append(Name.text)

    try:
        Category = i.find_element(by='xpath', value=".//div[2]/div[2]/div/span")
    except Exception as ex:
        Category = 'NaN'
    finally:
        if Category == 'NaN':
            C.append(Category)
        else:
            C.append(Category.text.replace('/','').strip())

    Name = i.find_element(by='xpath', value=".//div[2]/div[2]/div/a")
    Name.click()
    child_windows = driver.window_handles
    time.sleep(2)
    for child in child_windows:
        if parent_window != child:
            driver.switch_to.window(child)
            time.sleep(2)
            try:
                Phone = driver.find_element(by='xpath', value=".//div[2]/div[1]/div[1]/div/a/span")
            except Exception as ex:
                Phone = 'NaN'
            finally:
                if Phone == 'NaN':
                    P.append(Phone)
                else:
                    P.append(Phone.text)

            try:
                Address = driver.find_element(by='xpath', value="//*[@id='info_location']/div[2]")
            except Exception as ex:
                Address = 'NaN'
            finally:
                if Address == 'NaN':
                    Ad.append(Address)
                else:
                    Ad.append(Address.text)

            try:
                Website = driver.find_element(by='xpath', value="//div[4]/div/div[4]/div[2]/a")
            except Exception as ex:
                Website = 'NaN'
            finally:
                if Website == 'NaN':
                    W.append(Website)
                else:
                    W.append(Website.get_attribute('href'))

            try:
                Location = driver.find_element(by='xpath', value= location)
            except Exception as ex:
                Location = 'NaN'
            finally:
                if Location == 'NaN':
                    L.append(Location)
                else:
                    L.append(Location.get_attribute('href').split('=')[-1].replace(',','; '))

            driver.close()
        driver.switch_to.window(parent_window)
        #driver.execute_script('window.scrollBy(0,200);')

print(len(P), len(L), len(Ad), len(W))
dict = {'Restaurant Name': N,'Restaurant Catogory': C, 'Restaurant Website': W, 'Restaurant Contact':P, 'Restaurant Address': Ad, 'Location': L}
df = pd.DataFrame(dict)
df.to_csv('Restaurant_guru.csv')
print(df)






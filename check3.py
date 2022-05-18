import time

import pandas as pd
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

path = r'C:\Users\DELL\OneDrive\Desktop\Scraping\chromedriver.exe'

browser = webdriver.Chrome(executable_path=path)
browser.get('https://www.pai.pt/restaurantes')
parent_window = browser.current_window_handle

browser.maximize_window()
print(browser.current_url)

restaurant_name = "//a[@class='card-link']"
restaurant_desc = "//p[@class='card-description']"
restaurant_location = "//div[@class='cell card-address sm:mt-10 lg:mt-0']"
restaurant_website = "//a[@class='card-link']"
restaurant_call = "//button[@name='button']"

website = []
name = []
description = []
location = []
call = []
website_1 = []

# input_search1 = browser.find_element(by="id", value = 'search_query')
# input_search1.send_keys('Restaurant')
#
# input_search2 = browser.find_element(by="id", value = 'search_location_value')
# input_search2.clear()
# input_search2.send_keys('Portugal')
# browser.find_element(by= "xpath", value= "(//input[@class='magnifying-glass show-for-large'])").click()
# child_windows = browser.window_handles
# time.sleep(2)
# print(child_windows)

# for child in child_windows:
#     if parent_window == child:
#         browser.switch_to.window(child)
#         time.sleep(2)
# print(browser.current_url)
for page in range(200):
    print(browser.current_url)
    print(f'Scraping Page {page + 1}')
    time.sleep(4)
    all_items = browser.find_elements(by='xpath', value= '//div[@class="card card--result mb-25"]')
    #print([i.text for i in all_items])
    for i in all_items:
        try:
            Name = i.find_element(by='xpath', value= ".//div/div[2]/div/h5")
        except Exception as ex:
            Name = 'NaN'
        finally:
            if Name=='NaN':
                name.append(Name)
            else:
                name.append(Name.text)


        try:
            Description = i.find_element(by='xpath', value=".//div/div[2]/div/div[2]/div[1]/p")
        except Exception as ex:
            Description = 'NaN'
        finally:
            if Description=='NaN':
                description.append(Description)
            else:
                description.append(Description.text)



        try:
            Location = i.find_element(by='xpath', value=".//div/div[2]/div/div[2]/div[3]")
        except Exception as ex:
            Location = 'NaN'
        finally:
            if Location=='NaN':
                location.append(Location)
            else:
                location.append(Location.text.replace('\n',''))



        try:
            Website = i.find_element(by='xpath', value=".//div/div[2]/div/h5/a")
        except Exception as ex:
            Website = 'NaN'
        finally:
            if Website=='NaN':
                website.append(Website)
            else:
                website.append(Website.get_attribute('href'))


        try:
            Call = i.find_element(by='xpath', value=".//div/div[2]/div/button")
        except Exception as ex:
            Call = 'NaN'
        finally:
            if Call=='NaN':
                call.append(Call)
            else:
                call.append(Call.get_attribute('value'))

        try:
            Name = i.find_element(by='xpath', value=".//div/div[2]/div/h5")
            print(Name.text)
            Name.click()
            time.sleep(2)
            Website_1 = browser.find_element(by='xpath', value="(//li[@class='listing-item'])[5]/a")
        except Exception as ex:
            Website_1 = 'NaN'
        finally:
            if Website_1 == 'NaN':
                website_1.append(Website_1)
            else:
                website_1.append(Website_1.get_attribute('href'))
            # browser.back()
            # browser.switch_to.window(parent_window)
            browser.execute_script("window.history.go(-1)")
            browser.implicitly_wait(5)
            # browser.execute_script("window.scrollBy(0, 200);")
            print(website_1)
            print(browser.current_url)
    if page <200:
        browser.find_element(by='xpath', value='//li[@class="next"]').click()

        time.sleep(2)

print(len(name), len(website), len(description), len(location), len(call))


dict = {'Restaurant Name': name, 'Restaurant Description': description,'Restaurant Website': website, 'Restaurant Location': location, 'Restaurant Contact': call}
df = pd.DataFrame(dict)
print(df)
df.to_csv('portugal_data1.csv', index=False)
df1 = pd.read_csv('portugal_data1.csv')
df1.head(10)
# //*[@id="results"]/div[2]/div[1]/div/div[2]/div[3]/div/div[2]/div/h5
# //*[@id="results"]/div[2]/div[1]/div/div[2]/div[4]/div/div[2]/div/h5/a
# //*[@id="results"]/div[2]/div[1]/div/div[2]/div[5]/div/div[2]/div/h5/a

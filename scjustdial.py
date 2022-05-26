from selenium import webdriver
import undetected_chromedriver as uc
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.proxy import Proxy, ProxyType
from pytesseract import image_to_string
from selenium.webdriver.common.by import By
import os, pyperclip, re, send2trash
from selenium.webdriver.common.keys import Keys
from PIL import Image
import phonenumbers
import time
import pandas as pd



location_input = input('Enter the city name: ').capitalize()
shops_input = input('Enter the category of shops: ')


options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
driver = uc.Chrome(options=options)

# driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)



# driver = webdriver.Chrome(ChromeDriverManager().install())
count = 1

# print(height)
matches = []
new = []
Names = []
dict_service = {}

page_number = 1
# driver.get('https://www.justdial.com/Ludhiana/Restaurants-in-Vishkarma-Chowk/nct-10408936')

driver.get('https://www.justdial.com')
driver.maximize_window()
time.sleep(2)
location= driver.find_element(By.ID,'city')

try:
    location.clear()
except:
    location.click()
time.sleep(1)

location.send_keys(location_input)
location.send_keys(Keys.ARROW_DOWN)

first_option = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//ul[@id="cuto"]/li/a[1]')))
first_option.send_keys(Keys.RETURN)
time.sleep(2)
input_key=driver.find_element(By.ID,'srchbx')
time.sleep(1)

input_key.send_keys(shops_input)
time.sleep(2)
search_button=driver.find_element(By.XPATH,'//*[@id="search"]/button')
time.sleep(1)
search_button.click()
current_url = driver.current_url
while True:
    # Check if reached end of result
    if page_number > 10:
        break
    print(page_number)
    url = '%s/page-%s' % (current_url, page_number)
    print(url)
    driver.get(url)
    time.sleep(5)


    sleep(1)

    height = driver.execute_script("return document.body.scrollHeight")
    for scrol in range(200, height-3000, 500):
        driver.execute_script(f"window.scrollTo(0,{scrol})")
        time.sleep(0.5)
        try:
            popup_message = driver.find_element(By.XPATH, '//*[@id="best_deal_div"]/section/span')
            time.sleep(5)
            popup_message.click()
            time.sleep(2)
        except:
            pass
        driver.get_screenshot_as_file(f"screenshot.png")
        all_text = []

        img = Image.open('screenshot.png')
        all_text.append(image_to_string(img))
        print(len(all_text))

        phone_regex = re.compile(
            r'''((\+91|0)?                                  (\s|-|\.)?                                 (\d{5})                                    (\s|-|\.)?                                  (\d{5})                                     )''',
            re.VERBOSE)

        # text = str('\n'.join(all_text))

        text_list = all_text[0].split('\n')
        # text2 = []
        for i in text_list:
            if i == ' ' or i == '  ' or i == '':
                text_list.remove(i)
        print(text_list)
        for i, text in enumerate(text_list):
            for match in phonenumbers.PhoneNumberMatcher(text, "GB"):
                matches.append(str(match).split(' ')[-1])
                print(str(match).split(' ')[-1])
                Name = text_list[i-2]
                Names.append(Name)
                print(Names)
                print(matches)
                print(len(Names), len(matches))
    page_number += 1

driver.quit()
print("end...")

for name, phone in zip(Names, matches):
    if name==" " or name== '':
        Names.remove(name)
        matches.remove(phone)


dict_service['Names'] = Names
dict_service['Phone'] = matches
print(dict_service)

df = pd.DataFrame(dict_service)

df.to_csv('scjustdial1.csv')

# for i in matches:
#     if i not in new:
#         new.append(i)
# print(new)
# driver.execute_script(f"window.scrollTo(0, 200)")
# driver.get_screenshot_as_file("screenshot.png")

# all_text = []
#
# img = Image.open('screenshot.png')
# all_text.append(image_to_string(img))
# print(all_text)
#
# phone_regex = re.compile(r'''((\+91|0)?                                  (\s|-|\.)?                                 (\d{5})                                    (\s|-|\.)?                                  (\d{5})                                     )''', re.VERBOSE)
#
# text = str('\n'.join(all_text))
# print(text)
# matches = []
# for match in phonenumbers.PhoneNumberMatcher(text, "GB"):
#     print(str(match).split(' ')[-1])
# phone_num = ''
# for groups in phone_regex.findall(text):
#     print(groups)
#     phone_num = ''.join([groups[3], groups[5]])
#     matches.append(phone_num)
#
# print(matches)
#
# if len(matches) > 0:
#     distinct_matches = list(dict.fromkeys(matches))
#
#     if len(matches)!=len(distinct_matches):
#         print(str(len(matches)-len(distinct_matches)) + ' Duplicates Removed')
#     else:
#         print('No duplicates found!')
#
#     # pyperclip.copy('\n'.join(distinct_matches))
#     # print('Copied to clipboard')
# else:
#     print('No Phone no. was found!!')

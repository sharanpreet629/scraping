from selenium import webdriver
import undetected_chromedriver as uc
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.proxy import Proxy, ProxyType
from pytesseract import image_to_string
from selenium.webdriver.common.by import By
import os, pyperclip, re, send2trash
from PIL import Image
import phonenumbers
import time
import pandas as pd
import random

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
while True:

    # Check if reached end of result
    if page_number > 10:
        break
    driver.get('https://www.justdial.com/Ludhiana/Restaurants-in-Vishkarma-Chowk/nct-10408936/page-%s' % (page_number))
    time.sleep(2)
    driver.maximize_window()

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
dict_service['Names'] = Names
dict_service['Phone'] = matches
print(dict_service)

df = pd.DataFrame(dict_service)

df.to_csv('retaurant.csv')

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

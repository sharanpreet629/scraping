from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time, os
import urllib.request
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select

name = []
location = []
contact = []
links = []
area_list = []
opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
driver.get('https://www.zomato.com/')
driver.execute_script(f"window.scrollTo(0,300)")
see_more = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[4]/div[3]/div[2]/div/div[9]/div/i')
see_more.click()
time.sleep(10)
areas = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[4]/div[3]/div[2]/div/div')
for i in areas:
    try:
        area = i.find_element(By.TAG_NAME, 'h5')
        area_list.append(area.text)
        links.append(i.find_element(By.XPATH,'.//a').get_attribute('href'))
    except Exception as e:
        continue

print(links)
print(area_list)
print(len(links), len(area_list))

for i in links[:1]:
    time.sleep(2)
    driver.get(i)
    time.sleep(5)
    driver.refresh()
    time.sleep(5)
    scroll_pause_time = 2  # You can set your own pause time. dont slow too slow that might not able to load more data
    screen_height = driver.execute_script("return window.screen.height;")  # get the screen height of the web
    i = 1

    while True:
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        i += 1
        time.sleep(scroll_pause_time)
        container = driver.find_elements(By.XPATH, '//div[@class="jumbo-tracker"]/div/a')
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height) * i > scroll_height:
            break
        elif len(container) > 150:
            break
    print('helo')
    base = "https://www.zomato.com"
    # container = driver.find_elements(By.XPATH, '//div[@class="jumbo-tracker"]/div/a')
    print('hyy')
    shop_links = [l.get_attribute('href') for l in container]
    #driver.execute_script(f"window.history.go(-1)")
    print(len(container))
    print(shop_links)
    # driver.execute_script(f"window.scrollTo(0,700)")
    for i in shop_links:
        print(i)
        if i.split('/')[-1]=='order':
            l = "/".join(i.split('/')[:-1])
            print(l)
            print('yoo')
            driver.get(l)
            time.sleep(5)
            Name = driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div/section[3]/section/section/div/div/div/h1').text
            article = driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div/section[4]/section/article')
            call = article.find_elements(By.XPATH, './p')
            address = article.find_element(By.XPATH, './section/p').text
            name.append(Name)
            location.append(address)
            contact.append([c.text for c in call])

print(name)
print(location)
print(contact)
print(len(name), len(location), len(contact))

dictionary = {}
dictionary['Product Name'] = name
dictionary['Product type'] = location
dictionary['Product catogary'] = contact
df = pd.DataFrame(dictionary)

df.to_csv('zomato.csv')

driver.close()
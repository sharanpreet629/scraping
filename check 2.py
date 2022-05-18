import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



path = r'C:\Users\DELL\OneDrive\Desktop\Scraping\chromedriver.exe'

driver = webdriver.Chrome(path)
driver.maximize_window()


A = []
N = []
C = []
Ad = []
P = []
L = []
R_n= []
R_c = []

container_p = "//div[@class='restaurant_row show ']"
#Name_p = "//a[@class= 'notranslate title_url']"
Name_p = "//div[@class='title']"
Website_p = "//a[@class= 'notranslate title_url']"
phone_p = "//a[@class='call']"
Category_p = "//div[@class='title']/span"
Address_p = "//div[@class='address']//div[2]"
location = "//iframe[@class='map_container']"
ads_p = "//div[@class='ads_block ads_item']"

driver.get('https://restaurantguru.com/restaurant-Portugal-t1')
parent_window = driver.current_window_handle
#print(parent_window)
#driver.execute_script("window.scrollBy(0,1000);")
time.sleep(5)

container = driver.find_elements(by= 'xpath', value= container_p)
all_iframes = driver.find_elements(By.TAG_NAME, "iframe")
if len(all_iframes) > 0:
    driver.execute_script("""
            var elems = document.getElementsByTagName("iframe"); 
            for(var i = 0, max = elems.length; i < max; i++)
                 {
                     elems[i].hidden=true;
                 }
                              """)
#driver.execute_script("window.scrollBy(0,-1000);")
previous_height = driver.execute_script('return document.body.scrollHeight')

# print(len(container))
try:
    #for contain in container:
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(5)

        Page_links = driver.find_elements(by= 'xpath', value= Name_p)
        for i in Page_links:
            if i==[]:
                A.append('Null')
            else:
                A.append(i)
        print(len(A))
        # Category = driver.find_elements(by='xpath', value=Category_p)
        # for i in Category:
        #     if i==[]:
        #         C.append('Not Given')
        #     else:
        #         C.append(i.text.replace('/','').strip())
        # print(len(C))
        Name = driver.find_elements(by='xpath', value=Name_p)
        for i in Name:
            if i==[]:
                N.append('Null')
            else:
                N.append(i.text)
        print(len(N))
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == previous_height:
            break
        elif len(A)>37:
            break
        previous_height = new_height

    time.sleep(3)
    driver.execute_script('window.scrollTo(0,0);')
    time.sleep(3)

    while True:
        driver.execute_script('window.scrollTo(0,0);')
        for link in A:
            time.sleep(3)
            all_iframes = driver.find_elements(By.TAG_NAME, "iframe")
            if len(all_iframes) > 0:
                driver.execute_script("window.scrollBy(0,100);")

            #driver.execute_script('window.scrollTo(0, 0);')
            print(link.text)
            link.click()
            child_windows = driver.window_handles
            time.sleep(2)

            for child in child_windows:

                if parent_window!=child:
                    driver.switch_to.window(child)
                    time.sleep(5)
                    Phone = driver.find_elements(by='xpath', value=phone_p)
                    if len(Phone)==0:
                        P.append('Null')
                    else:
                        for i in Phone:
                            P.append(i.get_attribute('href'))
                    Address = driver.find_elements(by='xpath', value=Address_p)
                    if len(Address)==0:
                        Ad.append('Null')
                    else:
                        for i in Address:
                            Ad.append(i.text)
                    Location = driver.find_elements(by='xpath', value=location)
                    if len(Location)==0:
                        L.append('Null')
                    else:
                        for i in Location:
                            L.append(i.get_attribute('src'))
                    driver.close()
                driver.switch_to.window(parent_window)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == previous_height:
            break
        elif len(P) > 37:
            break
        previous_height = new_height
except Exception as e:
    print(e)
finally:
    # for i in N:
    #     l = i.split('/')
    #     R_n.append(l[0])
    #     R_c.append(l[1])

    dict = {'Restaurant Name': N, 'Phone':P, 'Address': Ad, 'Location': L}
    print(len(N),len(P),len(Ad),len(L))
    print(dict)
    df = pd.DataFrame(dict)
    print(df)
    df.to_csv('rest.csv')

    df['Restaurant Catogory'] = df['Restaurant Name'].apply(lambda x: x.split('/')[1], axis=1)
    df['Restaurant Name'] = df['Restaurant Name'].apply(lambda x: x.split('/')[0], axis=1)
    df['Restaurant Website'] = [i.get_attribute('href') for i in A]
    df.to_csv('rest.csv')

    print(len(A))
    print(len(N))
    print(len(P))

# dict = {'Restaurant Name':N, 'Category':C, 'Website':container}
# df = pd.DataFrame(data= dict)
# print(df)

#scroll upto end of the page
# previous_height = driver.execute_script('return document.body.scrollHeight')
# while True:
#     driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
#     time.sleep(2)
#     new_height = driver.execute_script('return document.body.scrollHeight')
#     if new_height==previous_height:
#         break
#     previous_height=new_height

# scroll upto element
# element_p = "//a[contains(text(), 'Adega Regional')]"
# element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, element_p)))
# print(element)
# driver.execute_script("arguments[0].scrollIntoView();", element)

# scroll using pixels








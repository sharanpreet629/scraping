import pandas as pd
from selenium import webdriver
from time import sleep

path = r'C:\Users\DELL\OneDrive\Desktop\Scraping\chromedriver.exe'

browser = webdriver.Chrome(executable_path=path)
browser.get('https://www.amazon.in/')

browser.maximize_window()
print(browser.current_url)

input_search = browser.find_element(by="id", value = 'twotabsearchtextbox')
input_search.send_keys('Smartphones under 10000')
browser.find_element(by= "xpath", value= "(//input[@type= 'submit'])[1]").click()
print(browser.current_url)
#browser.find_element(by='xpath', value= "(//i[@class='a-icon a-icon-checkbox'])[2]").click()

sleep(1)


product_class= "//span[@class='a-size-medium a-color-base a-text-normal']"
price_class = "//span[@class='a-price-whole']"
rating_class = "//span[@class='a-icon-alt']"


products = []
Prices = []
Rating = []

for i in range(10):
    print('Scraping Page', i+1)
    product = browser.find_elements(by= 'xpath', value = product_class)
    # price = browser.find_elements(by='xpath', value= price_class)
    # rating = browser.find_elements(by='xpath', value=rating_class)
    for p in product:
        products.append(p.text)
    # for q in price:
    #     Prices.append(q.text)
    #

    # for r in rating:
    #     Rating.append(r.text)
    browser.find_element(by = 'xpath', value= '//li[@class="a-last"]').click()

    sleep(1)

print(products)
print(browser.current_url)



pro_dict = {'Product Names':products, 'Prices': Prices, 'Ratings' : Rating}
# print(pro_dict)
# for i in Rating:
#     if products[i]=="":
#         Rating.remove(i)

print(len(Prices))
print(len(Rating))
print(len(products))

df = pd.DataFrame(data = pro_dict['Product Names'], columns= ['Titles'])
#df['Prices'] = Prices
print(df)




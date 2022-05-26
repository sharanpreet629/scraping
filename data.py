from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time, os
import urllib.request
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select

product_image = []
product_name = []
product_type = []
product_cat = []
product_thc = []
product_oz = []
product_price = []
product_detail = []

dir = os.getcwd()
photos_dir = os.path.join(dir, r'photos')
if not os.path.exists(photos_dir):
   os.makedirs(photos_dir)

opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
driver.get('https://curaleaf.com/shop/florida/curaleaf-dispensary-bonita-springs?')

try:
    popup_button=driver.find_element(By.XPATH,'//div[@class="cta-button-curaleaf"]')
    time.sleep(1)
    popup_button.click()
except:
    pass
time.sleep(1)

secound_popup=driver.find_element(By.CLASS_NAME,'mailingOptIn_close__VO7xF')
secound_popup.click()
time.sleep(1)
driver.execute_script("window.scrollTo(0,400)")

driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))
a = ActionChains(driver)
dropdown = driver.find_element(By.XPATH,'//button[@tabindex="0"]')
time.sleep(2)
a.move_to_element(dropdown).perform()
time.sleep(2)
# print(dropdown)
dropdown.click()

list_elements = driver.find_elements(By.XPATH, '//ul[@role="menu"]/li')
# print(list_elements)
for i in list_elements:
    print(i.text)
count=0
for link in list_elements:
    print(count)
    links = []
    if count==0:
        link.click()
    driver.switch_to.parent_frame()
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)
    driver.switch_to.frame(driver.find_element(By.XPATH, '//iframe[@class="dutchie--iframe"]'))
    container = driver.find_elements(By.XPATH, '//*[@id="main-content"]/div[2]/div/div')
    # container_link = driver.find_elements(By.XPATH, '//a[@class="desktop-product-list-item__ProductInfoContainer-sc-8wto4u-4 jTTcVS"]')
    # links = [con.get_attribute('href') for con in container_link]
    url = driver.current_url
    print(url)
    print(len(container))
    driver.switch_to.parent_frame()

    height = driver.execute_script("return document.body.scrollHeight")
    print(height)
    # for scrol in range(400, height, 600):
    #driver.execute_script(f"window.scrollTo(0,450)")
    # driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))
    time.sleep(2)
    for product in container:
        time.sleep(2)
        print(product)

        # driver.execute_script(f"window.scrollBy(0,100)")
        driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))
        driver.execute_script("arguments[0].scrollIntoView();", product)
        try:
            products_name = product.find_element(By.XPATH, './/div[@class="desktop-product-list-item__ProductNameContainer-sc-8wto4u-12 bMVVKM"]/span').text
            product_name.append(products_name)
        except Exception as e:
            products_name = " "
            product_name.append(products_name)
        print(products_name)

        try:
            products_image = product.find_element(By.XPATH, './/div[@class="desktop-product-list-item__ProductImageContainer-sc-8wto4u-15 ecIWrT"]/img').get_attribute('data-src')
            urllib.request.install_opener(opener)
            path = f"{photos_dir}/{str(products_name)}.jpg"
            urllib.request.urlretrieve(products_image, path)
            product_image.append(path)
            print(path)
        except Exception as e:
            products_image = " "
            product_image.append(products_image)
        print(products_image)

        try:
            products_type = product.find_element(By.XPATH, './/span[@class="desktop-product-list-item__ProductBrand-sc-8wto4u-6 bUxuOp"]').text
            product_type.append(products_type)
        except Exception as e:
            products_type = " "
            product_type.append(products_type)
        print(products_type)
        try:
            products_cat = product.find_element(By.XPATH,'.//p[@class="desktop-product-list-item__StrainText-sc-8wto4u-13 gfWvo"]' ).text
            product_cat.append(products_cat)
        except Exception as e:
            products_cat = " "
            product_cat.append(products_cat)
        print(products_cat)

        try:
            products_thc = product.find_element(By.XPATH,'.//div[@class="desktop-product-list-item__PotencyInfo-sc-8wto4u-14 hdncuE"]').text
            product_thc.append(products_thc)
        except Exception as e:
            products_thc = " "
            product_thc.append(products_thc)
        print(products_thc)

        try:
            products_oz = product.find_element(By.XPATH, './/span[@class="weight-tile__Label-otzu8j-4 hYKiO"]').text
            product_oz.append(products_oz)
        except Exception as e:
            products_oz = " "
            product_oz.append(products_oz)
        print(products_oz)

        try:
            products_price = product.find_element(By.XPATH,'.//span[@class="weight-tile__PriceText-otzu8j-5 hJFddt"]').text
            product_price.append(products_price)
        except Exception as e:
            products_price = " "
            product_price.append(products_price)
        print(products_price)
        time.sleep(2)
        link = product.find_element(By.XPATH, './/a[@class="desktop-product-list-item__ProductInfoContainer-sc-8wto4u-4 jTTcVS"]').get_attribute('href')
        links.append(link)
        print(link)
        # link.click()
        # time.sleep(2)
        # try:
        #     products_detail = driver.find_element(By.XPATH, '//div[@class="sanitized-html__Wrapper-fpulka-0 gSLdKa"]/p').text
        #     product_detail.append(products_detail)
        # except Exception as e:
        #     products_detail = " "
        #     product_detail.append(products_detail)
        # print(products_detail)
        # driver.get(url)
        # # driver.execute_script("window.history.go(-1)")
        # time.sleep(5)
        # driver.execute_script("window.scrollTo(0,500)")
        # print(driver.current_url)
        # product_image.append(products_image)
        # product_name.append(products_name)
        # product_type.append(products_type)
        # product_cat.append(products_cat)
        # product_thc.append(products_thc)
        # product_price.append(products_price)

        # for i in products_image:
        #     product_image.append(i.get_attribute('src'))
        # for i in products_name:
        #     product_name.append(i.text)
        # for i in products_type:
        #     product_type.append(i.text)
        # for i in products_cat:
        #     product_cat.append(i.text)
        # for i in products_thc:
        #     product_thc.append(i.text)
        # # for i in products_oz:
        # #     product_oz.append(i.text)
        # for i in products_price:
        #     product_price.append(i.text)

        time.sleep(3)
        driver.switch_to.parent_frame()
    for link in links:
        driver.get(link)
        time.sleep(2)
        try:
            products_detail = driver.find_element(By.XPATH, '//div[@class="sanitized-html__Wrapper-fpulka-0 gSLdKa"]/p').text
            product_detail.append(products_detail)
        except Exception as e:
            products_detail = " "
            product_detail.append(products_detail)
        print(products_detail)
    print(len(product_detail))

    driver.execute_script(f"window.history.go(-{len(links)})")
    time.sleep(5)
    driver.execute_script(f"window.scrollTo(0,450)")
    for name, type, cat, thc, price in zip(product_name, product_type, product_cat, product_thc, product_price):
        print(name, " ", type," ", cat," ",thc," ",  " ", price)

    #driver.execute_script("window.history.go(-1)")
    time.sleep(3)
    driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))
    a = ActionChains(driver)
    dropdown = driver.find_element(By.XPATH, '//button[@tabindex="0"]')
    time.sleep(2)
    a.move_to_element(dropdown).perform()
    time.sleep(5)
    # dropdown.click()
    l = driver.find_elements(By.XPATH, '//ul[@role="menu"]/li')
    print(len(l))
    count = count+1
    if count<len(list_elements):
        l[count].click()
        time.sleep(5)

# for product in container:
#     driver.execute_script("window.scrollBy(0, -document.body.scrollHeight);")
#     print('yoo')
#     product.find_element(By.CLASS_NAME,"desktop-product-list-item__ProductImageContainer-sc-8wto4u-15 ecIWrT")
#     print(product)
dictionary = {}
dictionary['Product Name'] = product_name
dictionary['Product type'] = product_type
dictionary['Product catogary'] = product_cat
dictionary['Product THC'] = product_thc
dictionary['Product OZ'] = product_oz
dictionary['Product Price'] = product_price
dictionary['Product Image'] = product_image
dictionary['Product Detail'] = product_detail

df = pd.DataFrame(dictionary)

df.to_csv('curaleaf.csv')
driver.close()
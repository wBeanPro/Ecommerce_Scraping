import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import csv
import os


class ScrapePlaces:
    def __init__(self):
        self.driver = webdriver.Chrome('./chromedriver')
        self.login()
        self.getHardProduct()
        self.getSoftProduct()
    def login(self):
        self.driver.get('https://www.brandboom.com/login')
        self.driver.find_element(By.NAME, 'email').send_keys('mark@boardwest.com')
        self.driver.find_element(By.NAME,'password').send_keys('Wheels001')
        self.driver.find_elements(By.CLASS_NAME,'login-btn')[-1].click()
    def getHardProduct(self):
        url = "https://www.brandboom.com/app/a/FEE6EB1005B"
        self.driver.get(url)
        product_list = self.driver.find_elements(By.CLASS_NAME, 'product-tile')
        self.df = pd.DataFrame()
        self.product_index = 0
        self.new_product = 0
        self.first_scraping_flag = True
        if os.path.isfile("product_list.csv"):
            self.df = pd.read_csv('product_list.csv')
            self.product_index = len(self.df)
            self.first_scraping_flag = False
        print("current product count: ", self.product_index)
        for i in range(len(product_list)):
            link = "https://www.brandboom.com/app/a/FEE6EB1005B" + "/p/" + product_list[i].get_attribute('data-product-id')
            if self.first_scraping_flag or not self.df['url'].str.contains(link).any():
                self.df.at[self.product_index,'url'] = link
                self.df.to_csv("product_list.csv", index=False)
                self.product_index += 1
                self.new_product += 1
        if self.new_product != 0:
            print("we found new ",self.new_product," Hard products.")
        else:
            print("There is no new Hard product.")
    def getSoftProduct(self):
        url = "https://www.brandboom.com/app/a/D14C4B37293"
        self.driver.get(url)
        product_list = self.driver.find_elements(By.CLASS_NAME, 'product-tile')
        self.df = pd.DataFrame()
        self.product_index = 0
        self.new_product = 0
        self.first_scraping_flag = True
        if os.path.isfile("product_list.csv"):
            self.df = pd.read_csv('product_list.csv')
            self.product_index = len(self.df)
            self.first_scraping_flag = False
        print("current product count: ", self.product_index)
        for i in range(len(product_list)):
            link = "https://www.brandboom.com/app/a/D14C4B37293" + "/p/" + product_list[i].get_attribute('data-product-id')
            if self.first_scraping_flag or not self.df['url'].str.contains(link).any():
                self.df.at[self.product_index,'url'] = link
                self.df.to_csv("product_list.csv", index=False)
                self.product_index += 1
                self.new_product += 1
        if self.new_product != 0:
            print("we found new ",self.new_product," Hard products.")
        else:
            print("There is no new Hard product.")
    def closeDriver(self):
        print("\n\nEnding Scrapper Session")
        self.driver.close()
    def getInformation(self):
        df = pd.read_csv('product_list.csv')
        info_df = pd.DataFrame()
        info_index = 0
        if os.path.isfile("result.csv"):
            info_df = pd.read_csv('result.csv')
            info_index = len(info_df)
        urlList = df["url"].tolist()
        self.driver.get('https://dealer.yocaher.com/login.php')
        self.driver.find_element(By.ID,'login_email').send_keys('mark@boardwest.com')
        self.driver.find_element(By.ID,'login_pass').send_keys('Streetwise85373')
        self.driver.find_element(By.CLASS_NAME,'form-actions').find_element(By.TAG_NAME,'input').click()
        for i in range(len(urlList)):
            link = urlList[i]
            if not 'Handle' in info_df.columns or not info_df['Handle'].str.contains(link.split('/')[-2]).any():
                if 'sola' in link and 'ski' in link:
                    continue
                self.driver.get(link)
                info_df.at[info_index,'Handle'] = link.split('/')[-2]
                original_title = self.driver.find_element(By.CLASS_NAME,'productView-title').text
                title = original_title.replace(' - ',' ').title().replace('Mm',"MM")
                info_df.at[info_index,'Title'] = title
                description = self.driver.find_element(By.ID,'accordion--description').find_element(By.TAG_NAME,'div').get_attribute('innerHTML')
                seo_description = self.driver.find_element(By.ID,'accordion--description').find_element(By.TAG_NAME,'div').text
                description_item = self.driver.find_element(By.ID,'accordion--description').find_elements(By.TAG_NAME,'li')
                color = 'Multi'
                hardness = ''
                detail_size = ''
                hanger = ''
                Graphic = ''
                deck_size = ''
                length = ''
                speed = ''
                for j in range(len(description_item)):
                    if '<strong>' in description_item[j].get_attribute('innerHTML'):
                        if 'Color:' in description_item[j].find_element(By.TAG_NAME,'strong').text:
                            color = description_item[j].get_attribute('innerHTML').split('</strong>')[1]
                        if 'Hardness' in description_item[j].find_element(By.TAG_NAME,'strong').text:
                            hardness = description_item[j].get_attribute('innerHTML').split('</strong>')[1]
                        if 'Size' in description_item[j].find_element(By.TAG_NAME,'strong').text:
                            detail_size = description_item[j].get_attribute('innerHTML').split('</strong>')[1]
                        if 'Hanger' in description_item[j].find_element(By.TAG_NAME,'strong').text:
                            hanger = description_item[j].get_attribute('innerHTML').split('</strong>')[1]
                        if 'Graphic' in description_item[j].find_element(By.TAG_NAME,'strong').text:
                            Graphic = description_item[j].get_attribute('innerHTML').split('</strong>')[1].replace('&nbsp;','').replace(':','')
                            if Graphic == '':
                                Graphic = description_item[j].text.split('Graphic:')[1].replace('&nbsp;','').replace(':','')
                        if 'Deck Size' in description_item[j].find_element(By.TAG_NAME,'strong').text:
                            deck_size = description_item[j].get_attribute('innerHTML').split('</strong>')[1].replace('&nbsp;','').replace(':','')
                        if 'Length' in description_item[j].find_element(By.TAG_NAME,'strong').text:
                            length = description_item[j].get_attribute('innerHTML').split('</strong>')[1]
                        if 'Speed' in description_item[j].find_element(By.TAG_NAME,'strong').text:
                            speed = description_item[j].get_attribute('innerHTML').split('</strong>')[1]
                    else:
                        if 'Graphic:' in description_item[j].text:
                            Graphic = description_item[j].text.split('Graphic:')[1].replace('&nbsp;','').replace(':','')
                        if 'Deck Size:' in description_item[j].text:
                            deck_size = description_item[j].text.split('Deck Size:')[1].replace('&nbsp;','').replace(':','')
                
                info_df.at[info_index,'Body (HTML)'] = description
                info_df.at[info_index,'Vendor'] = 'Yocaher'
              
                info_df.at[info_index,'Standardized Product Type'] = df['Standardized Product Type'][i]
                info_df.at[info_index,'Custom Product Type'] = df['Custom Product Type'][i]
                try:
                    sku = self.driver.find_element(By.CLASS_NAME,'productSKU').find_element(By.TAG_NAME,'dd').text
                except NoSuchElementException:
                    sku = ''
                try:
                    upc = self.driver.find_element(By.CLASS_NAME,'productUPC').find_element(By.TAG_NAME,'dd').text
                except NoSuchElementException:
                    upc = ''
                try:
                    size_list = self.driver.find_elements(By.CLASS_NAME,'form-option-variant')
                except NoSuchElementException:
                    size_list = []
                tag_sizes = ''
                for j in range(len(size_list)):
                    if tag_sizes == '':
                        tag_sizes = size_list[j].text
                    else:
                        tag_sizes += ", " + size_list[j].text
                tag_str = "Yocaher, Unisex, Adult, " + title
                if color != '':
                    tag_str += ", " + color
                tag_str += ", " + sku + ", " + upc
                if tag_sizes != "":
                    tag_str += ", " + tag_sizes
                try:
                    price = self.driver.find_element(By.CLASS_NAME,'productView-price').find_element(By.CLASS_NAME,'price--withoutTax').text[1:]
                except NoSuchElementException:
                    self.driver.get('https://dealer.yocaher.com/login.php')
                    self.driver.find_element(By.ID,'login_email').send_keys('mark@boardwest.com')
                    self.driver.find_element(By.ID,'login_pass').send_keys('Streetwise85373')
                    self.driver.find_element(By.CLASS_NAME,'form-actions').find_element(By.TAG_NAME,'input').click()
                    self.driver.get(link)
                    price = self.driver.find_element(By.CLASS_NAME,'productView-price').find_element(By.CLASS_NAME,'price--withoutTax').text[1:]
                tag_str += ", " + str(df['Custom Product Type'][i]) + ", $" + str(price) + ", $" + str(float(price) * 2)
                info_df.at[info_index,'Tags'] = tag_str 
                info_df.at[info_index,'Published'] = "TRUE"
                type_text = df['Standardized Product Type'][i]
                if df['Category'][i] == 'Complete Longboards':
                    info_df.at[info_index,'Option1 Name'] = "Color:"
                    info_df.at[info_index,'Option1 Value'] = Graphic
                    info_df.at[info_index,'Option2 Name'] = "Deck Size:"
                    info_df.at[info_index,'Option2 Value'] = deck_size
                    info_df.at[info_index,'Option3 Name'] = ""
                    info_df.at[info_index,'Option3 Value'] = ""
                elif df['Category'][i] == 'Rails':
                    info_df.at[info_index,'Option1 Name'] = "Color:"
                    info_df.at[info_index,'Option1 Value'] = color
                    info_df.at[info_index,'Option2 Name'] = "Length:"
                    info_df.at[info_index,'Option2 Value'] = length
                    info_df.at[info_index,'Option3 Name'] = ""
                    info_df.at[info_index,'Option3 Value'] = ""
                elif df['Category'][i] == 'Tools':
                    info_df.at[info_index,'Option1 Name'] = "Color:"
                    info_df.at[info_index,'Option1 Value'] = color
                    info_df.at[info_index,'Option2 Name'] = ""
                    info_df.at[info_index,'Option2 Value'] = ''
                    info_df.at[info_index,'Option3 Name'] = ""
                    info_df.at[info_index,'Option3 Value'] = ""
                elif df['Category'][i] == 'Griptape':
                    info_df.at[info_index,'Option1 Name'] = "Color:"
                    info_df.at[info_index,'Option1 Value'] = color
                    info_df.at[info_index,'Option2 Name'] = "Size:"
                    info_df.at[info_index,'Option2 Value'] = detail_size
                    info_df.at[info_index,'Option3 Name'] = ""
                    info_df.at[info_index,'Option3 Value'] = ""
                elif df['Category'][i] == 'Bearings':
                    info_df.at[info_index,'Option1 Name'] = "Color:"
                    info_df.at[info_index,'Option1 Value'] = color
                    info_df.at[info_index,'Option2 Name'] = "Speed:"
                    info_df.at[info_index,'Option2 Value'] = speed
                    info_df.at[info_index,'Option3 Name'] = ""
                    info_df.at[info_index,'Option3 Value'] = ""
                elif df['Category'][i] == 'Trucks':
                    info_df.at[info_index,'Option1 Name'] = "Color:"
                    info_df.at[info_index,'Option1 Value'] = color
                    info_df.at[info_index,'Option2 Name'] = "Size:"
                    info_df.at[info_index,'Option2 Value'] = hanger
                    info_df.at[info_index,'Option3 Name'] = ""
                    info_df.at[info_index,'Option3 Value'] = ""
                elif df['Category'][i] == 'Wheels':
                    info_df.at[info_index,'Option1 Name'] = "Color:"
                    info_df.at[info_index,'Option1 Value'] = color
                    info_df.at[info_index,'Option2 Name'] = "Size:"
                    info_df.at[info_index,'Option2 Value'] = detail_size
                    info_df.at[info_index,'Option3 Name'] = "Hardness:"
                    info_df.at[info_index,'Option3 Value'] = hardness
                else:
                    info_df.at[info_index,'Option1 Name'] = "Color:"
                    info_df.at[info_index,'Option1 Value'] = Graphic
                    info_df.at[info_index,'Option2 Name'] = "Deck Size:"
                    info_df.at[info_index,'Option2 Value'] = deck_size
                    info_df.at[info_index,'Option3 Name'] = ""
                    info_df.at[info_index,'Option3 Value'] = ""
                if len(size_list) == 0:
                    info_df.at[info_index,'Option4 Name'] = ""
                    info_df.at[info_index,'Option4 Value'] = ""
                else:
                    info_df.at[info_index,'Option4 Name'] = "Select a Size:"
                    info_df.at[info_index,'Option4 Value'] = size_list[0].text
                
                info_df.at[info_index,'Color'] = color
                info_df.at[info_index,'Variant SKU'] = sku
                info_df.at[info_index,'Variant Grams'] = df['WEIGHTS'][i]
                info_df.at[info_index,'Variant Inventory Tracker'] = 'shopify'
                info_df.at[info_index,'Variant Inventory Qty'] = ''
                info_df.at[info_index,'Variant Inventory Policy'] = 'deny'
                info_df.at[info_index,'Variant Fulfillment Service'] = 'manual'
                
                info_df.at[info_index,'Variant Price'] = "$" + str(float(price) * 2)
                info_df.at[info_index,'Variant Compare At Price'] = ''
                info_df.at[info_index,'Variant Requires Shipping'] = 'TRUE'
                info_df.at[info_index,'Variant Taxable'] = 'TRUE'
                info_df.at[info_index,'Variant Barcode'] = upc
                image_list = self.driver.find_elements(By.CLASS_NAME,'productView-thumbnail-link')
                if len(image_list) > 0:
                    info_df.at[info_index,'Image Src'] = image_list[0].get_attribute('href')
                    info_df.at[info_index,'Image Position'] = 1
                    info_df.at[info_index,'Image Alt Text'] = image_list[0].find_element(By.TAG_NAME,'img').get_attribute('alt')
                else:
                    info_df.at[info_index,'Image Src'] = ''
                    info_df.at[info_index,'Image Position'] = ''
                    info_df.at[info_index,'Image Alt Text'] = ''
                info_df.at[info_index,'Gift Card'] = 'FALSE'
                info_df.at[info_index,'SEO Title'] = title
                info_df.at[info_index,'SEO Description'] = seo_description
                info_df.at[info_index,'Google Shopping / Google Product Category'] = df['Standardized Product Type'][i]
                info_df.at[info_index,'Google Shopping / Gender'] = 'unisex'
                info_df.at[info_index,'Google Shopping / Age Group'] = 'Adult'
                info_df.at[info_index,'Google Shopping / MPN'] = ''
                info_df.at[info_index,'Google Shopping / AdWords Grouping'] = ''
                info_df.at[info_index,'Google Shopping / AdWords Labels'] = ''
                info_df.at[info_index,'Google Shopping / Condition'] = 'New'
                info_df.at[info_index,'Variant Image'] = ''
                info_df.at[info_index,'Variant Weight Unit'] = 'g'
                info_df.at[info_index,'Variant Tax Code'] = ''
                info_df.at[info_index,'Cost per item'] = "$" + price
                info_df.at[info_index,'Status'] = 'Active'
                info_df.to_csv("result.csv", index=False)
                
                info_index += 1
                if len(size_list)-1 > len(image_list)-1:
                    for j in range(len(size_list)-1):
                        if j < len(image_list)-1:
                            self.setValue(info_df, info_index, link.split('/')[-2], size_list[j+1].text,image_list[j+1].get_attribute('href'),j+2,image_list[j+1].find_element(By.TAG_NAME,'img').get_attribute('alt'))
                        else:
                            self.setValue(info_df, info_index, link.split('/')[-2], size_list[j+1].text,'','','')
                        info_index += 1
                else:
                    for j in range(len(image_list)-1):
                        if j < len(size_list)-1:
                            self.setValue(info_df, info_index, link.split('/')[-2], size_list[j+1].text,image_list[j+1].get_attribute('href'),j+2,image_list[j+1].find_element(By.TAG_NAME,'img').get_attribute('alt'))
                        else:
                            self.setValue(info_df, info_index, link.split('/')[-2], '',image_list[j+1].get_attribute('href'),j+2,image_list[j+1].find_element(By.TAG_NAME,'img').get_attribute('alt'))
                        info_index += 1
                # info_index += 1
    def setValue(self, info_df, info_index, handle, size_value, image_link, image_index, image_alt):
        info_df.at[info_index,'Handle'] = handle
        info_df.at[info_index,'Title'] = ''
        info_df.at[info_index,'Body (HTML)'] = ''
        info_df.at[info_index,'Vendor'] = ''
        info_df.at[info_index,'Standardized Product Type'] = ''
        info_df.at[info_index,'Custom Product Type'] = ''
        info_df.at[info_index,'Tags'] = ""
        info_df.at[info_index,'Published'] = ""
        info_df.at[info_index,'Option1 Name'] = ""
        info_df.at[info_index,'Option1 Value'] = ""
        info_df.at[info_index,'Option2 Name'] = ""
        info_df.at[info_index,'Option2 Value'] = ""
        info_df.at[info_index,'Option3 Name'] = ""
        info_df.at[info_index,'Option3 Value'] = ""
        info_df.at[info_index,'Option4 Name'] = ""
        info_df.at[info_index,'Option4 Value'] = size_value
        info_df.at[info_index,'Variant SKU'] = ""
        info_df.at[info_index,'Variant Grams'] = ""
        info_df.at[info_index,'Variant Inventory Tracker'] = ''
        info_df.at[info_index,'Variant Inventory Qty'] = ''
        info_df.at[info_index,'Variant Inventory Policy'] = ''
        info_df.at[info_index,'Variant Fulfillment Service'] = ''
        info_df.at[info_index,'Variant Price'] = ""
        info_df.at[info_index,'Variant Compare At Price'] = ''
        info_df.at[info_index,'Variant Requires Shipping'] = ''
        info_df.at[info_index,'Variant Taxable'] = ''
        info_df.at[info_index,'Variant Barcode'] = ''
        info_df.at[info_index,'Image Src'] = image_link
        info_df.at[info_index,'Image Position'] = image_index
        info_df.at[info_index,'Image Alt Text'] = image_alt
        info_df.at[info_index,'Gift Card'] = ''
        info_df.at[info_index,'SEO Title'] = ''
        info_df.at[info_index,'SEO Description'] = ''
        info_df.at[info_index,'Google Shopping / Google Product Category'] = ''
        info_df.at[info_index,'Google Shopping / Gender'] = ''
        info_df.at[info_index,'Google Shopping / Age Group'] = ''
        info_df.at[info_index,'Google Shopping / MPN'] = ''
        info_df.at[info_index,'Google Shopping / AdWords Grouping'] = ''
        info_df.at[info_index,'Google Shopping / AdWords Labels'] = ''
        info_df.at[info_index,'Google Shopping / Condition'] = ''
        info_df.at[info_index,'Variant Image'] = ''
        info_df.at[info_index,'Variant Weight Unit'] = ''
        info_df.at[info_index,'Variant Tax Code'] = ''
        info_df.at[info_index,'Cost per item'] = ""
        info_df.at[info_index,'Status'] = 'Active'
        info_df.to_csv("result.csv", index=False)
    def waiting(self, class_name):
        timeout = 6# timeout , change if connection slow
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.CLASS_NAME,class_name)))
        except TimeoutException:
            pass
if __name__ == "__main__":
    scrap = ScrapePlaces()
    # scrap.closeDriver()

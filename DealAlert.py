# this program will go through known & safe websites and check products
# next it will save the data in a database, so the price is known
# and if there's a good sale, alert me.

# maybe try to make a shopping list, and run it across multiple known stores and get the best deal

# add a few more websites... EG mahsanei hashmal, TMS , bug
# make an Alert vehicle, such as sending an email ,
# calculate the average price and if the latest price drops below it, send an email
# make a UI where it will be easy to insert alerts or delete alerts - either TKinter or frontend
# figure out how to enter URLs and save them easier
# bug & ERROR fixes


import json
import os



from winotify import Notification , audio

# libraries for scraping data
import sqlite3
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver import ChromeOptions

# other libraries...
import datetime



# sites where i scrape my data from
class Sites:
    @staticmethod
    # searches the price on an Ivory URL and returns it.
    # ID=cancelproduct, if exists site, has removed the product
    def IVORY(URL : str):
        if URL  == '' :
            return 'None'
        try :
            ivory = requests.get(URL)
        except :
            return 'None'
        HTML_site = ivory.text
        soup: BeautifulSoup = BeautifulSoup(HTML_site, 'html.parser')
        does_not_exist = soup.find('div',id ='cancelproduct')

        if does_not_exist :
            return 'Removed'
        else :
            ivory_price = soup.find_all('span', class_='print-actual-price')[0].string
        return ivory_price.replace(',','')

    # uses selenium because it's a JS heavy website... runs a bit slower than the other 2
    @staticmethod
    def KSP(URL : str):
        options = ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        driver = webdriver.Chrome(options=options)
        driver.get(URL)
        driver.implicitly_wait(5)
        try :
            text_box = driver.find_element(By.ID, value='product-page-root').text
            text_box = list(text_box.split())
        except :
            print('Page not found...')
            return 'DNE'


        for i, k in enumerate(text_box):
            if k == 'או':
                if '₪' in text_box[i - 1]:
                    return text_box[i - 1].replace('₪', '')

    #  סופר-פארם
    @staticmethod
    def SUPERPHARM(URL: str):
        if URL == '':
            return 'None'
        try :
            r = requests.get(URL)
        except : 
            return 'None'
        html_text = r.text
        soup = BeautifulSoup(html_text, 'html.parser')
        soup = soup.find('span', class_='price-container').text.split()
        return soup[-1]

    # מחסני-חשמל
    @staticmethod
    def Electric_Storage(URL : str):
        if URL == ''  :
            return 'None'
        try :
            r = requests.get(URL)
        except :
            return 'None'
        HTML_text = r.text
        soup = BeautifulSoup(HTML_text , 'html.parser')
        price = soup.find('span', class_= 'price').text
        print(price.replace('₪',''))



#starts the process 
def search(products : list ):
    connection = sqlite3.connect("Products.db")
    cursor = connection.cursor()
    time = str(datetime.datetime.now()).split(' ')[1].split('.')[0]
    date = str(datetime.datetime.now()).split(' ')[0]
    for product in products :
        name = product['Name'].replace(' ','_')
        print(f'\nSearching for : {name.replace('_',' ')}')
        print('Scraping KSP...')
        ksp = Sites.KSP(product['ksp'])
        if ksp != None :
        
            ksp = Sites.KSP(product['ksp']).replace(',','')
        else :
            ksp = 'None'
        print('Scraping Ivory...')

        # does not exist

        ivory = Sites.IVORY(product['ivory'])
        print('Scraping Super-Pharm')
        super_pharm = Sites.SUPERPHARM(product['super-pharm'])
        print('Scraping MH')
        mh = Sites.Electric_Storage(product['MH'])

        values = (date, time, ivory, ksp,super_pharm,mh)


        try:
            cursor.execute(f'CREATE TABLE {name} (date, time , IVORY , KSP, SUPERPHARM,MH)')
            sql = f'INSERT INTO {name} (date,time, IVORY, KSP, SUPERPHARM,MH) Values (?,?,?,?,?,?)'
            cursor.execute(sql, values)
        except:
            last_entry = list(cursor.execute(f'select * from {name} order by rowid desc LIMIT 1'))[0]
            last_ivory = last_entry[2]
            last_ksp = last_entry[3]
            last_super_pharm = last_entry[4]
            last_mh = last_entry[5]

            new_lowest_price = min(filter(lambda a : int(a) if a.isdigit() else False,[ksp,ivory,super_pharm,mh]))
            old_lowest_price = min(filter(lambda a : int(a) if a.isdigit() else False, [last_ivory,last_ksp,last_super_pharm,last_mh]))
            
            sites = [ivory,ksp,super_pharm,mh].index(str(new_lowest_price))
            site = {0 : 'ivory' , 1 : 'ksp' , 2 : 'super-pharm' , 3 : 'MH'}

            
            if int(old_lowest_price) > int(new_lowest_price) :
                toast = Notification(app_id='DealAlert',
                     title = f'{name.replace('_',' ')} New Low by {site[sites]}',
                     msg = f'New low of : {new_lowest_price}\n',
                     duration ='long',
                     )
                toast.set_audio(audio.Default, loop = False)
                toast.add_actions(label = 'go-to site' , launch = product[site[sites]])
                toast.show()
            
            



            sql = f'INSERT INTO {name} (date,time, IVORY, KSP, SUPERPHARM,MH) Values (?,?,?,?,?,?)'
            cursor.execute(sql, values)


    connection.commit()
    print('Done.')

# product class, designed to add an item & it's corresponding links
class Product :
    def __init__(self ,name : str, ksp = None, ivory = None, super_pharm = None, mh = None):
        self.name = name
        self.ksp = ksp
        self.ivory = ivory
        self.super_pharm = super_pharm
        self.mh = mh


    def CreateDict(self):
        return {f'Name' : f'{self.name.replace(' ','_')}',
                f'ksp' : f'{self.ksp}',
                f'ivory' : f'{self.ivory}',
                f'super-pharm' : f'{self.super_pharm}',
                f'MH' : f'{self.mh}'
                }






# Products to scrape
f = open('products.json')
data = json.load(f)

products = []

for i in data['products']:
    products.append(i)



if __name__ == '__main__' :
    search(products)


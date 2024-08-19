from selenium import webdriver
from bs4 import BeautifulSoup as bp
import csv
driver=webdriver.Chrome()

def get_hotel_price(bs):
    price_element=bs.find('div', class_ = "css-901oao r-t1w4ow r-adyw6z r-b88u0q r-135wba7 r-1ff274t")
    if price_element:
        true_price = price_element.text.strip().replace('VND', '').replace('.', '')
        return float(true_price)
    return None 
def extract_hotels_url(url,i):
    info={}
    print(f"scraping URL number: {i}")
    driver.get(url)
    driver.implicitly_wait(10)
    bs=bp(driver.page_source,'lxml')
    info['id']=i
    info['price']=get_hotel_price(bs)
    return info

if __name__ =="__main__":
    data=[]
    with open('hotels.csv',newline='',encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        i=0
        for row in reader:
            url=row[0]
            file_name = "price.txt"
            data.append(extract_hotels_url(url,i))
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(str(data))
            file.close()


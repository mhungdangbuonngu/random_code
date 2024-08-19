import requests
from bs4 import BeautifulSoup as bp
import csv
from datetime import datetime
import time
from selenium import webdriver


USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
REQUEST_HEADER = {
    'User-Agent': USER_AGENT,
    'Accept-language': 'en-US, en;q=0.5',
}
def get_page_html(url):
    res= requests.get(url=url,headers= REQUEST_HEADER)
    return res.text


def get_hotel_price(soup):
    price_element=soup.find('div', attrs={'style':'color: rgb(255, 94, 31); font-size: 20px;'})
    if price_element:
        true_price = price_element.text.strip().replace('VND', '').replace('.', '')
        return float(true_price)
    return None    
            
def get_hotel_name(soup):
    name=soup.find('div',class_='css-901oao r-a5wbuh r-1enofrn r-b88u0q r-1cwl3u0 r-fdjqy7 r-3s2u2q')
    return name.text.strip() if name else None


def get_hotel_rating(soup):
    rating=soup.find('div',class_ = 'css-901oao r-jwli3a r-a5wbuh r-s67bdx r-b88u0q r-10cxs7j r-q4m81j')
    return rating.text.strip() if rating else None


def get_hotel_des(soup):
    des=soup.find('div',attrs={'style':'font-family:Godwit, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Arial, sans-serif, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol;font-size:14px;line-height:20px;max-height:80px;overflow:hidden'})
    return des.text.strip().replace('\n','') if des else None

def get_hotel_location(soup):
    location=soup.find('div',class_='css-901oao css-cens5h r-13awgt0 r-a5wbuh r-1b43r93 r-majxgm r-rjixqe r-fdjqy7')
    return location.text.strip().replace('\t','') if location else None

def get_hotel_comments(soup):
    comments=[]
    a = soup.findAll('div',class_='css-901oao css-cens5h r-cwxd7f r-a5wbuh r-1b43r93 r-majxgm r-rjixqe r-fdjqy7')
    for comment in a:
        comments.append(comment.text.strip())
    return comments
def get_hotel_img_url(soup):
    div=soup.find('div', class_='css-1dbjc4n r-j9b53g r-1i97xy8 r-1ta3fxp r-18u37iz r-1z0tv5g r-1udh08x')
    img_tag=div.findAll('img')
    img_url=[img['src'] for img in img_tag]

    return img_url
    

def extract_hotels_url(url,i):
    info={}
    print(f"scraping URL number: {i}")
    html = get_page_html(url=url)
    soup=bp(html,'lxml')
    info['id']=i
    info['name'] = get_hotel_name(soup)
    info['price']=get_hotel_price(soup)
    info['rating']=get_hotel_rating(soup)
    info['location'] = get_hotel_location(soup)
    info['description']=get_hotel_des(soup)
    info['comments']=get_hotel_comments(soup)
    info['image_url']=get_hotel_img_url(soup)
    return info


if __name__ =="__main__":
    data=[]
    with open('hotels.csv',newline='',encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        i=0
        for row in reader:
            url=row[0]
            file_name = "hotels.txt"
            data.append(extract_hotels_url(url,i))
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(str(data))
            i+=1
            time.sleep(0.25)
    
    
        
    
    
            
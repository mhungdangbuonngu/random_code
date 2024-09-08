import requests
from bs4 import BeautifulSoup as bp
import csv
import time
base_url='https://www.traveloka.com'

USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
headers = {
    'User-Agent': USER_AGENT,
    'Accept-Language': 'vi-vn'  # Đặt ngôn ngữ mặc định là tiếng Việt
}

for x in range(1,138):
    r=requests.get(f'https://www.traveloka.com/vi-vn/hotel/vietnam/region/hanoi-10009843/{x}',headers=headers)
    soup=bp(r.content,'lxml')

    hotel_list=soup.find_all('div',class_='css-1dbjc4n r-14lw9ot r-awg2lu r-1dzdj1l r-rs99b7 r-18u37iz r-1jbys1g r-1udh08x')
    hotel_urls=[]
    for hotel in hotel_list:
        link=hotel.find('a',href=True)
        hotel_urls.append(base_url+link['href'])
    with open(f'hotel_urls_{x}.csv',mode='w',newline='') as file:
        writer = csv.writer(file)
        for url in hotel_urls:
            writer.writerow([url])
    time.sleep(0.5)
    if (x % 10 == 0):
        time.sleep(30)


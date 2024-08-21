import requests
from bs4 import BeautifulSoup as bp
import csv
import time

USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
REQUEST_HEADER = {
    'User-Agent': USER_AGENT,
    'Accept-language': 'en-US, en;q=0.5',
}

def get_page_html(url):
    res= requests.get(url=url,headers= REQUEST_HEADER)
    return res.text
def get_tour(soup):
    print(f"scraping URL number:")
    html = get_page_html(url=url)
    soup=bp(html,'lxml')
    return soup
if __name__ == '__main__':
    url='https://www.tripadvisor.com.vn/Attraction_Review-g293924-d311083-Reviews-Temple_of_Literature_National_University-Hanoi.html'
    file_name='play_html.txt'
    data= get_tour(url)
    with open(file_name, 'w', encoding='utf-8') as file:
                file.write(str(data))
    
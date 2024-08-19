import requests
from bs4 import BeautifulSoup as bp

url='https://www.traveloka.com/vi-vn/hotel/detail?spec=17-08-2024.18-08-2024.1.1.HOTEL.9000001039894.22land%20Residence%20Hotel%2071%20Hang%20Bong.2&contexts=%7B%22inventoryRateKey%22%3A%22povEwB3ZzsU2C6pd%2B6MdU13LUNuufACdbU0usK5vg0dM0tKsNUio4Rxug1zOzHJilcvZa8YdqqIySdppe7dolTIewZlxfjiOGz6oXLTucMvN0%2BgQ3yZPvZcoHwUFNN%2BZpcr%2F%2FNa8o9ElfN8zOYhzzZeg0X586laFpeUViPi9rxC3Dyxw1TnOeHp0wBwofecLmhLDdV0WLeT%2FFKfQ0QL8LH02Dvlx%2F8PjYogEE5yzx6g6yOKyKeIDf7jO3GM45O1o1hmSkmz3HiZNSbS8gXb3CDW9nmlhkqLKa4lLkAkZpAH0gcTfW1b8h02Mkay%2BiC4I1LU%2FuFfn%2F4XqAhG74D2hKmS6bi7h%2Fw2IxaeAsuP0oBqC0I%2B4MpT6AtjonGvWhSFYeOjRTl6ytxGba%2F42pjcyydEESW7Hq%2F%2BXk7KJE212dw5uzCQvj3U9tQgF0HznDB7SYn%2Bxx0tb9%2BpxAg0Ppk3eA%2FmzREQ0KgV1vvYuRfaKd1eNmO0SRV1ogUSH81Kgs05BsmVHb%2FDz2eMMIR3KhBjDXyMn1qdaM1viWqCGwU1siX1ZIegdsZIo1sjlWnbsTcjefS6Pj3RtIU6lROCEB6QAgiS1WJabPNVEO7waQAXksTDyQHUY2wqyAfRzb44KOjG0H%2Fyaj8MBIo5YyvEVTpdvVDyhX%2Fvi4PswzgC5JhUlHZrcYsqJ2%2Fap3SGpbJdQ22ng3q%2Bfqt4KSNCPNxIlJ8xQoLeekG4C3Wfzu3vEJ07kKAzDDZvHNY9JJ5O%2F0vjIhtS03gvQKas1MNMJB%2BYT4sQNKOedxo73ys83rbc%2BDYNwLiL7soYssR%2FlubZFfGuV8p%2F7Uyrcx0JbbnOhcrDvcXJI6g%3D%3D%22%7D&loginPromo=1&prevSearchId=1807515394908379958'
USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
REQUEST_HEADER = {
    'User-Agent': USER_AGENT,
    'Accept-language': 'en-US, en;q=0.5',
}
def get_html(url):
    try:
        # Gửi yêu cầu GET tới trang web
        response = requests.get(url, headers=REQUEST_HEADER)
        
        # Kiểm tra nếu yêu cầu thành công (mã trạng thái 200)
        if response.status_code == 200:
            # Trả về nội dung HTML của trang
            return response.text
        else:
            # In thông báo lỗi nếu yêu cầu không thành công
            print(f"Lỗi: Không thể lấy HTML từ {url}, Mã trạng thái: {response.status_code}")
            return None
    except Exception as e:
        print(f"Đã xảy ra lỗi khi gửi yêu cầu: {e}")
        return None
page_url=get_html(url)
soup=bp(page_url,'html.parser')
price=soup.find('div', class_='css-1dbjc4n r-1w6e6rj r-1rxb9bi')
print(price)
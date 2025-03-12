import time
import requests
import csv
import sys
from bs4 import BeautifulSoup

import datetime


def get_resource(url):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
               "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    return requests.get(url, headers=headers)

def parse_html(r):
    if r.status_code == requests.codes.ok:
        r.encoding = "utf8"
        soup = BeautifulSoup(r.text, "lxml")
    else:
        print("HTTP request error..." + url)
        soup = None

    return soup

def save_to_csv(items, file):
    with open(file, 'w+', newline='', encoding='utf-8') as fp:
        writer = csv.writer(fp)
        for item in items:
            writer.writerow(item)

def web_scraping_bot(url):
    book = []
    soup = parse_html(get_resource(url))
    if soup != None:
        # print(soup)
        try:
            book_url = url
            str = soup.find('section', {'class':"col left auw-2"})
    
            title = str.find('h1').text.strip()
            author = str.find('a', {'class': "txt-ora1"}).text.strip()
            publisher = str.find_next('a', {'class': "txt-ora1"}).find_next('a', {'class': "txt-ora1"}).text.strip()    
            publish_date = str.find('span', {'class': "txt-bk1"}).text.strip()
            list_price = str.find('span', {'class': "txt-bk1 tdlt"}).text.strip()
            bargain_price = str.find_all('span', {'class': "txt-bk1"})[2].text.strip()
            member_price = str.find_all('span', {'class': "txt-bk1"})[3].text.strip()

            str2 = soup.find('section', {'class': "cntModBd-block cntModBd-book_basicInf-block"})

            category = str2.find_all('li')[0].text.split('：')[1]
            isbn = str2.find_all('li')[5].text.split('ISBN：')[1]
            series_num = str2.find_all('li')[6].text.split('：')[1]
            spec = str2.find_all('li')[7].text.split('：')[1]

            book.append(title)
            book.append(author)
            book.append(publisher)
            book.append(publish_date)
            book.append(list_price)
            book.append(bargain_price)
            book.append(member_price)
            book.append(category)
            book.append(isbn)
            book.append(series_num)
            book.append(spec)
            book.append(book_url)

        except Exception as e: 
            print("Book not found: {}".format(e))

    return book


if __name__ == '__main__':
    # url = generate_search_url(url, "演算法")

    if len(sys.argv) >= 3:
        fromid = int(sys.argv[1])
        toid = int(sys.argv[2])
    else:
        fromid = 700
        toid = 720

    master_list = [['書名','作者','出版社','出版日期','定價','優惠價','會員價','分類','ISBN','商城書號','規格','網址']]

    for id in range(fromid, toid):
        url = f'https://www.ipci.com.tw/books_in.php?book_id={id}'
       
        ts = time.time()
        currtime = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        print (f'[{currtime}] Get data from {url}')

        book_list = web_scraping_bot(url)
        # for item in book_list:
            # print(item)

        if book_list != []:
            master_list.append(book_list)

        print("Wait 5 sec...")
        time.sleep(5) 


    ts = time.time()
    timestr = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d-%H%M%S')

    fname = f'ipci-list-{timestr}.csv'
    save_to_csv(master_list, fname)

    currtime = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    print (f'[{currtime}] CSV file {fname} saved')



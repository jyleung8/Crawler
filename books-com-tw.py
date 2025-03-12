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

def get_ISBN(url):
    soup = parse_html(get_resource("http:" + url))
    if soup != None:
        try:
           isbn = soup.find(itemprop="productID")["content"][5:]
        except:
           isbn = "0000"
    else:
        isbn = "1111"
    return isbn

def save_to_csv(items, file):
    with open(file, 'w+', newline='') as fp:
        writer = csv.writer(fp)
        for item in items:
            writer.writerow(item)

def web_scraping_bot(url):
    booklist = [["書名","作者","網址","書價"]]
    print("Getting data...")
    soup = parse_html(get_resource(url))
    if soup != None:
        # print(soup)
        tag_item = soup.find_all('div', {'class': 'table-td'})
        for item in tag_item:
            book = []

            try:
                title = item.find('h4').find('a')['title']
                author = item.find('p',{'class':'author'}).find('a').text
        
                # isbn = item.find(itemprop="productID")["content"][5:]
                bookurl = 'https:' + item.find('h4').find('a')['href']
                pricestr = item.find('ul').find('li').find_all('b')
                if len(pricestr) == 1:
                     price = pricestr[0].string
                else:
                     price = pricestr[1].string

                book.append(title)
                book.append(author)
                book.append(bookurl)
                book.append(price)
                booklist.append(book)

                print("Wait 5 sec...")
                time.sleep(5) 

            except Exception as e: 
                print("Book not found: {}".format(e))

    return booklist


if __name__ == '__main__':
    # url = generate_search_url(url, "演算法")

    if len(sys.argv) >= 2:
        keyword = sys.argv[1]
    else:
        keyword = '寰宇出版'

    url = f'http://search.books.com.tw/search/query/key/{keyword}/cat/all'

    ts = time.time()
    currtime = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    print (f'[{currtime}] Get data from {url}')

    booklist = web_scraping_bot(url)
    # for item in booklist:
        # print(item)

    ts = time.time()
    timestr = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d-%H%M%S')

    fname = f'books-com-tw-{keyword}-{timestr}.csv'
    save_to_csv(booklist, fname)

    currtime = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    print (f'[{currtime}] CSV file {fname} saved')


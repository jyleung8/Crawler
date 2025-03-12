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
        writer = csv.writer(fp, quoting=csv.QUOTE_ALL)
        for item in items:
            writer.writerow(item)

def web_scraping_bot(url, booklist):
    # booklist = []
    soup = parse_html(get_resource(url))
    if soup != None:
        # print(soup)
        try:
            tag_item = soup.find_all('div', {'class':"recordHighlight"})
            for item in tag_item:
                # title = item.find('a', {'class':'title'})
                publisher = item.find_all('span', {'dir':'ltr'})[0].text.strip()
                searchnum = item.find_all('span', {'dir':'ltr'})[1].text.strip()
                title = item.find_all('a', {'dir':'ltr'})[0].text.strip()
                author = item.find_all('a', {'dir':'ltr'})[1].text.strip()
                if len(item.find_all('a', {'dir':'ltr'})) > 2:
                    series = item.find_all('a', {'dir':'ltr'})[2].text.strip()
                else:
                    series = ''
                bookurl = 'https://webcat.hkpl.gov.hk' + item.find('a', {'class':'title'}).get('href')[2:]

                book = [title, author, publisher, searchnum, series, bookurl]
                # book.append(category)
                # book.append(isbn)

                booklist.append(book)
  
        except Exception as e: 
            print("Book not found: {}".format(e))

    return booklist


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        keyword = sys.argv[1]
    else:
        keyword = '寰宇出版'

    frompg = 1
    topg = 13

    master_list = [['書名','作者','出版社','索書號','系列名稱','網址']]
    book_list = [['書名','作者','出版社','索書號','系列名稱','網址']]

    for pg in range(frompg, topg):
        # url = f'https://webcat.hkpl.gov.hk/search/query?term_1={keyword}&theme=WEB'

        url = f'https://webcat.hkpl.gov.hk/search/query?match_1=MUST&field_1&term_1={keyword}&sort=relevance&pageNumber={pg}&theme=WEB'
       
        ts = time.time()
        currtime = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        print (f'[{currtime}] Get data from {url}')

        book_list = web_scraping_bot(url, book_list)
        # for item in book_list:
            # print(item)

        # if book_list != []:
        #    master_list.append(book_list)

        print("Wait 5 sec...")
        time.sleep(5) 


    master_list = book_list

    ts = time.time()
    timestr = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d-%H%M%S')

    fname = f'hkpl-{keyword}-{timestr}.csv'
    save_to_csv(master_list, fname)

    currtime = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    print (f'[{currtime}] CSV file {fname} saved')



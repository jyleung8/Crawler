import requests
from bs4 import BeautifulSoup
import pandas as pd

import time
import datetime
import csv
import sys


headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"}


def save_to_csv(items, file):
    with open(file, 'w+', newline='', encoding='utf-8') as fp:
        writer = csv.writer(fp, quoting=csv.QUOTE_ALL)
        for item in items:
            writer.writerow(item)


def get_yahoo_news(stock):
    data = requests.get(f'https://tw.stock.yahoo.com/quote/{stock}/news', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    all_news = soup.find_all("h3", {"class": "Mt(0) Mb(8px)"})

    all_news_store = []
    for a in all_news:
        news_path = a.find('a')['href']
        if news_path[-4:] == "html":
            all_news_store.append(news_path)

    count = 0
    date_store, title_store, body_store = [], [], []
    rows = []
    for new in all_news_store:
        each_data = requests.get(f'{new}', headers=headers)
        each_soup = BeautifulSoup(each_data.text, 'html.parser')
        title = each_soup.find("h1", {"data-test-locator": "headline"}).text
        body = each_soup.find("div", {"class": "caas-body"}).text
        news_time = each_soup.find("div", {"class": "caas-attr-time-style"}).text
        # news_time = news_time.split(" ")[0]
        news_time = news_time.replace("年", "-")
        news_time = news_time.replace("月", "-")
        news_time = news_time.replace("日", "")
        news_time = news_time.replace("上午", "am ")
        news_time = news_time.replace("下午", "pm ")

        news_timestamp = datetime.datetime.strptime(news_time, '%Y-%m-%d %p %I:%M')
        news_timestr = datetime.datetime.strftime(news_timestamp, '%Y-%m-%d %H:%M:%S')

        title_store.append(title)
        body_store.append(body)
        date_store.append(news_time)

        rows.append([stock, news_timestr, title, body, new])
        count += 1
        # currtime = datetime.datetime.now().strftime('%H:%M:%S')
        # print (f'[{currtime}] Getting {count} news')

    result = pd.DataFrame()
    result['title'] = title_store
    result['url'] = all_news_store
    result['date'] = date_store

    #result2 = [[title_store, all_news_store, date_store] for t in title_store]

    return rows


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        stock = sys.argv[1]
    else:
        stock = '2330'

    sstr = get_yahoo_news(stock)

    ts = time.time()
    timestr = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d-%H%M%S')

    fname = f'yahoo-news-{stock}-{timestr}.csv'
    save_to_csv(sstr, fname)

    currtime = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    print (f'[{currtime}] CSV file {fname} saved')


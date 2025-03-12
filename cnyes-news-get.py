import sys
import csv
import json
import requests
import pandas as pd

import time
import datetime
from bs4 import BeautifulSoup


def save_to_csv(items, file):
    with open(file, 'w+', newline='', encoding='utf-8') as fp:
        writer = csv.writer(fp, quoting=csv.QUOTE_ALL)
        for item in items:
            writer.writerow(item)


def stock_news(stock_name = '大盤'):
  if stock_name == '大盤':
    stock_name = '台股'

  stock_name = stock_name + ' -盤中速報'

  data = []
  json_data = requests.get(f'https://ess.api.cnyes.com/ess/api/v1/news/keyword?q={stock_name}&limit=5&page=1').json()

  items = json_data['data']['items']
  for item in items:
      news_id = item["newsId"]
      title = item["title"]
      publish_at = item["publishAt"]
      utc_time = datetime.datetime.utcfromtimestamp(publish_at)
      formatted_date = utc_time.strftime('%Y-%m-%d')
      url = requests.get(f'https://news.cnyes.com/news/id/{news_id}').content
      soup = BeautifulSoup(url, 'html.parser')
      p_elements = soup.find_all('p')
      p=''
      for paragraph in p_elements[4:]:
          p += paragraph.get_text()
      data.append([stock_name, formatted_date, title, p])

  return data


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        keyword = sys.argv[1]
    else:
        keyword = '台積電'

    sstr = stock_news(keyword)

    ts = time.time()
    timestr = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d-%H%M%S')

    fname = f'cnyes-{keyword}-{timestr}.csv'
    save_to_csv(sstr, fname)

    currtime = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    print (f'[{currtime}] CSV file {fname} saved')



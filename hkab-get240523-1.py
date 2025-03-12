import requests
from bs4 import BeautifulSoup
import sys
import csv
import json
import time
import datetime
import pandas as pd


# 'Overnight': 0.09929, '1 Week': 0.12143, '2 Weeks': 0.20071, '1 Month': 0.30214, '2 Months': 0.37071, '3 Months': 0.40143, '4 Months': 0.4225, '5 Months': 0.4625, '6 Months': 0.55179, '7 Months': 0.5625, '8 Months': 0.56929, '9 Months': 0.57821, '10 Months': 0.65893, '11 Months': 0.74607, '12 Months': 0.83536, 'year': 2012, 'month': 3, 'day': 2, 'date': '2012-3-2', 'time': '11:15am', 'isHoliday': False,
# url = 'https://www.hkab.org.hk/api/hibor?year=2012&month=3&day=2'

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

columns = ['Date', 'Overnight', '1 Week', '2 Weeks', '1 Month', '2 Months', '3 Months', '4 Months', '5 Months', '6 Months', '7 Months', '8 Months', '9 Months', '10 Months', '11 Months', '12 Months']


y1 = int(sys.argv[1])
y2 = int(sys.argv[2]) + 1

row = []
# for y in range(2012, 2025):

for y in range(y1, y2):
    for m in range(1, 13):
        currtime = datetime.datetime.now().strftime('%H:%M:%S')
        print (f'[{currtime}] Getting data of {y}-{m}')

        for d in range(1, 32):
            url = f'https://www.hkab.org.hk/api/hibor?year={y}&month={m}&day={d}'

            r = requests.get(url, headers=headers)
            if r.status_code == requests.codes.ok:
                # r.encoding = 'big5hkscs'
                soup = BeautifulSoup(r.text, 'lxml')
                data = json.loads(soup.text)

                if data['isHoliday'] == False and data['Overnight'] is not None:
                    col = []
                    col = [data['date']]
                    for i in range(0, 15):
                        if (list(data.values())[i] == None):
                            col.append(float(0.0))
                        else:
                            col.append(float(list(data.values())[i]))

                    # row.append(data['Overnight'], data['1 Week'], data['2 Weeks'], data['1 Month'], data['2 Months'], data['3 Months'], data['4 Months'], data['5 Months'], data['6 Months'], data['7 Months'], data['8 Months'], data['9 Months'], data['10 Months'], '11 Months', '12 Months', 'year', 'month', 'day', 'date', 'time', 'isHoliday'
                    row.append(col)

            time.sleep(8)


tnow = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
fname = f'hkab-hibor-{tnow}.csv'
currtime = datetime.datetime.now().strftime('%H:%M:%S')
print (f'[{currtime}] Saving csv file to {fname}')

df = pd.DataFrame(row, columns=columns)
df = df.set_index('Date')
df.index = pd.to_datetime(df.index)
df.to_csv(fname)

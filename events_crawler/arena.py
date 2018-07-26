# -*- coding: utf-8 -*-
import time
from bs4 import BeautifulSoup
from backports import csv
import io
from datetime import datetime
import requests


def getInfo(url):
    data = []
    res2 = requests.get(url)
    soup2 = BeautifulSoup(res2.text)
    
    print(soup2.select('.cp')[0].select('span')[0].text) # show name
    data.append(soup2.select('.cp')[0].select('span')[0].text)
    
    # show date
    text = ''
    for p in soup2.select('.cp')[0].select('p'):
        if p.text.find(u'日期') != -1:
            text = p.text
            break
    if text == '':
        return []

    #posDate = text.find(u'活動日期')
    posEnterTime = text.find(u'進場時間')
    posStartTime = text.find(u'開演時間')
    
    
    if posEnterTime == -1 and posStartTime == -1:
        posLocation = text.find(u'活動地點')
        print(text[6:posLocation])
        data.append(text[6:posLocation])
    elif posEnterTime == -1 and posStartTime != -1:
        posEnd = text.find(u'結束時間')
        print(text[6:posStartTime])
        print(text[posStartTime+6:posEnd])
        data.append(text[6:posStartTime])
        data.append(text[posStartTime+6:posEnd])
    else:
        print(text[6:posEnterTime])
        print(text[posEnterTime+6:posStartTime])
        data.append(text[6:posEnterTime])
        data.append(text[posEnterTime+6:posStartTime])
    
    return data
    


dataList = []
res = requests.get('http://www.arena.taipei/lp.asp?ctNode=62914&CtUnit=31718&BaseDSD=7&mp=12203a')
soup = BeautifulSoup(res.text)
numData = soup.select('.page')[0].select('em')[0].text
#numData = 20

res = requests.get('http://www.arena.taipei/lp.asp?ctNode=62914&CtUnit=31718&BaseDSD=7&mp=12203a' + '&pagesize=' + str(numData))
soup = BeautifulSoup(res.text)

aRows = soup.select('.list')[0].select('a')
for aRow in aRows[2:50]:
    dataList.append(getInfo('http://www.arena.taipei/' + aRow['href']))

    
# write file
time = str(datetime.now())
filename = '/Users/biceneutron/Python/crawler/arena/data/' + time + '.csv'
with io.open(filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(dataList)
    f.close()



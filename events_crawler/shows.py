# -*- coding: utf-8 -*-
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from backports import csv
import io
from datetime import datetime
import requests

def scrollDown(times):
    for i in range(times + 1):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(5)

def getInfo(url):
    url = 'https://www.indievox.com' + url
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}
    pageSource2 = requests.get(url, headers=headers)

    soup = BeautifulSoup(pageSource2.text, 'html.parser')
    info = ''
    rows = soup.select('.event-data')[0].select('tr')
    for row in rows:
        rowTh = row.select('th')
        #print('hi')
        if len(rowTh) != 0 and unicode(rowTh[0].text.strip()) == u'時間':
            info = info + row.select('td')[0].text.strip()
        elif len(rowTh) != 0 and unicode(rowTh[0].text.strip()) == u'場館':
            info = info + '||' + row.select('td')[0].text.strip()
        elif len(rowTh) != 0 and unicode(rowTh[0].text.strip()) == u'地址':
            info = info + '||' + row.select('td')[0].text.strip()
        
    return info
        

driver = webdriver.PhantomJS(executable_path=r'/Users/biceneutron/Desktop/phantomjs-2.1.1-macosx/bin/phantomjs')  # PhantomJs
driver.get('https://www.indievox.com/event/') # send GET request to web server

scrollDown(6) # scroll down
pageSource = driver.page_source # get web page source code
driver.close()

soup = BeautifulSoup(pageSource, 'html.parser') # wrap in BeautifulSoup

# parse
dataList = []
show = []
rows = soup.select('tr')
for row in rows:
    rowH5 = row.select('h5')
    rowP = row.select('p')
    if len(rowP) != 0:
        tagA = rowH5[0].a
        show = (rowH5[0].text.strip() + '||' + getInfo(tagA['href'])).split('||')
        dataList.append(show)
        print('One data done')
    

# write file
time = str(datetime.now())
filename = '/Users/biceneutron/Python/crawler/ticket/data/' + time + '.csv'
with io.open(filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(dataList)
    f.close()





#print(pageSource)


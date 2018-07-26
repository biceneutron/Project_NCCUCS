# -*- coding: utf-8 -*-
from __future__ import print_function
from  selenium import webdriver
from bs4 import BeautifulSoup
from backports import csv
import io
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import logging
logging.basicConfig()

def job():
    # print console info
    global num
    print(str(num) + ': ' + 'In function at ' + str(datetime.now()))

    while True:
        driver = webdriver.PhantomJS(executable_path=r'/Users/biceneutron/Desktop/phantomjs-2.1.1-macosx/bin/phantomjs')  # PhantomJs
        driver.get('http://www.cwb.gov.tw/V7/observe/real/46692.htm') # send GET request to web server
        pageSource = driver.page_source # get web page source code
        driver.close()

        soup = BeautifulSoup(pageSource, 'html.parser')

        dataList = []
        rows = soup.select('tr')
        count = 0

        # parse source code
        for row in rows:
            if count == 5: # dealing with title
                titles = row.select('th')
                dataList.append([title.text for title in titles])
            elif count > 5 and count < 156: # dealing with data
                dataList.append([row.select('th')[0].text] + [td.text for td in row.select('td')])
            count += 1

        # write data into file
        time = str(datetime.now())
        filename = '/Users/biceneutron/Desktop/dataTest/' + time + '.csv'
        with io.open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(dataList)
            f.close()

        if os.path.getsize(filename) < 5: # if the file size < 5 Bytes
            print('File size: ' + str(os.path.getsize(filename)) + ', is be deleted')
            print('Recrawling data...')
            os.remove(filename)
            continue
        else:
            break


    # print console info
    print(str(num) + ': ' + 'Out function at ' + str(datetime.now()))
    num += 1


num = 1
scheduler = BlockingScheduler()
scheduler.add_job(job, 'interval', minutes=1)
scheduler.start()



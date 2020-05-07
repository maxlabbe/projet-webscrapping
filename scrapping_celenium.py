# -*- coding: utf-8 -*-
"""
Created on Fri May  1 20:21:43 2020

@author: Max
"""

import time
import datetime
from selenium import webdriver
import pandas as pd

driver = webdriver.Firefox()
driver.get("https://trade.kraken.com/fr-fr/charts/KRAKEN:BTC-USD?period=1m%22")

market_values = []
time_values = []

for i in range(10):
    time.sleep(1)
    a_element = driver.find_element_by_css_selector('a[title="Kraken BTC/USD"]')
    market_values.append(float(a_element.find_element_by_class_name("price").text))
    day = str(datetime.date.today())
    hour = str(time.localtime().tm_hour)
    minute = str(time.localtime().tm_min)
    second = str(time.localtime().tm_sec)
    current_time = str(day + " " + hour + ':' + minute + ':' + second)
    time_values.append(current_time)
    df = pd.DataFrame({'market value': market_values, 'time': time_values})
    date = str(datetime.date.today())
    csv_name = date + '.csv'
    df.to_csv(csv_name)






# partie html :
"""
<a class="_3ywBVpN9pWrbtn3OTg0-ka br-weak" href="/markets/kraken/btc/usd" title="Kraken BTC/USD">
    <i class="crypton exc-default-s exc-kraken-s mr-4"></i>
    <div class="pr-3 uppercase">btc/usd</div>
    <div>
        <span class="price">8777.90</span><span class="ml-3">
        <span class="color-long">+1.66%</span></span>
    </div>
</a>
"""
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 20:21:43 2020

@author: Max
"""


import datetime
from selenium import webdriver
import pandas as pd
import time


driver = webdriver.Firefox()
driver.get("https://www.cnbc.com/quotes/?symbol=.SPX")


"""
Create a data frame with the values of the S&P500 and the time of each value during the session
param[in] market_value: Actual market_value
param[in] market_values: list of values collected during the session
param[in] time_values: list of the time when each values was collected

return: DataFrame with the values of the session and their times
"""
def create_market_dataFrame(market_value, market_values, time_values):
    market_value = market_value.replace(',', '')
    
    # Storage in the value list
    market_values.append(float(market_value))
    print(market_value)
    
    # Date and time retrieval
    day = str(datetime.date.today())
    hour = str(time.localtime().tm_hour)
    minute = str(time.localtime().tm_min)
    second = str(time.localtime().tm_sec)
    current_time = str(day + " " + hour + ':' + minute + ':' + second)
    
    # Storage in the time list
    time_values.append(current_time)
    
    # Creating the data frame
    return pd.DataFrame({'market_values': market_values, 'time_values': time_values})
    


"""
save the data in a csv file
param[in] market_values: list of values collected during the session
param[in] time_values: list of the time when each values was collected
"""
def save_to_csv(market_values, time_values):
    
    # Creating the data frame
    df = pd.DataFrame({'market_values': market_values, 'time_values': time_values})
    
    # Creating file name
    date = str(datetime.date.today())
    file_name = date + '.csv'
    
    # Save data in a csv file
    df.to_csv(file_name)

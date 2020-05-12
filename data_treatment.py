# -*- coding: utf-8 -*-
"""
Created on Fri May  1 20:21:43 2020

@author: Max
"""


import datetime
import pandas as pd
import time
import numpy as np

# Fetch the website

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
    
    # Date and time retrieval
    hour = str(time.localtime().tm_hour)
    minute = str(time.localtime().tm_min)
    second = str(time.localtime().tm_sec)
    current_time = str(hour + ':' + minute + ':' + second)
    
    # Storage in the time list
    time_values.append(current_time)
    
    # Creating the data frame
    return pd.DataFrame({'market_values': market_values, 'time_values': time_values})

# List of the higher values of the S&P500 each 60 seconds
high_value_list = []

# List of the lower values of the S&P500 each 60 seconds
low_value_list = []

# List og=f the color of each bar
color_list = []

# List of the time at each minute
time_values = []

"""
Create a data frame with the high values, the low values, the difference between high and low values and the time of each
parma[in] market_value_60secondes: list of the value of the market for a minute
"""
def create_high_low_df(market_value_60secondes):
    # Date and time retrieval
    hour = str(time.localtime().tm_hour)
    minute = str(time.localtime().tm_min)
    second = str(time.localtime().tm_sec)
    current_time = str(hour + ':' + minute + ':' + second)
    
    # Storage in the time list
    time_values.append(current_time)
    
    # Store the high and low values
    high_value_list.append(max(market_value_60secondes))
    low_value_list.append(min(market_value_60secondes))
    
    # Create the difference list
    diff_high_low_value = []
    for i in range(0, len(high_value_list)):
        diff_high_low_value.append(high_value_list[i] - low_value_list[i])
    
    # When the first value ina minute is lower than the last value we want the bar green, red if it's the opposite
    if market_value_60secondes[0] <= market_value_60secondes[-1]:
        color_list.append('green')
    else:
        color_list.append('red')
    
    # return the data frame with al the columns
    return pd.DataFrame({'Diff_High_Low': diff_high_low_value, 'High_values': high_value_list, 'Low_values': low_value_list,  'time_values': time_values, 'color': color_list})
    
                     
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
    
# Data for the year
df_year = pd.read_csv("SP_year.csv")

"""
Create a list of the moving average of a list
param[in] offset: offset at wich the calcul of the moving average begin 
"""
def moving_average(offset):
    
    # Create two list, one with all the sum and another of the moving average
    cumsum, moving_aves = [0], []

    # Scan the list that we want to calculate the moving average
    for i, x in enumerate(Adj_close, 1):
        
        # Calcul the sum of all the element to i
        cumsum.append(cumsum[i-1] + x)
        
        # Calculate the sum of all the element within the range of the offset
        if i>=offset:
            moving_ave = (cumsum[i] - cumsum[i-offset])/offset
            
            #can do stuff with moving_ave here
            moving_aves.append(moving_ave)
    return moving_aves

# List of all the value of the  S&P500's indices each day for a year
Adj_close = list(df_year['Adj Close'])

# Lists of moving averages
moving_average20 = moving_average(20)
moving_average50 = moving_average(50)

# Put the lists in the data frame
moving_average20_index = 0
df_year['moving_average20'] = np.nan
for i in range (20, len(df_year['Date'])):
        df_year.loc[i,'moving_average20'] = moving_average20[moving_average20_index]
        moving_average20_index += 1

moving_average50_index = 0
df_year['moving_average50'] = np.nan
for i in range (50, len(df_year['Date'])):
        df_year.loc[i,'moving_average50'] = moving_average50[moving_average50_index]
        moving_average50_index += 1



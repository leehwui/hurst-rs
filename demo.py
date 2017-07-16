import requests 
import json
import numpy as np
import pandas as pd
import math
import random
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

from datetime import datetime, timedelta 
from hurst import Hurst


def main():
    menu = {"1": ("Calculate Hurst", caculate_hurst), 
            "2": ("Calculate Circle", calculate_cirle),
            "3": ("Generate local hust graph", draw_local_hurst)}
    for key in menu:
        print(key + ": " + menu[key][0])
    ans = input("Make a choice: ");
    menu.get(ans, [None, invalid_choice])[1]()

def draw_local_hurst():
    stock_code  = input("input a stock code:")
    days_ago = input("how many days data you want to calculate? ")
    
    closing_prices = retrieve_data2(stock_code, int(days_ago))

    hurst_list = []
    xAxis = []
    expected_hurst_list = []
    for i in range(0, 800):
        if i ==0:
            data_list = closing_prices[-241:]
        else:
            data_list = closing_prices[(-241-i):-i]
        if len(data_list) == 241:
            hurst = Hurst(data_list)
            exponent = hurst.exponent()
            hurst_list.append(exponent)
            expected_hurst = hurst.expected_hurst()
            expected_hurst_list.append(expected_hurst)
            xAxis.append(i)

    hurst_list = list(reversed(hurst_list))
    aa_20 = []
    for i in range(0, len(hurst_list)):
        if i<20:
            aa = 0
        else:
            aa = np.mean(hurst_list[i-20:i])
        aa_20.append(aa)
    aa_60 = []
    for i in range(0, len(hurst_list)):
        if i <60:
            aa = 0
        else:
            aa = np.mean(hurst_list[i-60:i])
        aa_60.append(aa)
    


    fig, ax1 = plt.subplots()
    ax1.plot(xAxis, hurst_list, 'b-', label="hurst")
    #ax1.plot(xAxis, aa_20, 'y-', label="20 day anti-aliasing")
    #ax1.plot(xAxis, aa_60, 'g-', label="60 day anti-aliasing")
    ax1.plot(xAxis, expected_hurst_list, 'b-', label="expected hurst")
    ax1.set_ylabel('hurst', color='b')

    ax2 = ax1.twinx()
    ax2.plot(xAxis, closing_prices[-len(xAxis):], 'r-', label="index")
    ax2.set_ylabel('index', color='r')
    #ax2.axis([0,240,0,4500])

    plt.legend()
    plt.show()

def caculate_hurst():
    stock_code  = input("input a stock code:")
    
    closing_prices = retrieve_data(stock_code)
    #closing_prices = fake_data('tr')
    if len(closing_prices) > 0:
        hurst = Hurst(closing_prices)
        hurst.exponent()
    else:
        print("failed to retrieve data.")

def calculate_cirle():
    stock_code  = input("input a stock code:")
    days_ago = input("how many days data you want to calculate? ")
    
    closing_prices = retrieve_data(stock_code, int(days_ago))
    #closing_prices = fake_data('tr')
    if len(closing_prices) > 0:
        hurst = Hurst(closing_prices)
        hurst.circle()
    else:
        print("failed to retrieve data.")

def invalid_choice():
    print("Invalid Choice!")

def retrieve_data2(stock_code, days_ago):
    base_url = 'http://stock.liangyee.com/bus-api/stock/freeStockMarketData'
    url = base_url + '/getDailyKBar'
    user_key = 'C293FB23EC384847A4AAA3AA3DD85C9A'

    now = datetime.now()
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date  = (now - timedelta(days = days_ago)).strftime("%Y-%m-%d")

    payload = {'userKey': user_key, 'symbol': stock_code, 'startDate':
            start_date, 'endDate': end_date, 'type': 0}

    response = requests.get(url, params=payload)
    if (response.status_code == requests.codes.ok):
        data = json.loads(response.content)
        result = data['result']
        if len(result) <= 0:
            return False 
        columns = data['columns'].split(',')
        index = []
        series_data = []
        for item in result:
            splited = item.split(',')
            index.append(splited[0])
            series_data.append(float(splited[2]))
        return pd.Series(series_data, index=index) 
    else:
        response.raise_for_status()
    
def retrieve_data(stock_code, days_ago):
    base_url = 'http://stock.liangyee.com/bus-api/stock/freeStockMarketData'
    url = base_url + '/getDailyKBar'
    user_key = 'C293FB23EC384847A4AAA3AA3DD85C9A'

    now = datetime.now()
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date  = (now - timedelta(days = days_ago)).strftime("%Y-%m-%d")

    payload = {'userKey': user_key, 'symbol': stock_code, 'startDate':
            start_date, 'endDate': end_date, 'type': 0}

    response = requests.get(url, params=payload)
    if (response.status_code == requests.codes.ok):
        data = json.loads(response.content)
        result = data['result']
        if len(result) <= 0:
            return False 
        closing_prices = []
        for item in result:
            splited = item.split(',')
            closing_prices.append((float)(splited[2]))
        return closing_prices 
    else:
        response.raise_for_status()


def fake_data(data_type):
    if data_type == 'gbm':
        return np.log(np.cumsum(np.random.randn(10000))+1000)
    elif data_type == 'mr':
        return np.log(np.random.randn(10000)+1000)
    elif data_type == 'tr':
        return np.log(np.cumsum(np.random.randn(10000)+1)+1000)



if __name__ == '__main__':
    main()

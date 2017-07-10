import requests 
import json
import numpy as np
import math
import random
from datetime import datetime, timedelta 


def main():
    stock_code  = input("Input stock code: ")
    
    closing_prices = retrieve_data(stock_code)
    #closing_prices = fake_data('tr')
    if (len(closing_prices) >= 1):
        
        subtracted = np.subtract(np.log(closing_prices[1:]), np.log(closing_prices[:-1]))
        length = len(subtracted)

        rg = range(4, math.floor(len(subtracted)/4))

        index = []
        
        # independent variable
        i_var = [] 
        # dependent variable
        d_var = []
        for i in rg:
            reshaped = reshape_list(subtracted, i)

            lst_r_per_s = []
            for item in reshaped:
                if len(item) == i:
                    r_per_s = caculate_r_per_s(item)
                    print("r_p_s: ")
                    print(r_per_s)
                    lst_r_per_s.append(r_per_s)
            
            i_var.append(i)
            d_var.append(np.mean(lst_r_per_s))

        log_rs = np.log(d_var)
        log_n = np.log(i_var)
        hurst = np.polyfit(log_n,log_rs,1)
        print("The Hurst Exponent is: ")
        print(hurst[0])
        
    else:
        print("failed to retrieve data.")


def retrieve_data(stock_code):
    data = [] 
    for i in range(1, 1000):
        #data.append(random.randint(1,20))
        data.append(i)
    return data
    base_url = 'http://stock.liangyee.com/bus-api/stock/freeStockMarketData'
    url = base_url + '/getDailyKBar'
    user_key = 'C293FB23EC384847A4AAA3AA3DD85C9A'

    now = datetime.now()
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date  = (now - timedelta(days = 365)).strftime("%Y-%m-%d")

    payload = {'userKey': user_key, 'symbol': stock_code, 'startDate':
            start_date, 'endDate': end_date, 'type': 0}

    response = requests.get(url, params=payload)
    if (response.status_code == requests.codes.ok):
        data = json.loads(response.content)
        result = data['result']
        closing_prices = []
        for item in result[-240:]:
            splited = item.split(',')
            closing_prices.append((float)(splited[2]))
        return data
    else:
        response.raise_for_status()



def reshape_list(values, n):
    return [values[i:i+n] for i in range(0, len(values), n)]

def caculate_r_per_s(sublist):
    e = np.mean(sublist)
    
    d = [x-e for x in sublist]

    x = np.cumsum(d) 
    R = np.max(x) - np.min(x)
    S = np.std(sublist)

    return R/S

def fake_data(data_type):
    if data_type == 'gbm':
        return np.log(np.cumsum(np.random.randn(10000))+1000)
    elif data_type == 'mr':
        return np.log(np.random.randn(10000)+1000)
    elif data_type == 'tr':
        return np.log(np.cumsum(np.random.randn(10000)+1)+1000)

if __name__ == '__main__':
    main()

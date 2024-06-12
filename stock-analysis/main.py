# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import requests
from datetime import datetime, timedelta

# Use your own api key here
with open('api-key.txt') as file:
    api_key = file.readline()


class Stock:
    def __init__(self, ticker_symbol):
        self.ticker_symbol = ticker_symbol
        self.set_stock_values()
        
    
    def set_stock_values(self):
        url = f"https://api.twelvedata.com/time_series?&start_date=2023-01-01&end_date=2024-06-12&symbol={self.ticker_symbol}&interval=1day&apikey={api_key}"
        response = requests.get(url).json()
        
        # Last element should be latest value
        self.values = response["values"][::-1]
        
        
    def plot(self):
        self.dates = []
        self.prices = []
        
        for value in self.values:
            self.dates.append(
                datetime.strptime(
                    value["datetime"], '%Y-%m-%d')
                )
            
            self.prices.append(float(value["close"]))
        
        
        plt.title(f'Stock: {self.ticker_symbol}')
        plt.plot(self.dates, self.prices, 'k', label="Close")
        plt.plot(self.dates, self.moving_average(), '--r', label="Moving average 10")
        plt.plot(self.dates, self.moving_average(50), linestyle="dotted", color="blue", label="Moving average 50")
        plt.plot(self.dates, self.moving_average(200), '-.g', label="Moving average 200")
        plt.xlim(self.dates[0] + timedelta(days=200), self.dates[-1])
        plt.legend()
        plt.grid()
        plt.gcf().autofmt_xdate()
        plt.xlabel("Date")
        plt.ylabel("Price at close (USD)")
        plt.show()
        
        
    def moving_average(self, w=10):
        average = []
        for i in range(len(self.prices)):
            # If we do not have w dates, we take the average of as many as we can
            if i < w:
                average.append(np.mean(self.prices[0:i+1]))
            else: # window of w dates
                average.append(np.mean(self.prices[i-w+1:i+1]))
                
        return average
    
    
    def compare_moving_averages(self):
        ma_10 = self.moving_average(10)
        ma_50 = self.moving_average(50)
        ma_200 = self.moving_average(200)
        
        if ma_50[-1] > ma_200[-1]:
            print("The moving average for the last 50 days is greater than the the last 200 days.")
        
        if ma_10[-1] > ma_50[-1]:
            print("The moving average for the last 10 days is greater than the the last 50 days.")
        
        print()
                
            
        

symbols = ["TSLA", "NVDA", "AAPL", "PARA"]

stocks = {}

for symbol in symbols:
    stock = Stock(symbol)    
    stock.plot()
    stocks[symbol] = stock






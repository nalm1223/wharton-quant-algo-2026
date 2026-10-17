# use yfinance for historical data, massive of real-time
from massive import RESTClient
import yfinance as yf
import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
import requests
import os


# extract ticker data from csv file

stocktrak_data = pd.read_csv(
    "/home/nick-mills/Documents/Investment Competition 2026-2027/open-positions-10_17_2026.csv", 
    usecols=['Symbol', 'Quantity']
)

open_total = stocktrak_data.shape[0]

dict_data = stocktrak_data.to_dict(orient="records")

yearly_trading_days = 252

for i in range(open_total):
    
    current_stock_data = yf.Ticker(dict_data[i].get("Symbol")).history(period='max')

    # annualized return

    daily_returns = current_stock_data['Close'].pct_change()
    annualized_return = np.pow(
        np.prod(daily_returns + 1),
        yearly_trading_days / daily_returns.shape[0]
    ) - 1

    # standard deviation (change to more accurate std over stock's life)

    annualized_daily_std_pct = daily_returns.std() * np.sqrt(yearly_trading_days)

    dict_data[i]['Annualized STD'] = annualized_daily_std_pct
    dict_data[i]['Annualized Return'] = annualized_return

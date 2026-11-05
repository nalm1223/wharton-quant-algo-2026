import yfinance as yf
import pandas as pd
import numpy as np

from enum import Enum
from constants import *

class Portfolio():
    def __init__(self, stocktrax_data: list[dict[str, int]] = None):
        self.stocktrax_data = stocktrax_data
  
        # if no data is provided, fetch and format it from StockTrak
        if stocktrax_data is None:
            self.make_dictionary_data()

        self.make_data()

    def make_dictionary_data(self):

        # extract ticker data from csv file
        stocktrak_data = pd.read_csv(
            "StockTrak Data 2026-2027/OpenPosition_11_2_2026.csv", 
            usecols=['Symbol', 'Quantity', 'LastPrice']
        )

        total_open_positions = stocktrak_data.shape[0]

        dict_data = stocktrak_data.to_dict(orient="records")

        return_matrix_size = self.make_returns_matrix_size(dict_data)
        self.return_matrix = np.zeros(shape=return_matrix_size)

        for i in range(total_open_positions):
            
            current_stock_data = yf.Ticker(dict_data[i].get("Symbol")).history(period='max')
            # annualized return

            daily_returns = current_stock_data['Close'].pct_change()
            daily_returns = daily_returns.iloc[-return_matrix_size[1]:].dropna()

            self.return_matrix[i] = np.array(daily_returns)

            annualized_return = np.pow(
                np.prod(daily_returns + 1),
                TRADE_DAYS / daily_returns.shape[0]
            ) - 1

            # standard deviation 

            annualized_daily_std_pct = daily_returns.std() * np.sqrt(TRADE_DAYS)

            dict_data[i]['Annualized STD'] = annualized_daily_std_pct
            dict_data[i]['Annualized Return'] = annualized_return

        self.stocktrax_data = dict_data

    def make_ticker_name_list(self):
            self.ticker_names = [stock.get('Symbol') for stock in self.stocktrax_data]

    def make_open_pos_total(self):
        self.open_total = round(
            np.sum([self.stocktrax_data[i].get('LastPrice') * self.stocktrax_data[i].get("Quantity") 
            for i in range(len(self.stocktrax_data))]), 2
        )

    def make_weighted_return(self):
        self.weights = np.array([
            stock['LastPrice'] * stock["Quantity"] / self.open_total 
            for stock in self.stocktrax_data
        ])

        self.annualized_returns = [stock.get('Annualized Return') for stock in self.stocktrax_data]
        self.weighted_return =  np.average(self.annualized_returns, weights=self.weights)
    
    def make_returns_matrix_size(self, data) -> tuple:
        daily_return_sizes = np.array([
                yf.Ticker(stock['Symbol'])
                .history(period="max")['Close']
                .dropna()
                .shape[0] 
                for stock in data
        ])
        return (len(data), np.min(daily_return_sizes)-1)

    def make_portfolio_risk(self):
        self.covariance_matrix = np.cov(self.return_matrix) * 252
        self.std = np.sqrt(np.dot(self.weights.T, np.dot(self.covariance_matrix, self.weights)))

    def make_data(self):

        self.make_ticker_name_list()
        self.make_open_pos_total()
        self.make_weighted_return()
        self.make_portfolio_risk()

    def get_portfolio_size(self):
        return len(self.stocktrax_data)
    def __add__(self, other):

        # add quanitites of new data with old data
        previous_portfolio = self.stocktrax_data
        added_allocations = other.stocktrax_data
        
        new_portfolio = Portfolio(previous_portfolio)

        for i in range(len(previous_portfolio)):
            new_portfolio[i]['LastPrice'] = previous_portfolio[i]['LastPrice'] + added_allocations[i]['LastPrice']

        return new_portfolio

    def __sub__(self, other):
    
            # subtract quanitites of new data with old data
            previous_portfolio = self.stocktrax_data
            added_allocations = other.stocktrax_data
            
            new_portfolio = Portfolio(previous_portfolio)
    
            for i in range(len(previous_portfolio)):
                new_portfolio[i]['LastPrice'] = previous_portfolio[i]['LastPrice'] - added_allocations[i]['LastPrice']
    
            return new_portfolio

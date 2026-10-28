import yfinance as yf
import pandas as pd
import numpy as np

from constants import *

class Portfolio():
    def __init__(self, stocktrax_data: dict[str, int] = None):
        self.stocktrax_data = stocktrax_data

        # if no data is provided, fetch and format it from StockTrak
        if stocktrax_data is None:
            self.make_dictionary_data()

        self.make_data()

    def make_dictionary_data(self):
        
        # extract ticker data from csv file
        stocktrak_data = pd.read_csv(
            "Investment Competition 2026-2027/OpenPosition_10_27_2026.csv", 
            usecols=['Symbol', 'Quantity', 'LastPrice']
        )

        total_open_positions = stocktrak_data.shape[0]

        dict_data = stocktrak_data.to_dict(orient="records")

        for i in range(total_open_positions):
            
            current_stock_data = yf.Ticker(dict_data[i].get("Symbol")).history(period='max')

            # annualized return

            daily_returns = current_stock_data['Close'].pct_change()
            annualized_return = np.pow(
                np.prod(daily_returns + 1),
                TRADE_DAYS / daily_returns.shape[0]
            ) - 1

            # standard deviation (change to more accurate std over stock's life)

            annualized_daily_std_pct = daily_returns.std() * np.sqrt(TRADE_DAYS)

            dict_data[i]['Annualized STD'] = annualized_daily_std_pct
            dict_data[i]['Annualized Return'] = annualized_return

        self.stocktrax_data = dict_data

    def make_ticker_list(self):
            self.tickers = [yf.Ticker(stock.get('Symbol')) for stock in self.stocktrax_data]

    def make_open_pos_total(self):
        self.open_total = round(
            np.sum([self.stocktrax_data[i].get('LastPrice') * self.stocktrax_data[i].get("Quantity") 
            for i in range(len(self.stocktrax_data))]), 2
        )

    def make_weighted_return_and_std(self):
        self.weights = np.array([
            self.stocktrax_data[i].get('LastPrice') * self.stocktrax_data[i].get("Quantity") / self.open_total 
            for i in range(len(self.stocktrax_data))
        ])
        returns = [stock.get('Annualized Return') for stock in self.stocktrax_data]

        self.weighted_return =  np.average(returns, weights=self.weights)
        self.weighted_std = np.sqrt(np.average((returns - self.weighted_return) ** 2, weights=self.weights))
    
    def make_data(self):

        self.make_ticker_list()
        self.make_open_pos_total()
        self.make_weighted_return_and_std()

    def order_by_last_price(self) -> list[dict]:
        ordered_stocks = self.stocktrax_data

        for i in range(1, len(self.stocktrax_data)):
            key = ordered_stocks[i].get('LastPrice')
            j = i - 1

            while j >= 0 and ordered_stocks[j].get('LastPrice') > key:
                ordered_stocks[j + 1]['LastPrice'] = ordered_stocks[j]['LastPrice']
                j -= 1

            ordered_stocks[j + 1]['LastPrice'] = key
        return ordered_stocks
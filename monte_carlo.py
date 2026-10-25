import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from portfolio_data import dict_data
from constants import *

# monte carlo class

class Monte_Carlo():

    def __init__(self, portfolio: dict[str, int], start_date: pd.Timestamp, sim_years: int, sim_count: int = 10_000) -> None:
        self.portfolio = portfolio
        self.start_date = start_date
        self.sim_years = sim_years
        self.sim_count = sim_count

    def make_ticker_list(self):
        self.tickers = [yf.Ticker(stock.get('Symbol')) for stock in self.portfolio]
    
    def make_todays_ticker_prices(self):
        self.current_prices = [ticker.fast_info.last_price for ticker in self.tickers]

    def make_open_pos_total(self):
        self.open_total = round(np.sum([self.current_prices[i] * self.portfolio[i].get("Quantity") for i in range(len(self.portfolio))]), 2)

    def make_weighted_return_and_std(self):
        weights = [self.current_prices[i] * self.portfolio[i].get("Quantity") / self.open_total for i in range(len(self.portfolio))]
        returns = [stock.get('Annualized Return') for stock in self.portfolio]

        self.weighted_return =  np.average(returns, weights=weights)
        self.weighted_std = np.sqrt(np.average((returns - self.weighted_return) ** 2, weights=weights))
    
    def make_data(self):

        self.make_ticker_list()
        self.make_todays_ticker_prices()
        self.make_open_pos_total()
        self.make_weighted_return_and_std()

    def make_simulation_prices(self):
        
        self.make_data()

        days_to_predict = self.sim_years * TRADE_DAYS
        dt = 1 / TRADE_DAYS

        dist_size = (self.sim_count, days_to_predict)
    
        simulations_normal = np.random.normal(loc=(1 + self.weighted_return) ** dt, scale=self.weighted_std * np.sqrt(dt), size=dist_size)
    
        simulations_normal = np.concat(
            (np.ones((self.sim_count, 1)), simulations_normal),
            axis = 1
        )
    
        self.normal_prices = self.open_total * simulations_normal.cumprod(axis=1)
        self.date_range = pd.date_range(start=self.start_date, periods=days_to_predict + 1, freq='B')

    def plot_simulations(self):

        for i in range(self.sim_count):
            plt.plot(self.date_range, self.normal_prices[i], alpha = 0.05)
        plt.show()

        final_normal_prices = self.normal_prices[:, -1]
        plt.hist(final_normal_prices, bins = 100, edgecolor= '000000')
        plt.show()
    

# monte carlo w/ initial investment

start_date = '2027-01-01 00:00:00'  
initial_monte_carlo = Monte_Carlo(dict_data, start_date, sim_years=16, sim_count=10_000)

initial_monte_carlo.make_simulation_prices()
initial_monte_carlo.plot_simulations()

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from portfolio_data import Portfolio
from constants import *

# monte carlo class

class Monte_Carlo():

    def __init__(self, portfolio: Portfolio, start_date: pd.Timestamp, sim_years: int, sim_count: int = 10_000) -> None:
        self.portfolio = portfolio
        self.start_date = start_date
        self.sim_years = sim_years
        self.sim_count = sim_count

    def make_simulation_prices(self):

        days_to_predict = self.sim_years * TRADE_DAYS
        dt = 1 / TRADE_DAYS
        
        dist_size = (self.sim_count, days_to_predict)
    
        simulations_normal = np.random.normal(loc=(1 + self.portfolio.weighted_return) ** dt, scale=self.portfolio.std * np.sqrt(dt), size=dist_size)
    
        simulations_normal = np.concat(
            (np.ones((self.sim_count, 1)), simulations_normal),
            axis = 1
        )
    
        self.p_normal_prices = self.portfolio.open_total * simulations_normal.cumprod(axis=1)
        self.date_range = pd.date_range(start=self.start_date, periods=days_to_predict + 1, freq='B')

    def make_ticker_simulation_prices(self, ticker_index):

        days_to_predict = self.sim_years * TRADE_DAYS
        dt = 1 / TRADE_DAYS
        
        dist_size = (self.sim_count, days_to_predict)
    
        simulations_normal = np.random.normal(
            loc=(1 + self.portfolio.stocktrax_data[ticker_index]['Annualized Return']) ** dt, 
            scale=self.portfolio.stocktrax_data[ticker_index]['Annualized STD'] * np.sqrt(dt), size=dist_size
        )
    
        simulations_normal = np.concat(
            (np.ones((self.sim_count, 1)), simulations_normal),
            axis = 1
        )
    
        self.t_normal_prices = self.portfolio.stocktrax_data[ticker_index]['LastPrice'] * simulations_normal.cumprod(axis=1)
        self.date_range = pd.date_range(start=self.start_date, periods=days_to_predict + 1, freq='B')

    def plot_p_simulations(self):

        for i in range(self.sim_count):
            plt.plot(self.date_range, self.p_normal_prices[i], alpha = 0.05)
        plt.show()

        final_normal_prices = self.p_normal_prices[:, -1]
        plt.hist(final_normal_prices, bins = 100, edgecolor= '000000')
        plt.show()

    def plot_t_simulations(self):
        for i in range(self.sim_count):
            plt.plot(self.date_range, self.t_normal_prices[i], alpha = 0.05)
        plt.show()

        final_normal_prices = self.t_normal_prices[:, -1]
        plt.hist(final_normal_prices, bins = 100, edgecolor= '000000')
        plt.show()

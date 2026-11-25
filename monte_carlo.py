import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from portfolio_data import Portfolio
from constants import *

# monte carlo class

class Monte_Carlo():

    def __init__(self, portfolio: Portfolio, sim_years: int = 16, start_date: pd.Timestamp = '2027-01-01 00:00:00', end_date: pd.Timestamp = '2043-01-01 00:00:00', sim_count: int = 10_000) -> None:
        
        self.portfolio = portfolio
        self.start_date = start_date
        self.end_date = end_date

        self.sim_years = sim_years
        self.sim_count = sim_count

        self.dt = 1 / TRADE_DAYS

        self.date_range = pd.date_range(start=self.start_date, end=self.end_date, freq='B')
        self.dist_size = (self.sim_count, len(self.date_range) - 1)

    def make_p_simulation_prices(self):
        
        simulations_normal = np.random.normal(
            loc=(1 + self.portfolio.weighted_return) ** self.dt, 
            scale=self.portfolio.std * np.sqrt(self.dt), 
            size=self.dist_size
        )
    
        simulations_normal = np.concat(
            (np.ones((self.sim_count, 1)), simulations_normal),
            axis = 1
        )
    
        self.p_normal_prices = self.portfolio.open_total * simulations_normal.cumprod(axis=1)

    def make_t_simulation_prices(self, ticker_index):
    
        simulations_normal = np.random.normal(
            loc=(1 + self.portfolio.stocktrax_data[ticker_index]['Annualized Return']) ** self.dt, 
            scale=self.portfolio.stocktrax_data[ticker_index]['Annualized STD'] * np.sqrt(self.dt), size=self.dist_size
        )

        simulations_normal = np.concat(
            (np.ones((self.sim_count, 1)), simulations_normal),
            axis = 1
        )
    
        self.t_normal_prices = self.portfolio.stocktrax_data[ticker_index]['LastPrice'] * simulations_normal.cumprod(axis=1)
    
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

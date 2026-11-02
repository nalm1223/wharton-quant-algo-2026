import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from portfolio_data import Portfolio
from monte_carlo import Monte_Carlo
from constants import *

# monte carlo w/ initial investment

start_date = '2028-01-01 00:00:00'  
competition_portfolio = Portfolio()

initial_monte_carlo = Monte_Carlo(portfolio=competition_portfolio, start_date=start_date, sim_years=16, sim_count=10_000)

initial_monte_carlo.make_simulation_prices()
initial_monte_carlo.plot_simulations()

# get_youngest_IPO

# stocks = ["SMH", "SCHD"]
# daily_return_sizes = np.array([yf.Ticker(stock).history(period="max")['Close'].shape[0] for stock in stocks])
# print(np.min(daily_return_sizes))
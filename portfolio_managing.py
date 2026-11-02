"""
-input: current weights of current portfolio
-output: weights to adjust portfolio for following year
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimize

from portfolio_data import Portfolio
from monte_carlo import Monte_Carlo
from constants import *

year_0_portfolio = Portfolio()
weights_0 = year_0_portfolio.weights

# get daily returns and covarience for sharpe

closing_prices = yf.download(year_0_portfolio.ticker_names, period='max', auto_adjust=False)['Adj Close'].dropna(axis=1)
returns_0 = np.log(closing_prices / closing_prices.shift())

print(closing_prices)
print(weights_0)

def portfolio_risk(returns, weights):
    """
    Calculates the covariance matrix of the daily returns, adjusting for a year,
    and then calculates the standard deviation of the portfolio using the given
    weights.
    """

    cov_matrix = returns.cov() * 252 # Calculate the covariance matrix

    risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

    return risk

# print(portfolio_return(returns_0, weights_0))
# print(year_0_portfolio.weighted_return)
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
returns = year_0_portfolio.return_matrix

def negative_sharpe_ratio(weights, rfr=RISK_FREE_RETURN):

    # after competition, improve make_weighted_return and make_portfolio_risk to be included here

    current_return = np.sum([weights[i] * returns[i].mean() for i in range(returns.shape[0])]) * TRADE_DAYS
    current_risk = np.sqrt(np.dot(weights.T, np.dot(year_0_portfolio.covariance_matrix, weights)))

    return -(current_return - rfr) / current_risk

print(negative_sharpe_ratio(weights_0))
''' ## = Code directly from Portfolio Optimization Medium'''

## This constraint means that the sum of all weights minus 1 must be equal to zero
constraints = {'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}

## This creates an array of (0, 0.5) for each stock
bounds = [(0, 0.5) for _ in range(returns.shape[0])]

optimized_results = optimize.minimize(
    fun=negative_sharpe_ratio, 
    x0=weights_0, 
    args=(0.02), 
    method='SLSQP', 
    constraints=constraints, 
    bounds=bounds
)

best_weights = optimized_results.x

print(weights_0)
print(best_weights)
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
from typing import Literal

year0_portfolio = Portfolio()
weights_0 = year0_portfolio.weights
returns = year0_portfolio.return_matrix

def negative_sharpe_ratio(weights, rfr=RISK_FREE_RETURN):

    # after competition, improve make_weighted_return and make_portfolio_risk to be included here

    current_return = np.sum([weights[i] * returns[i].mean() for i in range(returns.shape[0])]) * TRADE_DAYS
    current_risk = np.sqrt(np.dot(weights.T, np.dot(year0_portfolio.covariance_matrix, weights)))

    return -(current_return - rfr) / current_risk

''' ## = Code directly from Portfolio Optimization Medium'''

## This constraint means that the sum of all weights minus 1 must be equal to zero
constraints = {'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}

## This creates an array of (0, 0.5) for each stock
bounds = [(0, 0.7) for _ in range(returns.shape[0])]

optimized_results = optimize.minimize(
    fun=negative_sharpe_ratio, 
    x0=weights_0, 
    method='COBYLA', 
    constraints=constraints, 
    bounds=bounds
)

best_weights = optimized_results.x

print(f'Initial Weights: \n{weights_0}')
print(f'Initial Return: {year0_portfolio.weighted_return}, Initial STD: {year0_portfolio.std}')
print(f'Initial Sharpe Ratio: {negative_sharpe_ratio(weights_0)}\n')

'''
Important Years:
2027 - Initial 300k invetsment
2028 - Additional 150k
2031 - Presenation to co-sponsors
2033 - Beginning of deallocation
2043 - Ending of deallocation (through)
'''
year_range = Literal[np.arange(0, 15)]

# def get_projected_ticker_prices(portfolio: Portfolio, sim_years, percentile=50):
#     portfolio_monte_carlo = Monte_Carlo(portfolio, sim_years)
#     projected_prices = np.zeros((len(portfolio.ticker_names), sim_years))

#     # index of first day of each year
#     days_passed = (portfolio_monte_carlo.date_range[-1] - portfolio_monte_carlo.date_range[0]).days
#     print(portfolio_monte_carlo.date_range[-1])
    
#     # for ticker in tickers:
#     #     ticker_index = np.where(tickers = ticker)[0]

#     #     ticker_price_distribution = portfolio_monte_carlo.make_t_simulation_prices(ticker_index)

#         # get price at beginning of every year and put it in projected_prices

# get_projected_ticker_prices(year_0_portfolio, 16)
    

def weights_to_allocation(current_portfolio: Portfolio, target_weights, allocation_amount=None, current_year = year_range, target_open_total=None, percentile=50):
    
    if(allocation_amount and target_open_total is None):
        raise ValueError('Either allocation amount or target open total needs to be provided')
    
    # current_weights = current_portfolio.weights
    # weight_change = current_weights - target_weights
    # allocation_change = weight_change * current_portfolio.open_total

    if target_open_total:
        new_portfolio = current_portfolio
        ticker_totals = target_weights * target_open_total
        
        for (i, stock) in enumerate(new_portfolio.stocktrax_data):
            new_quantity = (ticker_totals[i] // stock['LastPrice']) * (ticker_totals[i] > stock['LastPrice'])
            stock['Quantity'] = int(new_quantity)

        # invest remaining money in stock with loewest sharpe ratio

        lowest_sharpe = np.min([stock['Annualized Return'] for stock in new_portfolio.stocktrax_data])
        return new_portfolio

optimized_year0_portfolio = weights_to_allocation(year0_portfolio, best_weights, target_open_total=YEAR0_INVESTMENT)
optimized_year0_portfolio.make_data()

print(f'Optimized Weights: \n{optimized_year0_portfolio.weights}')
print(f'Optimized Return: {optimized_year0_portfolio.weighted_return}, Optimized STD: {optimized_year0_portfolio.std}')
print(f'Optimized Sharpe Ratio: {negative_sharpe_ratio(best_weights)}\n')

print(f'{optimized_year0_portfolio.stocktrax_data}\n')
print(YEAR0_INVESTMENT - optimized_year0_portfolio.open_total)


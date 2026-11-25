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

def negative_sharpe_ratio(weights, portfolio: Portfolio, rfr=RISK_FREE_RETURN) -> float:
    # after competition, improve make_weighted_return and make_portfolio_risk to be included here

    current_return = np.sum([
        weights[i] * portfolio.return_matrix[i].mean() for i in range(portfolio.return_matrix.shape[0])
    ]) * TRADE_DAYS

    current_risk = np.sqrt(np.dot(portfolio.weights.T, np.dot(portfolio.covariance_matrix, portfolio.weights)))

    return -(current_return - rfr) / current_risk

class Managing:
    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio

    def make_optimized_weights(self):
        ''' ## = Code directly from Portfolio Optimization Medium'''

        ## This constraint means that the sum of all weights minus 1 must be equal to zero
        constraints = {'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}

        bounds = [(0.05, 0.4) for _ in range(self.portfolio.return_matrix.shape[0])]

        weights_0 = self.portfolio.weights

        optimized_results = optimize.minimize(
            fun=negative_sharpe_ratio, 
            x0=weights_0, 
            args=self.portfolio,
            method='COBYLA', 
            constraints=constraints, 
            bounds=bounds
        )

        return np.array([optimized_results.x])

    def weights_to_allocation(self, target_weights, target_open_total) -> Portfolio:
        
        new_portfolio = self.portfolio
        ticker_totals = target_weights * target_open_total
        
        for (i, stock) in enumerate(new_portfolio.stocktrax_data):
            new_quantity = (ticker_totals[:, i] // stock['LastPrice']) * (ticker_totals[:, i] > stock['LastPrice'])
            stock['Quantity'] = new_quantity.item()

        # invest remaining money in stock with loewest sharpe ratio

        return new_portfolio

year0_portfolio = Portfolio()
managing_year0 = Managing(year0_portfolio)

print(f'Initial Weights: \n{year0_portfolio.weights}')
print(f'Initial Return: {year0_portfolio.weighted_return}, Initial STD: {year0_portfolio.std}')
print(f'Initial Sharpe Ratio: {negative_sharpe_ratio(year0_portfolio.weights, year0_portfolio)}\n')

best_weights = managing_year0.make_optimized_weights()

optimized_year0_portfolio = managing_year0.weights_to_allocation(best_weights, target_open_total=YEAR0_INVESTMENT)
optimized_year0_portfolio.make_data()

print(f'Optimized Weights: \n{optimized_year0_portfolio.weights}')
print(f'Optimized Return: {optimized_year0_portfolio.weighted_return}, Optimized STD: {optimized_year0_portfolio.std}')
print(f'Optimized Sharpe Ratio: {negative_sharpe_ratio(optimized_year0_portfolio.weights, optimized_year0_portfolio)}\n')

print(f'{optimized_year0_portfolio.stocktrax_data}\n')
print(YEAR0_INVESTMENT - optimized_year0_portfolio.open_total)


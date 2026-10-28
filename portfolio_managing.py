"""
-input: current weights of current portfolio
-output: weights to adjust portfolio for following year
"""
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from portfolio_data import Portfolio
from monte_carlo import Monte_Carlo
from constants import *

year_0_portfolio = Portfolio()
weights_0 = year_0_portfolio.weights
print(sum(weights_0) - 1)


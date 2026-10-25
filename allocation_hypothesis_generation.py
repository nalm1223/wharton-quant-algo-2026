"""
-Start with list of possible allocations/deallocations given budget and current portfolio
    -Make sure to account for market fluctuation over 1 year when determining ticker share prices and quantities
-Option A:
    -Test hypothesis w/ Monte Carlo and get return (median from new distribution)
    -Repeat for y interations
    -Keep allocation strategy with highest return
-Option B:
    -machine learning through gradient descent (modelling target return to coefficients and adjusting allocations to fit target)

"""
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from portfolio_data import Portfolio
from monte_carlo import Monte_Carlo
from constants import *

def generate_allocation_possibilities(portfolio, amount):
    pass
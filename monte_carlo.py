import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from portfolio_data import dict_data

# initial criteria/constants
year0_investment = 300_000
year0_investment = 150_000
operating_reserve = 50_000

trade_days = 252

# get weighted average return and standard deviation

tickers = [yf.Ticker(data.get('Symbol')) for data in dict_data]
last_prices = [ticker.fast_info.last_price for ticker in tickers]
total_invested = round(np.sum([last_prices[i] * dict_data[i].get("Quantity") for i in range(len(dict_data))]), 2)

weights = [tickers[i].fast_info.last_price * dict_data[i].get("Quantity") / total_invested for i in range(len(dict_data))]
returns = [data.get('Annualized Return') for data in dict_data]

weighted_return = np.average(returns, weights=weights)

weighted_std = np.sqrt(np.average((returns - weighted_return) ** 2, weights=weights))

# monte carlo w/ initial investment

sim_count = 50000
sim_years = 1
dt = 1 / trade_days

days_to_predict = sim_years * trade_days
start_date = '2026-10-17 00:00:00'

dist_size = (sim_count, days_to_predict)

simulations_normal = np.random.normal(loc=(1 + weighted_return) ** dt, scale=weighted_std * np.sqrt(dt), size=dist_size)

simulations_normal = np.concat(
    (np.ones((sim_count, 1)), simulations_normal),
    axis = 1
)
normal_prices = total_invested * simulations_normal.cumprod(axis=1)

print(simulations_normal.shape)

date_range = pd.date_range(start=start_date, periods=days_to_predict + 1, freq='B')

## plots

# for i in range(sim_count):
#     plt.plot(date_range, normal_prices[i], alpha = 0.08)
# plt.show()

final_normal_prices = normal_prices[:, -1]
plt.hist(final_normal_prices, bins = 100, edgecolor= '000000')
plt.show()
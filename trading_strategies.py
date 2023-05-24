import pandas as pd
import yfinance as yf

# Define the lookback period for calculating moving average and standard deviation
lookback = 20

# Fetch historical data
data = yf.download('AAPL', period='1d', interval='1m').dropna()

# Calculate mean and standard deviation
data['avg'], data['std'] = data['Close'].rolling(window=lookback).mean(), data['Close'].rolling(window=lookback).std()

# Define the mean-reversion strategy
def mean_reversion(data):
    # If the current price is higher than the mean + 1 standard deviation, short
    if data['Close'][-1] > data['avg'][-1] + data['std'][-1]:
        return -1
    # If the current price is lower than the mean - 1 standard deviation, long
    elif data['Close'][-1] < data['avg'][-1] - data['std'][-1]:
        return 1
    # Do nothing if the price is within one standard deviation of the mean
    else:
        return 0

# Define the momentum-based strategy
def momentum_based(data):
    # If the current price is higher than the mean, long
    if data['Close'][-1] > data['avg'][-1]:
        return 1
    # If the current price is lower than the mean, short
    elif data['Close'][-1] < data['avg'][-1]:
        return -1
    # Do nothing if the price is equal to the mean
    else:
        return 0

import pandas as pd
import numpy as np

data = pd.read_csv('data.csv')

def calculate_sma(data, window, ticker, var):
    return data[var].rolling(window=window).mean()

data['sma_50_p'] = np.nan
data['sma_200_v'] = np.nan
data['sma_50_p'] = np.nan
data['sma_200_v'] = np.nan

# calculate the simple moving average for the price and volume column
for t in pd.unique(data.ticker): # for each ticker
    dt = data[data.ticker == t]
    data.loc[data.ticker==t,'sma_50_p'] = calculate_sma(dt, 50, t, 'last')
    data.loc[data.ticker==t,'sma_200_p'] = calculate_sma(dt, 200, t, 'last')
    data.loc[data.ticker==t,'sma_50_v'] = calculate_sma(dt, 50, t, 'volume')
    data.loc[data.ticker==t,'sma_200_v'] = calculate_sma(dt, 200, t, 'volume')

# initialize trade signal
data['signal'] = 0

# buy signal (low price and low volume)
data.loc[(data['sma_50_p'] < data['sma_200_p']) & (data['sma_50_v'] < data['sma_200_v']), 'signal'] = 1  # Buy signal
# sell signal (hight price and high volume)
data.loc[(data['sma_50_p'] > data['sma_200_p']) & (data['sma_50_v'] > data['sma_200_v']), 'signal'] = -1  # Sell signal

# apply this strategy to each ticker and compare their results
portfolio_value = {}

for t in pd.unique(data.ticker):

    d = data[data.ticker == t]

    cash = 100000 # initial cash
    positions = 0 # initial position

    for index, row in d.iterrows():
        ticker = row['ticker']
        price = row['last']
        volume = row['volume']
        signal = row['signal']

        if signal == 1:  # buy signal
            # calculate the number of shares to buy based on available funds and positio
            shares_to_buy = cash * 0.25 / price  # allocate 25% of cash
            cash *= 0.75
            positions += shares_to_buy

        elif signal == -1:  # sell signal
            if positions > 0:
                # sell all positions
                shares_to_sell = positions
                cash += shares_to_sell * price
                positions = 0 # reset position

    portfolio_value[t] = cash + price * positions # append the result for this ticker

# portfolio_value compares the strategy among different tickers
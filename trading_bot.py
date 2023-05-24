import time

# Define the list of stocks the bot will trade
symbols = ['AAPL']

# Define the quantity of stocks to trade
qty = 1

# Run the bot
while True:
    for symbol in symbols:
        # Fetch the latest data
        data = yf.download(symbol, period='1d', interval='1m').dropna()
        data['avg'], data['std'] = data['Close'].rolling(window=lookback).mean(), data['Close'].rolling(window=lookback).std()

        # Decide on the strategy to use
        strategy = mean_reversion if data['std'][-1] > 0 else momentum_based

        # Get the trading signal from the strategy
        signal = strategy(data)

        # Place the appropriate order based on the signal
        if signal == 1:
            place_order(strategy='mean_reversion', symbol=symbol, qty=qty, side='buy', typ='market', time_in_force='gtc')
        elif signal == -1:
            place_order(strategy='mean_reversion', symbol=symbol, qty=qty, side='sell', typ='market', time_in_force='gtc')

    # Wait for the next minute
    time.sleep(60)

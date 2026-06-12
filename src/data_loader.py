import yfinance as yf

def load_data(symbol,period,interval):
    equity = yf.Ticker(symbol).history(period=period, interval=interval)
    equity = equity.dropna()
    return equity

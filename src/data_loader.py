import yfinance as yf

def load_data(symbol):
    data= yf.download(symbol,period='1y')
    return data
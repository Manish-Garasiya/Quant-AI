def execute(data):
    data['position'] = data['signal'].shift()

    data['returns'] = data['position']*data['Close'].pct_change()

    delta = data["Close"].diff()
    data['delta'] = delta*data['position']

    return data
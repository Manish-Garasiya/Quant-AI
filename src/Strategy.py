def signal(data):
    data['signal'] = 0

    macd = (data['adx'] >25)
    trend_filter = data['Close'] > data['ema_100']

    bullish = (
            (data['di_plus']>data['di_minus']) & 
            (data['macd']>data['signal_line']) & 
            (data['macd'] > 0) &
            (data['adx'] > data['adx'].shift(1))
        )
    bearish = (
            (data['di_plus']<data['di_minus']) & 
            (data['macd']<data['signal_line']) & 
            (data['macd'] < 0) &
            (data['adx'] > data['adx'].shift(1))
        )
    data.loc[macd & bullish & trend_filter, 'signal'] = 1
    data.loc[macd & bearish & ~trend_filter, 'signal'] = -1

    return data                    

def hybrid_signal(data, prob_col="probability_up", threshold=0.70):
    data = data.copy()
    data["hybrid_signal"] = 0

    trend_strength = data["adx"] > 25
    trend_filter = data["Close"] > data["ema_100"]

    bullish = (
        (data["di_plus"] > data["di_minus"]) &
        (data["macd"] > data["signal_line"]) &
        (data["macd"] > 0)
    )

    bearish = (
        (data["di_plus"] < data["di_minus"]) &
        (data["macd"] < data["signal_line"]) &
        (data["macd"] < 0)
    )

    if prob_col in data.columns:
        data.loc[
            trend_strength & bullish & trend_filter & (data[prob_col] >= threshold),
            "hybrid_signal"
        ] = 1

        data.loc[
            trend_strength & bearish & (~trend_filter) & (data[prob_col] <= 1 - threshold),
            "hybrid_signal"
        ] = -1

    return data
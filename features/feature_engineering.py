import pandas as pd
import numpy as np
import numpy as np
import pandas as pd


def calculate_rsi(close, period=14):
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi


def build_feature_frame(df, horizon=5):
    df = df.copy().sort_index()

    # Returns
    df["return_1d"] = df["Close"].pct_change()
    df["return_5d"] = df["Close"].pct_change(5)
    df["log_return_1d"] = np.log(df["Close"] / df["Close"].shift(1))

    # Rolling volatility
    df["volatility_20d"] = df["return_1d"].rolling(20).std() * np.sqrt(252)

    # Volume features
    df["volume_change"] = df["Volume"].pct_change()
    df["volume_ratio_20d"] = df["Volume"] / df["Volume"].rolling(20).mean()

    # Trend features
    df["sma20"] = df["Close"].rolling(20).mean()
    df["sma50"] = df["Close"].rolling(50).mean()
    df["sma200"] = df["Close"].rolling(200).mean()

    df["dist_sma20"] = (df["Close"] - df["sma20"]) / df["sma20"]
    df["dist_sma50"] = (df["Close"] - df["sma50"]) / df["sma50"]
    df["dist_sma200"] = (df["Close"] - df["sma200"]) / df["sma200"]

    # Indicator-based features
    if "macd" in df.columns and "signal_line" in df.columns:
        df["macd_hist"] = df["macd"] - df["signal_line"]
    else:
        df["macd_hist"] = np.nan

    if "di_plus" in df.columns and "di_minus" in df.columns:
        df["di_spread"] = df["di_plus"] - df["di_minus"]
    else:
        df["di_spread"] = np.nan

    if "adx" in df.columns:
        df["adx_change"] = df["adx"].diff()
    else:
        df["adx_change"] = np.nan

    # RSI
    df["rsi_14"] = calculate_rsi(df["Close"], 14)

    # Target
    df["future_return"] = (df["Close"].shift(-horizon) / df["Close"]) - 1
    df["target"] = (df["future_return"] > 0).astype(int)

    df = df.dropna().copy()
    return df


def get_feature_columns():
    return [
        "macd",
        "signal_line",
        "macd_hist",
        "adx",
        "di_plus",
        "di_minus",
        "di_spread",
        "adx_change",
        "ema_100",
        "rsi_14",
        "return_1d",
        "return_5d",
        "log_return_1d",
        "volatility_20d",
        "volume_change",
        "volume_ratio_20d",
        "dist_sma20",
        "dist_sma50",
        "dist_sma200",
    ]

class FeatureEngineer:
    def __init__(self, data):

        self.df = data.copy()

    def add_return_features(self):

        self.df["ret_1"] = self.df["Close"].pct_change()

        self.df["ret_5"] = self.df["Close"].pct_change(5)

        self.df["ret_10"] = self.df["Close"].pct_change(10)

        return self

    def add_volatility_features(self):

        self.df["volatility_20"] = (

            self.df["ret_1"]

            .rolling(20)

            .std()

        )

        return self
    
    def add_volume_features(self):

        self.df["volume_change"] = (

            self.df["Volume"]

            .pct_change()

        )

        self.df["volume_ratio"] = (

            self.df["Volume"]

            /

            self.df["Volume"]

            .rolling(20)

            .mean()

        )

        return self
    
    def add_trend_features(self):

        self.df["sma20"] = (

            self.df["Close"]

            .rolling(20)

            .mean()

        )

        self.df["sma50"] = (

            self.df["Close"]

            .rolling(50)

            .mean()

        )

        self.df["distance_sma20"] = (

            self.df["Close"]

            -

            self.df["sma20"]

        ) / self.df["sma20"]

        return self  
     
    def create_target(self):

        self.df["future_return"] = (

            self.df["Close"]

            .shift(-5)

            /

            self.df["Close"]

            - 1

        )

        self.df["target"] = (

            self.df["future_return"]

            > 0

        ).astype(int)

        return self

    def build(self):

        self.df = self.df.dropna()

        return self.df 
    

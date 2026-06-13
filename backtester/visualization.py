import matplotlib.pyplot as plt


def plot_equity_curve(df):
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["equity"])
    plt.title("Equity Curve")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value")
    plt.grid(True)
    plt.show()


def plot_price_with_trades(df):
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["Close"], label="Close")

    if "trade_action" in df.columns:
        buys = df[df["trade_action"] == "BUY"]
        sells = df[df["trade_action"] == "SELL"]
        forced = df[df["trade_action"] == "FORCED_EXIT"]

        plt.scatter(buys.index, buys["Close"], marker="^", s=100, label="Buy")
        plt.scatter(sells.index, sells["Close"], marker="v", s=100, label="Sell")
        plt.scatter(forced.index, forced["Close"], marker="x", s=100, label="Forced Exit")

    plt.title("Price with Trade Markers")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.show()
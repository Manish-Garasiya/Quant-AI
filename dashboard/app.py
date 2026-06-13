import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.data_loader import load_data
from features.Indicators import MACD, calculate_DIs_and_ADX
from strategies.Strategy import signal
from backtester.engine import BacktestEngine
from backtester.Performance import performance
from backtester.visualization import plot_equity_curve, plot_price_with_trades

st.title("QuantLab AI")

ticker = st.text_input("Ticker", value="INFY.NS")

if st.button("Run Backtest"):
    data = load_data(ticker, "5y", "1d")

    data["macd"] = MACD(data["Close"])
    data["signal_line"] = data["macd"].ewm(span=9, adjust=False).mean()
    data["di_plus"], data["di_minus"], data["adx"] = calculate_DIs_and_ADX(
        data["High"], data["Low"], data["Close"]
    )
    data["ema_100"] = data["Close"].ewm(span=100, adjust=False).mean()

    data = signal(data)

    engine = BacktestEngine(data, ticker=ticker)
    bt_df, portfolio = engine.run()
    metrics = performance(bt_df, portfolio)

    st.subheader("Metrics")
    st.dataframe(metrics.T)

    st.subheader("Closed Trades")
    trade_df = pd.DataFrame([t.to_dict() for t in portfolio.closed_trades])
    st.dataframe(trade_df)

    st.subheader("Equity Curve")
    st.line_chart(bt_df["equity"])

    st.subheader("Price with Trades")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(bt_df.index, bt_df["Close"], label="Close")
    buys = bt_df[bt_df["trade_action"] == "BUY"]
    sells = bt_df[bt_df["trade_action"] == "SELL"]
    ax.scatter(buys.index, buys["Close"], marker="^", s=100, label="Buy")
    ax.scatter(sells.index, sells["Close"], marker="v", s=100, label="Sell")
    ax.legend()
    st.pyplot(fig)
from fastapi import FastAPI
from src.data_loader import load_data
from features.Indicators import MACD, calculate_DIs_and_ADX
from strategies.Strategy import signal
from backtester.engine import BacktestEngine
from backtester.Performance import performance

app = FastAPI(title="QuantLab AI API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/backtest/{ticker}")
def run_backtest(ticker: str):
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
    return {
        "ticker": ticker,
        "metrics": metrics.T.to_dict(),
        "total_trades": len(portfolio.closed_trades),
    }
from src.data_loader import load_data
from features.Indicators import MACD, calculate_DIs_and_ADX
from strategies.Strategy import signal
from backtester.engine import BacktestEngine
from backtester.Performance import performance
from backtester.visualization import plot_equity_curve, plot_price_with_trades
import matplotlib.pyplot as plt
from features.feature_engineering import FeatureEngineer
from ml.train_model import train_model
from database.db import SessionLocal
from database.repositories import save_features,save_predictions
import pandas as pd
# from database.models import Prediction, StrategyRun, TradeModel, Stock, Feature

def main():
    ticker = str(input("Enter the ticker symbol of stock/equity: "))
    print("Loading the data....")
    data = load_data(ticker, "5y", "1d")

    print("Calculating the indicators....")
    data["macd"] = MACD(data["Close"])
    data["signal_line"] = data["macd"].ewm(span=9, adjust=False).mean()
    data["di_plus"], data["di_minus"], data["adx"] = calculate_DIs_and_ADX(
        data["High"], data["Low"], data["Close"]
    )
    data["ema_100"] = data["Close"].ewm(span=100, adjust=False).mean()

    print("Applying strategy logic....")
    data = signal(data)

    print("Running backtest engine....")
    engine = BacktestEngine(
        data=data,
        ticker=ticker,
        initial_cash=100000,
        transaction_cost_bps=10,
        signal_col="signal"
    )

    bt_df, portfolio = engine.run()

    feature_df = (
    FeatureEngineer(data)
    .add_return_features()
    .add_volatility_features()
    .add_volume_features()
    .add_trend_features()
    .create_target()
    .build()
    )
    # print(feature_df.head())

    session = SessionLocal()
    save_features(session, feature_df, ticker)

    model, prediction_df,X_test = train_model(feature_df)

    save_predictions(session,prediction_df,ticker)
    
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:,1]

    prediction_df = pd.DataFrame({

        "date": X_test.index,

        "probability_up": probs,

        "prediction": preds
    })

    
    print("Calculating results....\n")
    results = performance(bt_df, portfolio)
    print(results.T)

    print("Plotting graphs....")
    plot_price_with_trades(bt_df)
    plot_equity_curve(bt_df)

    # drawdown graph
    if "drawdown" in bt_df.columns:
        bt_df[["drawdown"]].plot(figsize=(10, 6))
        plt.title("Drawdown Graph")
        plt.xlabel("Date")
        plt.ylabel("Drawdown")
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    main()
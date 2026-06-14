# from datetime import date
from database.models import Feature,Prediction, Stock, TradeModel, StrategyRun
from datetime import datetime
def save_features(
    session,
    feature_df,
    ticker
):
    rows = []
    for idx, row in feature_df.iterrows():
        rows.append(
            Feature(
                ticker=ticker,
                date=idx,
                macd=float(row["macd"]),
                adx=float(row["adx"]),
                di_plus=float(row["di_plus"]),
                di_minus=float(row["di_minus"]),
                ret_5=float(row["ret_5"]),
                volatility_20=float(row["volatility_20"]),
                volume_ratio=float(row["volume_ratio"]),
                distance_sma20=float(row["distance_sma20"]),
                target=int(row["target"])
            )
        )
    session.add_all(rows)
    session.commit()

def save_stock(session, ticker):
    stock = session.query(Stock).filter_by(
        ticker=ticker
    ).first()
    if stock is None:
        stock = Stock(
            ticker=ticker
        )
        session.add(stock)
        session.commit()
    return stock    

def save_trades(session,trades):
    trade_rows = []
    for trade in trades:
        trade_rows.append(
            TradeModel(
                ticker=trade.ticker,
                entry_date=trade.entry_date,
                exit_date=trade.exit_date,
                entry_price=float(trade.entry_price),
                exit_price=float(trade.exit_price),
                quantity=float(trade.quantity),
                pnl=float(trade.net_pnl),
                holding_days=int(trade.holding_days)
            )
        )
    session.add_all(trade_rows)
    session.commit()

def save_strategy_run(session,strategy_name,ticker,result_df):
    row = result_df.iloc[0]
    run = StrategyRun(
        strategy_name=strategy_name,
        ticker=ticker,
        total_return=float(row["total_return"]),
        sharpe=float(row["sharpe"]),
        max_drawdown=float(row["Maximum Drawdown"]),
        win_rate=float(row["win rate(in %)"]),
        created_at=datetime.now()
    )
    session.add(run)
    session.commit()

def save_predictions(session,prediction_df,ticker):
    rows = []
    for idx, row in prediction_df.iterrows():
        rows.append(
            Prediction(
                ticker=ticker,
                date=idx,
                probability_up=float(
                    row["probability_up"]
                ),
                prediction=int(
                    row["prediction"]
                )
            )
        )
    session.add_all(rows)
    session.commit()



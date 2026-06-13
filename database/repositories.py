# from datetime import date
from database.models import Feature,Prediction, Stock, TradeModel, StrategyRun

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


def get_or_create_stock(session, ticker):
    stock = session.query(Stock).filter(Stock.ticker == ticker).first()
    if stock is None:
        stock = Stock(ticker=ticker)
        session.add(stock)
        session.commit()
        session.refresh(stock)
    return stock


def save_trade(session, stock_id, strategy_name, trade):
    db_trade = TradeModel(
        stock_id=stock_id,
        strategy_name=strategy_name,
        ticker=trade.ticker,
        entry_date=trade.entry_date.date() if hasattr(trade.entry_date, "date") else trade.entry_date,
        exit_date=trade.exit_date.date() if hasattr(trade.exit_date, "date") else trade.exit_date,
        entry_price=trade.entry_price,
        exit_price=trade.exit_price,
        quantity=trade.quantity,
        entry_fee=trade.entry_fee,
        exit_fee=trade.exit_fee,
        gross_pnl=trade.gross_pnl,
        net_pnl=trade.net_pnl,
        holding_days=trade.holding_days,
    )
    session.add(db_trade)
    session.commit()


def save_strategy_run(session, stock_id, strategy_name, start_date, end_date, metrics):
    row = StrategyRun(
        stock_id=stock_id,
        strategy_name=strategy_name,
        start_date=start_date,
        end_date=end_date,
        total_return=float(metrics.get("total_return", 0)),
        annualized_return=float(metrics.get("annualized_return", 0)),
        sharpe=float(metrics.get("sharpe", 0)),
        sortino=float(metrics.get("sortino ratio", 0)),
        max_drawdown=float(metrics.get("Maximum Drawdown", 0)),
        win_rate=float(metrics.get("win rate(in %)", 0)),
        total_trades=int(metrics.get("total_trades", 0)),
    )
    session.add(row)
    session.commit()


def save_predictions(
    session,
    prediction_df,
    ticker
):

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

def save_predictions(
    session,
    prediction_df,
    ticker
):

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
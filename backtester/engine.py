import numpy as np
import pandas as pd
from .portfolio import Portfolio


class BacktestEngine:
    def __init__(
        self,
        data,
        ticker,
        initial_cash=100000,
        transaction_cost_bps=10,
        signal_col="signal",
    ):
        self.data = data.copy()
        self.ticker = ticker
        self.signal_col = signal_col
        self.portfolio = Portfolio(
            initial_cash=initial_cash,
            transaction_cost_bps=transaction_cost_bps
        )

    def run(self):
        df = self.data.copy().sort_index()

        if self.signal_col not in df.columns:
            raise ValueError(f"'{self.signal_col}' column not found in dataframe")

        df["cash"] = np.nan
        df["equity"] = np.nan
        df["position"] = 0
        df["trade_action"] = ""

        for date, row in df.iterrows():
            signal = row[self.signal_col]
            if pd.isna(signal):
                signal = 0
            signal = int(signal)

            price = float(row["Close"])

            # Buy
            if signal == 1 and self.portfolio.open_trade is None:
                opened = self.portfolio.open_position(
                    ticker=self.ticker,
                    date=date,
                    price=price,
                    side="LONG"
                )
                if opened:
                    df.at[date, "trade_action"] = "BUY"

            # Sell
            elif signal == -1 and self.portfolio.open_trade is not None:
                closed_trade = self.portfolio.close_position(date, price)
                if closed_trade is not None:
                    df.at[date, "trade_action"] = "SELL"

            equity = self.portfolio.record_equity(date, price)

            df.at[date, "cash"] = self.portfolio.cash
            df.at[date, "equity"] = equity
            df.at[date, "position"] = 0 if self.portfolio.open_trade is None else 1

        # Force close at the end if a trade is still open
        if self.portfolio.open_trade is not None:
            last_date = df.index[-1]
            last_price = float(df.iloc[-1]["Close"])
            closed_trade = self.portfolio.close_position(last_date, last_price)

            if closed_trade is not None:
                df.at[last_date, "trade_action"] = "FORCED_EXIT"
                df.at[last_date, "cash"] = self.portfolio.cash
                df.at[last_date, "equity"] = self.portfolio.cash
                df.at[last_date, "position"] = 0

        return df, self.portfolio
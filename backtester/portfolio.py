from .trade import Trade


class Portfolio:
    def __init__(self, initial_cash=100000, transaction_cost_bps=10):
        self.initial_cash = float(initial_cash)
        self.cash = float(initial_cash)
        self.transaction_cost = transaction_cost_bps / 10000.0

        self.open_trade = None
        self.closed_trades = []
        self.equity_curve = []

    def open_position(self, ticker, date, price, side="LONG"):
        if self.open_trade is not None:
            return False

        price = float(price)
        if price <= 0:
            return False

        # Spend almost all available cash, including fee
        quantity = self.cash / (price * (1 + self.transaction_cost))
        entry_fee = quantity * price * self.transaction_cost
        total_cost = quantity * price + entry_fee

        self.cash -= total_cost

        self.open_trade = Trade(
            ticker=ticker,
            entry_date=date,
            entry_price=price,
            quantity=quantity,
            side=side,
            entry_fee=entry_fee
        )
        return True

    def close_position(self, date, price):
        if self.open_trade is None:
            return None

        price = float(price)
        trade = self.open_trade

        proceeds = trade.quantity * price
        exit_fee = proceeds * self.transaction_cost

        trade.close(date, price, exit_fee=exit_fee)

        self.cash += proceeds - exit_fee
        self.closed_trades.append(trade)
        self.open_trade = None

        return trade

    def current_equity(self, current_price):
        current_price = float(current_price)

        if self.open_trade is None:
            return self.cash

        return self.cash + self.open_trade.quantity * current_price

    def record_equity(self, date, current_price):
        equity = self.current_equity(current_price)

        self.equity_curve.append(
            {
                "date": date,
                "cash": self.cash,
                "equity": equity,
                "position": 0 if self.open_trade is None else 1,
                "price": float(current_price),
            }
        )
        return equity
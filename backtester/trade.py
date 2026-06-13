from dataclasses import dataclass, asdict
from typing import Optional
import pandas as pd


@dataclass
class Trade:
    ticker: str
    entry_date: pd.Timestamp
    entry_price: float
    quantity: float
    side: str = "LONG"
    entry_fee: float = 0.0

    exit_date: Optional[pd.Timestamp] = None
    exit_price: Optional[float] = None
    exit_fee: float = 0.0

    gross_pnl: Optional[float] = None
    net_pnl: Optional[float] = None
    holding_days: Optional[int] = None

    def close(self, exit_date, exit_price, exit_fee: float = 0.0):
        self.exit_date = pd.Timestamp(exit_date)
        self.exit_price = float(exit_price)
        self.exit_fee = float(exit_fee)

        if self.side.upper() == "LONG":
            self.gross_pnl = (self.exit_price - self.entry_price) * self.quantity
        else:
            self.gross_pnl = (self.entry_price - self.exit_price) * self.quantity

        self.net_pnl = self.gross_pnl - self.entry_fee - self.exit_fee
        self.holding_days = (self.exit_date - pd.Timestamp(self.entry_date)).days

    def to_dict(self):
        return asdict(self)
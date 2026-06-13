from sqlalchemy import *

from database.db import Base

class Stock(Base):

    __tablename__ = "stocks"

    stock_id = Column(
        Integer,
        primary_key=True
    )

    ticker = Column(
        String,
        unique=True
    )

class Feature(Base):

    __tablename__ = "features"

    feature_id = Column(
        Integer,
        primary_key=True
    )

    ticker = Column(String)

    date = Column(Date)

    macd = Column(Float)

    adx = Column(Float)

    di_plus = Column(Float)

    di_minus = Column(Float)

    ret_5 = Column(Float)

    volatility_20 = Column(Float)

    volume_ratio = Column(Float)

    distance_sma20 = Column(Float)

    target = Column(Integer)

class Prediction(Base):

    __tablename__ = "predictions"

    prediction_id = Column(
        Integer,
        primary_key=True
    )

    ticker = Column(String)

    date = Column(Date)

    probability_up = Column(Float)

    prediction = Column(Integer)

class TradeModel(Base):

    __tablename__ = "trades"

    trade_id = Column(
        Integer,
        primary_key=True
    )

    ticker = Column(String)

    entry_date = Column(Date)

    exit_date = Column(Date)

    entry_price = Column(Float)

    exit_price = Column(Float)

    quantity = Column(Float)

    pnl = Column(Float)

    holding_days = Column(Integer)

class StrategyRun(Base):

    __tablename__ = "strategy_runs"

    run_id = Column(Integer, primary_key=True)

    strategy_name = Column(String)

    ticker = Column(String)

    total_return = Column(Float)

    sharpe = Column(Float)

    max_drawdown = Column(Float)

    win_rate = Column(Float)

    created_at = Column(DateTime)
        
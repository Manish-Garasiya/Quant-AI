import numpy as np
import pandas as pd


def performance(df, portfolio):
    result = pd.DataFrame(index=["Strategy Results"])

    equity = df["equity"].dropna().astype(float)
    if len(equity) < 2:
        result["total_return"] = np.nan
        result["annualized_return"] = np.nan
        result["sharpe"] = np.nan
        result["sortino ratio"] = np.nan
        result["Maximum Drawdown"] = np.nan
        result["win rate(in %)"] = np.nan
        result["profit_factor"] = np.nan
        result["total_trades"] = 0
        return result

    returns = equity.pct_change().dropna()

    # Total return
    total_return = (equity.iloc[-1] / equity.iloc[0]) - 1
    result["total_return"] = total_return

    # Annualized return / CAGR
    years = len(equity) / 252
    if years > 0:
        result["annualized_return"] = (equity.iloc[-1] / equity.iloc[0]) ** (1 / years) - 1
    else:
        result["annualized_return"] = np.nan

    # Sharpe ratio
    if returns.std() != 0:
        result["sharpe"] = np.sqrt(252) * (returns.mean() / returns.std())
    else:
        result["sharpe"] = np.nan

    # Sortino ratio
    risk_free_rate = 0.04 / 252
    downside_returns = returns[returns < 0]
    downside_std = downside_returns.std()

    if pd.notna(downside_std) and downside_std != 0:
        result["sortino ratio"] = np.sqrt(252) * (returns.mean() - risk_free_rate) / downside_std
    else:
        result["sortino ratio"] = np.nan

    # Drawdown
    rolling_max = equity.cummax()
    drawdown = (equity / rolling_max) - 1
    result["Maximum Drawdown"] = drawdown.min()

    df.loc[equity.index, "drawdown"] = drawdown

    # Trade metrics
    trades = pd.DataFrame([t.to_dict() for t in portfolio.closed_trades])

    result["total_trades"] = len(trades)

    if not trades.empty and "net_pnl" in trades.columns:
        wins = trades[trades["net_pnl"] > 0]
        losses = trades[trades["net_pnl"] < 0]

        result["win rate(in %)"] = (len(wins) / len(trades)) * 100

        if len(losses) > 0:
            profit_factor = wins["net_pnl"].sum() / abs(losses["net_pnl"].sum())
        else:
            profit_factor = np.inf

        result["profit_factor"] = profit_factor
        result["avg_profit(in ₹)"] = wins["net_pnl"].mean() if len(wins) > 0 else np.nan
        result["avg_loss(in ₹)"] = abs(losses["net_pnl"].mean()) if len(losses) > 0 else np.nan
        result["max_profit(in ₹)"] = wins["net_pnl"].max() if len(wins) > 0 else np.nan
        result["max_loss(in ₹)"] = abs(losses["net_pnl"].min()) if len(losses) > 0 else np.nan
        result["avg_holding_days"] = trades["holding_days"].mean()
    else:
        result["win rate(in %)"] = np.nan
        result["profit_factor"] = np.nan
        result["avg_profit(in ₹)"] = np.nan
        result["avg_loss(in ₹)"] = np.nan
        result["max_profit(in ₹)"] = np.nan
        result["max_loss(in ₹)"] = np.nan
        result["avg_holding_days"] = np.nan

    return result
import pandas as pd
import numpy as np
   

def MACD(close):
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    return macd


def calculate_DIs_and_ADX(high, low, close, period=14):

    n = len(close)

    true_range = [high.iloc[0] - low.iloc[0]]
    smoothed_tr = [true_range[0]]

    dm_plus = [0] * n
    dm_minus = [0] * n

    smooth_dm_plus = [0]
    smooth_dm_minus = [0]

    di_plus = pd.Series(index=close.index, dtype=float)
    di_minus = pd.Series(index=close.index, dtype=float)
    adx = pd.Series(index=close.index, dtype=float)

    di_plus.iloc[0] = 0
    di_minus.iloc[0] = 0
    adx.iloc[0] = 0

    dx = [0]

    for i in range(1, n):

        h = high.iloc[i]
        l = low.iloc[i]
        prev_close = close.iloc[i-1]

        tr = max(
            h - l,
            abs(h - prev_close),
            abs(l - prev_close)
        )
        true_range.append(tr)

        smoothed_tr.append(
            smoothed_tr[i-1] - (smoothed_tr[i-1] / period) + tr
        )

        upmove = h - high.iloc[i-1]
        downmove = low.iloc[i-1] - l

        if upmove > downmove and upmove > 0:
            dm_plus[i] = upmove
        elif downmove > upmove and downmove > 0:
            dm_minus[i] = downmove

        smooth_dm_plus.append(
            smooth_dm_plus[i-1] - (smooth_dm_plus[i-1] / period) + dm_plus[i]
        )

        smooth_dm_minus.append(
            smooth_dm_minus[i-1] - (smooth_dm_minus[i-1] / period) + dm_minus[i]
        )

        # DI
        if smoothed_tr[i] != 0:
            di_p = 100 * (smooth_dm_plus[i] / smoothed_tr[i])
            di_m = 100 * (smooth_dm_minus[i] / smoothed_tr[i])
        else:
            di_p = 0
            di_m = 0

        di_plus.iloc[i] = di_p
        di_minus.iloc[i] = di_m

        if di_p + di_m != 0:
            dx_val = 100 * abs(di_p - di_m) / (di_p + di_m)
        else:
            dx_val = 0

        dx.append(dx_val)

        adx.iloc[i] = (
            adx.iloc[i-1] - (adx.iloc[i-1] / period) + dx_val
        )

    return di_plus, di_minus, adx

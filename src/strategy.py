"""
Bollinger Bands signal generation with fixed stop loss.

Entry: Close crosses above (Middle + x·σ) from below,
       AND Open[T+1] > Low[T] (skip trade if not met).
Exit:  Close crosses below (Middle + y·σ) from above, OR
       Close falls below the stop loss (Low of signal day T).

Stop loss is fixed at Low[T] where T is the day the entry signal fires.
Entry executes at T+1 open.
"""

import pandas as pd


def generate_signals(close: pd.Series, x: int, y: int, window: int = 20,
                     low: pd.Series | None = None,
                     open_price: pd.Series | None = None) -> dict:
    """
    Generate entry/exit boolean signals from BB crossover with stop loss.

    Parameters
    ----------
    close      : pd.Series — daily close prices
    x          : int — entry band multiplier
    y          : int — exit band multiplier
    window     : int — moving average window length
    low        : pd.Series | None — daily low prices (for stop loss)
    open_price : pd.Series | None — daily open prices (for entry filter)

    Returns dict with keys:
        entries, exits, bb_mid, bb_std, entry_band, exit_band,
        bb_upper, bb_lower, stop_loss_levels
    """
    bb_mid = close.rolling(window).mean()
    bb_std = close.rolling(window).std(ddof=0)
    entry_band = bb_mid + x * bb_std
    exit_band = bb_mid + y * bb_std
    bb_upper = bb_mid + 2 * bb_std
    bb_lower = bb_mid - 2 * bb_std

    n = len(close)
    entries = pd.Series(False, index=close.index)
    exits = pd.Series(False, index=close.index)
    # Track stop loss level for each bar (NaN when not in position)
    stop_loss_levels = pd.Series(float("nan"), index=close.index)
    in_position = False
    current_stop = None

    for i in range(1, n):
        if pd.isna(bb_mid.iloc[i]):
            continue
        prev_c = close.iloc[i - 1]
        curr_c = close.iloc[i]
        eb = entry_band.iloc[i]
        xb = exit_band.iloc[i]

        if not in_position:
            # Entry signal: close crosses above entry band
            if prev_c < eb and curr_c >= eb:
                # Additional filter: Open[T+1] > Low[T]
                # T = signal day = i, T+1 = i+1
                if i + 1 < n and open_price is not None and low is not None:
                    next_open = float(open_price.iloc[i + 1])
                    signal_low = float(low.iloc[i])
                    if next_open <= signal_low:
                        # Skip this trade — gap-down at open
                        continue
                entries.iloc[i] = True
                in_position = True
                # Stop loss = Low of signal day (day T = today, i)
                if low is not None:
                    current_stop = float(low.iloc[i])
                else:
                    current_stop = None
        else:
            # Check exit conditions:
            # 1) Close crosses below exit band
            band_exit = prev_c > xb and curr_c <= xb
            # 2) Close falls below stop loss
            stop_exit = current_stop is not None and curr_c <= current_stop

            if band_exit or stop_exit:
                exits.iloc[i] = True
                in_position = False
                current_stop = None

        # Record current stop loss level if in position
        if in_position and current_stop is not None:
            stop_loss_levels.iloc[i] = current_stop

    return {
        "entries": entries,
        "exits": exits,
        "bb_mid": bb_mid,
        "bb_std": bb_std,
        "entry_band": entry_band,
        "exit_band": exit_band,
        "bb_upper": bb_upper,
        "bb_lower": bb_lower,
        "stop_loss_levels": stop_loss_levels,
    }

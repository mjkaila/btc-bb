"""
VectorBT portfolio construction.

Executes entries and exits at next-day open. Long-only, fully invested or out.
No leverage, no shorting. Initial capital: $100,000.
"""

import pandas as pd
import vectorbt as vbt


def run_backtest(
    df: pd.DataFrame,
    entries: pd.Series,
    exits: pd.Series,
    cost_pct: float = 0.0,
    init_cash: float = 100_000,
) -> tuple:
    """
    Run VBT backtest with next-day-open execution.

    Returns: (pf, open_price, close_price)
    """
    date_index = pd.to_datetime(df["Date"].values)
    open_price = pd.Series(df["Open"].values, index=date_index, name="Open")
    close_price = pd.Series(df["Close"].values, index=date_index, name="Close")

    entries_shifted = entries.shift(1).infer_objects(copy=False).fillna(False).astype(bool)
    exits_shifted = exits.shift(1).infer_objects(copy=False).fillna(False).astype(bool)

    pf = vbt.Portfolio.from_signals(
        close=open_price,
        entries=entries_shifted,
        exits=exits_shifted,
        freq="1D",
        init_cash=init_cash,
        size=1.0,
        size_type="percent",
        fees=cost_pct / 100.0,
        direction="longonly",
    )
    return pf, open_price, close_price

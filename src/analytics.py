"""
Metrics computation and trade extraction.

Uses VBT pf.stats() as the primary source. CAGR from QuantStats,
Alpha/Beta from empyrical, W/L Ratio and E[R] are custom-calculated.
"""

import math
import numpy as np
import pandas as pd
import empyrical
import quantstats as qs

PERIODS = 365  # crypto annualisation


def _safe(v, decimals=2) -> float:
    if isinstance(v, (np.floating, np.integer)):
        v = float(v)
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return 0.0
    return round(v, decimals)


def compute_metrics(pf, close_price: pd.Series) -> dict:
    """Full metrics for a single strategy."""
    stats = pf.stats()
    strat_returns = pf.returns()
    bh_returns = close_price.pct_change().fillna(0.0)
    bh_returns.name = "Benchmark"

    trades_readable = pf.trades.records_readable
    num_trades = int(pf.trades.count())

    # VBT native
    total_return = _safe(float(stats.get("Total Return [%]", 0.0)))
    benchmark_return = _safe(float(stats.get("Benchmark Return [%]", 0.0)))
    max_dd = _safe(float(stats.get("Max Drawdown [%]", 0.0)))
    sharpe = _safe(float(stats.get("Sharpe Ratio", 0.0)), 3)
    calmar = _safe(float(stats.get("Calmar Ratio", 0.0)), 3)
    sortino = _safe(float(stats.get("Sortino Ratio", 0.0)), 3)
    profit_factor = _safe(float(stats.get("Profit Factor", 0.0)), 3)
    win_rate = _safe(float(stats.get("Win Rate [%]", 0.0)), 1)

    # QuantStats
    cagr = _safe(float(qs.stats.cagr(strat_returns, rf=0.0, periods=PERIODS)) * 100)

    # Empyrical
    alpha = _safe(float(empyrical.alpha(strat_returns, bh_returns, period="daily")) * 100)
    beta = _safe(float(empyrical.beta(strat_returns, bh_returns)), 3)

    # Custom
    if num_trades > 0:
        winners = trades_readable[trades_readable["Return"] > 0]
        losers = trades_readable[trades_readable["Return"] <= 0]
        avg_win_pct = float(winners["Return"].mean()) * 100 if len(winners) > 0 else 0.0
        avg_loss_pct = float(losers["Return"].mean()) * 100 if len(losers) > 0 else 0.0
        wl_ratio = abs(avg_win_pct) / abs(avg_loss_pct) if abs(avg_loss_pct) > 1e-10 else (
            9999.0 if avg_win_pct > 0 else 0.0)
        p_win = len(winners) / num_trades
        p_loss = len(losers) / num_trades
        expected_return = p_win * avg_win_pct + p_loss * avg_loss_pct
    else:
        wl_ratio = 0.0
        expected_return = 0.0

    return {
        "strategy_return": total_return,
        "benchmark_return": benchmark_return,
        "max_dd": max_dd,
        "sharpe": sharpe,
        "calmar": calmar,
        "sortino": sortino,
        "profit_factor": profit_factor,
        "win_rate": win_rate,
        "num_trades": num_trades,
        "cagr": cagr,
        "alpha": alpha,
        "beta": beta,
        "wl_ratio": _safe(wl_ratio),
        "expected_return": _safe(expected_return),
    }


def extract_trades(pf) -> list[dict]:
    """Extract trade log from VBT portfolio."""
    trades_df = pf.trades.records_readable
    trade_list = []
    for _, t in trades_df.iterrows():
        trade_list.append({
            "trade": int(t["Exit Trade Id"]) + 1,
            "entry_date": str(t["Entry Timestamp"])[:10],
            "entry_price": round(float(t["Avg Entry Price"]), 2),
            "exit_date": str(t["Exit Timestamp"])[:10],
            "exit_price": round(float(t["Avg Exit Price"]), 2),
            "pnl": round(float(t["PnL"]), 2),
            "return_pct": round(float(t["Return"]) * 100, 2),
            "status": str(t["Status"]),
        })
    return trade_list


def build_chart_data(df, pf, close_price, open_price, entries, exits, signals, low_price=None) -> dict:
    """Build all arrays needed for Plotly charts."""
    date_index = pd.to_datetime(df["Date"].values)
    dates = [d.strftime("%Y-%m-%d") for d in date_index]
    strat_equity = pf.value()
    bh_equity = (1 + close_price.pct_change().fillna(0)).cumprod() * pf.init_cash
    strat_dd = (strat_equity / strat_equity.cummax() - 1) * 100
    bh_dd = (bh_equity / bh_equity.cummax() - 1) * 100

    entries_shifted = entries.shift(1).infer_objects(copy=False).fillna(False).astype(bool)
    exits_shifted = exits.shift(1).infer_objects(copy=False).fillna(False).astype(bool)

    def to_list(s, d=2):
        vals = s.values if hasattr(s, "values") else s
        out = []
        for v in vals:
            if isinstance(v, (np.floating, np.integer)):
                v = float(v)
            try:
                fv = float(v)
                out.append(None if (math.isnan(fv) or math.isinf(fv)) else round(fv, d))
            except (TypeError, ValueError):
                out.append(None)
        return out

    return {
        "dates": dates,
        "open_price": to_list(open_price),
        "high": to_list(pd.Series(df["High"].values, index=date_index)),
        "low": to_list(pd.Series(df["Low"].values, index=date_index)),
        "close": to_list(close_price),
        "volume": [int(v) for v in df["Volume"].values],
        "entry_band": to_list(signals["entry_band"]),
        "exit_band": to_list(signals["exit_band"]),
        "bb_mid": to_list(signals["bb_mid"]),
        "bb_upper": to_list(signals["bb_upper"]),
        "bb_lower": to_list(signals["bb_lower"]),
        "strat_equity": to_list(strat_equity, 2),
        "bh_equity": to_list(bh_equity, 2),
        "strat_dd": to_list(strat_dd),
        "bh_dd": to_list(bh_dd),
        "entry_indices": [i for i, v in enumerate(entries_shifted.values) if v],
        "exit_indices": [i for i, v in enumerate(exits_shifted.values) if v],
        "stop_loss_levels": to_list(signals.get("stop_loss_levels", pd.Series(dtype=float))),
    }

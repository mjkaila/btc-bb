#!/usr/bin/env python3
"""
Pre-compute all backtesting results and save to pickle.

Run this once locally:
    python precompute.py

Outputs: data/precomputed.pkl
"""

import pickle
import sys
import time
from pathlib import Path

import pandas as pd

# Ensure src is importable
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.data import load_csv, get_data_info
from src.strategy import generate_signals
from src.backtesting import run_backtest
from src.analytics import compute_metrics, extract_trades, build_chart_data

# ── Grid parameters ──
X_MIN, X_MAX = -2, 2
Y_MIN, Y_MAX = -2, 2
WIN_MIN, WIN_MAX, WIN_STEP = 10, 50, 10
COST_PCT = 0.0

OUT_PATH = Path(__file__).resolve().parent / "data" / "precomputed.pkl"


def main():
    t0 = time.time()

    print("Loading static CSV...")
    df = load_csv()
    data_info = get_data_info(df)
    print(f"  {data_info['rows']} bars, {data_info['start']} → {data_info['end']}")

    close = pd.Series(
        df["Close"].values,
        index=pd.to_datetime(df["Date"].values),
        name="Close",
    )
    low = pd.Series(
        df["Low"].values,
        index=pd.to_datetime(df["Date"].values),
        name="Low",
    )
    open_s = pd.Series(
        df["Open"].values,
        index=pd.to_datetime(df["Date"].values),
        name="Open",
    )

    windows = list(range(WIN_MIN, WIN_MAX + 1, WIN_STEP))
    total = len(windows) * (X_MAX - X_MIN + 1) * (Y_MAX - Y_MIN + 1)
    print(f"Running grid search: {total} combinations...")

    # Store full detail for every combination
    all_strategies = {}  # key: (x, y, window) → dict
    grid_results = []    # list of metric dicts for table/heatmap

    done = 0
    for win in windows:
        for x_val in range(X_MIN, X_MAX + 1):
            for y_val in range(Y_MIN, Y_MAX + 1):
                signals = generate_signals(close, x=x_val, y=y_val, window=win,
                                           low=low, open_price=open_s)
                pf, open_price, close_price = run_backtest(
                    df, signals["entries"], signals["exits"], cost_pct=COST_PCT,
                )
                metrics = compute_metrics(pf, close_price)
                trades = extract_trades(pf)
                chart_data = build_chart_data(
                    df, pf, close_price, open_price,
                    signals["entries"], signals["exits"], signals,
                )

                key = (x_val, y_val, win)
                all_strategies[key] = {
                    "metrics": metrics,
                    "trades": trades,
                    "chart_data": chart_data,
                }

                grid_row = {**metrics, "x": x_val, "y": y_val, "window": win}
                grid_results.append(grid_row)

                done += 1
                if done % 25 == 0:
                    elapsed = time.time() - t0
                    print(f"  {done}/{total}  ({elapsed:.0f}s)")

    # Find best by Calmar
    best_row = max(grid_results, key=lambda r: r["calmar"])
    best_key = (int(best_row["x"]), int(best_row["y"]), int(best_row["window"]))
    print(f"Best: x={best_key[0]}, y={best_key[1]}, window={best_key[2]}, "
          f"Calmar={best_row['calmar']}")

    output = {
        "data_info": data_info,
        "grid_results": grid_results,
        "all_strategies": all_strategies,
        "best_key": best_key,
        "params": {
            "x_min": X_MIN, "x_max": X_MAX,
            "y_min": Y_MIN, "y_max": Y_MAX,
            "win_min": WIN_MIN, "win_max": WIN_MAX, "win_step": WIN_STEP,
            "cost_pct": COST_PCT,
        },
    }

    with open(OUT_PATH, "wb") as f:
        pickle.dump(output, f, protocol=pickle.HIGHEST_PROTOCOL)

    size_mb = OUT_PATH.stat().st_size / (1024 * 1024)
    elapsed = time.time() - t0
    print(f"Saved to {OUT_PATH} ({size_mb:.1f} MB) in {elapsed:.0f}s")


if __name__ == "__main__":
    main()

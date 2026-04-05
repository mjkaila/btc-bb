"""
Static CSV loader for BTC-USD data.
No yfinance calls, no DuckDB — just reads the bundled CSV.
"""

from pathlib import Path
import pandas as pd

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "btc_usd_2021_2025.csv"


def load_csv() -> pd.DataFrame:
    """Load BTC-USD OHLCV from the bundled static CSV."""
    df = pd.read_csv(CSV_PATH)
    df["Date"] = pd.to_datetime(df["Date"])
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        df[col] = df[col].astype(float)
    return df.sort_values("Date").reset_index(drop=True)


def get_data_info(df: pd.DataFrame) -> dict:
    return {
        "symbol": "BTC-USD",
        "rows": len(df),
        "start": df["Date"].iloc[0].strftime("%Y-%m-%d"),
        "end": df["Date"].iloc[-1].strftime("%Y-%m-%d"),
    }

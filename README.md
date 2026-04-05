# Kaila — Bitcoin Breakout Strategy

A Streamlit portfolio demo app showcasing a systematic mean-reversion backtester on BTC-USD using Bollinger Bands.

## Features

- **125 pre-computed strategies** across BB window, buy-signal (x), and sell-signal (y) parameters
- **Interactive heatmap** — click any cell to load that strategy's detailed analysis
- **Strategy table** — sortable, with bidirectional highlight sync to heatmap
- **Detailed analysis** — equity curve, drawdown, trade markers on price chart
- **Trade log** — click any trade row to zoom into a single-trade view
- **KPI dashboard** — Strategy Return, Alpha, CAGR, Sharpe, Sortino, Calmar, and more
- **Instant load** — all results are pre-computed; no runtime computation or API calls

## Quick Start (Local)

```bash
# 1. Clone and enter the project
cd btc-bb-app

# 2. Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Deploy on Streamlit Cloud

1. Push this repo to GitHub (public or private).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**, select the repo, branch, and set `app.py` as the main file.
4. Click **Deploy**. Streamlit Cloud installs from `requirements.txt` automatically.

> **Note:** The `data/precomputed.pkl` file (~25 MB) is included in the repo. Streamlit Cloud's default resource limits handle this comfortably.

## Regenerating Pre-computed Data

If you modify the strategy logic or parameters, regenerate the pickle:

```bash
# Requires additional libraries for the computation step
pip install vectorbt quantstats empyrical yfinance
python precompute.py
```

This overwrites `data/precomputed.pkl`. The runtime app (`app.py`) only needs the lightweight dependencies in `requirements.txt`.

## Project Structure

```
btc-bb-app/
├── app.py                  # Main Streamlit application
├── faq.md                  # Editable FAQ content (Q&A format)
├── precompute.py           # Script to regenerate precomputed.pkl
├── requirements.txt        # Runtime dependencies (lightweight)
├── README.md
├── .streamlit/
│   └── config.toml         # Theme configuration (navy + gold)
├── data/
│   ├── btc_usd_2021_2025.csv   # Static BTC-USD daily data (2021–2025)
│   └── precomputed.pkl          # Pre-computed results for 125 strategies
└── src/
    ├── __init__.py
    ├── data.py              # Data loading utilities
    ├── strategy.py          # Bollinger Band signal generation
    ├── backtesting.py       # VectorBT portfolio construction
    └── analytics.py         # Metrics calculation (CAGR, alpha, beta, etc.)
```

## Tech Stack

- **Streamlit** — UI framework
- **Plotly** — Interactive charts
- **Pandas / NumPy** — Data manipulation
- **VectorBT** — Backtesting engine (precompute only)
- **QuantStats** — CAGR calculation (precompute only)
- **empyrical** — Alpha/Beta CAPM (precompute only)

## Data

BTC-USD daily OHLCV from Yahoo Finance, 2021-01-01 to 2025-12-31 (1,826 bars). Bundled as a static CSV — no live API calls.

---

*Past performance is not indicative of future results.*

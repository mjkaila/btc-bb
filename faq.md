## What's the purpose of this application?

The application presents a systematic, rules-based trading strategy inspired by Bollinger Bands. The purpose is to explore whether active, rules-based trading can improve risk-adjusted returns compared to a simple buy-and-hold approach.

**Key Characteristics**

- Long-only, fully invested or fully out (no partial exposures).
- No leverage.
- Initial capital: $100,000.
- Benchmark asset: Bitcoin (buy-and-hold)
- Not investment advice.

**Data**

- Daily BTC-USD OHLCV data sourced from Yahoo Finance.
- 1,826 daily bars from 2021-01-01 to 2025-12-31.

## What's the Strategy?

The trading strategy is based on Bollinger Bands, volatility bands built around a moving average. The core idea is to participate in upward market moves while avoiding prolonged drawdowns.

Standard Bollinger Bands use a 20-day simple moving average of close prices as the Middle. Upper and Lower Bands are defined as Middle ± 2 standard deviations.

The application has parameters for the entry *(x)* and exit *(y)* multipliers as well as the moving average window length in days *(z)*.

- Middle μ = Simple Moving Average of Close Prices of Last *z* Days
- Entry Band = μ + *x* · σ
- Exit Band = μ + *y* · σ

The user can explore which strategy (the combination of *x*, *y* , and *z* parameters) has the best performance. 

The user can optimize for various performance metrics such as annualized returns (CAGR), risk-adjusted returns (Calmar Ratio), or Expected Return per Trade.

&nbsp;

**Entry & Exit Criteria**

Buy signal (day T): 1. Close price crosses above the entry band and 2. Open price of the next day (T+1) is above the Low price of day T.

Sell signal (day T): 1. Close price crosses below the exit band or 2. Close price falls below the stop loss.

Execution (day T+1): Both entries and exits execute at the next-day open price, avoiding look-ahead bias.

Stop loss: When entering a trade on day T+1, the stop loss is set to the low price of day T. The stop loss remains fixed for the duration of the trade.


## What's Strategy Heatmap?

Grid of all strategy variants for one window length. Each cell shows a performance metric for a unique (x, y) combination. Click any cell to select that strategy.

Use the Performance Metric dropdown to switch between different metrics (e.g. Calmar Ratio, Strategy Return, Max Drawdown). Use the Window (z) dropdown to view heatmaps for different moving average window lengths.

## What's Equity Curve?

Growth of the portfolio indexed to start = 1. Index = 10 means the final equity is 10× compared to start equity. Index = 0 means all equity would have been lost.

The solid gold line represents the selected strategy. The dotted grey line represents the buy-and-hold benchmark (BTC-USD). Comparing the two lines reveals whether active trading outperformed simply holding the asset.

## What's Drawdown?

Peak-to-trough decline in portfolio equity, expressed as a percentage. Drawdown = −20 means the equity has dropped 20% from its peak.

The red area represents the selected strategy's drawdown over time. The dotted grey line shows the buy-and-hold benchmark's drawdown. Shallower drawdowns indicate better capital preservation during adverse market conditions.

## What's Strategy Table?

All 125 strategy variants ranked by Calmar Ratio. Click any row to select that strategy. The heatmap, equity curve, and drawdown chart update accordingly.

The application evaluates strategy variants by combining 5 moving average window lengths with 5 entry and 5 exit thresholds. In total, 5 × 5 × 5 = 125 strategy variants (x, y, z parameter combinations) are tested.

By default, the application displays the results of best-performing strategy as measured by the Calmar Ratio (a measure of risk-adjusted returns).

## What do the performance metrics mean?

**Strategy Return (%)**

Definition: Compounded total return of the strategy (2021-2025).

Example: 500% means $100k grew to $600k.

Formula: (Final Equity / Initial Equity − 1) × 100

&nbsp;

**Benchmark Return (%)**

Definition: Compounded total return of the benchmark asset (2021-2025).

Example: 197.9% means the value of Bitcoin nearly tripled.

Formula: (Final Price / Initial Price − 1) × 100

&nbsp;

**Beta**

Definition: Sensitivity of strategy returns to benchmark returns. Measures how much the strategy moves when the benchmark moves.

Example: Beta = 0.5 means when Bitcoin moves 1%, the strategy tends to move 0.5%.

Formula: β = Cov(R_strategy, R_benchmark) / Var(R_benchmark)

&nbsp;

**Alpha**

Definition: Annualized excess return unexplained by benchmark exposure. Measures the strategy's value-add over passive benchmark exposure.

Example: Alpha = 0.48 means 48% annualized excess return.

Formula: α = R_strategy − [R_f + β × (R_benchmark − R_f)], annualized

&nbsp;

**CAGR (%)**

Definition: Compounded Annual Growth Rate, or, annualized geometric growth rate of the portfolio.

Example: CAGR = 62.8% means the portfolio grew at 62.8% per year on average.

Formula: (Final Equity / Initial Equity)^(1/years) − 1

&nbsp;

**Max Drawdown (%)**

Definition: Worst peak-to-trough decline in portfolio equity during the backtest period (2021-2025).

Example: Max DD = 35.3 means the portfolio fell 35.3% from its highest point.

Formula: Max over t of (Peak_Equity_t − Equity_t) / Peak_Equity_t × 100

&nbsp;

**Calmar Ratio**

Definition: Risk-adjusted return ratio. Higher values indicate better return per unit of drawdown risk.

Example: Calmar = 1.78 means the annual return is 1.78× the max drawdown.

Formula: CAGR / |Max Drawdown|

&nbsp;

**Trades**

Definition: Total number of completed round-trip trades over the backtest period (2021-2025).

Example: Trades = 106 means 106 buy-then-sell cycles.

Formula: Count of all closed positions

&nbsp;

**Win Rate (%)**

Definition: Percentage of trades with positive return.

Example: Win Rate = 57.5% means 57.5 out of 100 trades were profitable.

Formula: Winning Trades / Total Trades × 100

&nbsp;

**Win/Loss Ratio**

Definition: Ratio of average winning return to average losing return.

Example: Win/Loss = 1.94 means average winners are 1.94× larger than average losers.

Formula: |Average Win %| / |Average Loss %|

&nbsp;

**Profit Factor**

Definition: Ratio of gross profit to gross loss in dollar terms.

Example: Profit Factor = 2.31 means gross profits are 2.31× gross losses.

Formula: Gross Profit ($) / Gross Loss ($)

&nbsp;

**E[R] per Trade (%)**

Definition: Expected Return per Trade.

Example: E[R] = 2.8% means each trade is expected to return 2.8% on average.

Formula: (Win Rate × Avg Win %) + (Loss Rate × Avg Loss %)
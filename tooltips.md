## Strategy

Fixed strategy number, sorted by (x, y, z) ascending.

## Buy (x)

Entry band multiplier. Determines how far above the moving average the price must cross to trigger a buy signal.

## Sell (y)

Exit band multiplier. Determines how far above the moving average the price must fall below to trigger a sell signal.

## Window (z)

Moving average window length in days. Controls the lookback period for computing the mean and standard deviation.

## Strategy Return %

Compounded total return of the strategy over the backtest period (2021–2025).

## Benchmark Return %

Compounded total return of the benchmark over the backtest period (2021–2025).

## Beta

Sensitivity of strategy returns to benchmark returns. Measures how much the strategy moves when the benchmark moves.

## Alpha

Annualized excess return unexplained by benchmark exposure. Measures the strategy's value-add over passive market exposure.

## CAGR %

Compounded Annual Growth Rate. Annualized geometric growth rate of the portfolio.

## Max Drawdown %

Worst peak-to-trough decline in portfolio equity during the backtest period.

## Calmar Ratio

Risk-adjusted return ratio. Higher values indicate better return per unit of drawdown risk.

## Trades

Total number of completed round-trip trades over the backtest period.

## Win %

Percentage of trades with positive return.

## Win/Loss Ratio

Ratio of average winning return to average losing return.

## Profit Factor

Ratio of gross profit to gross loss in dollar terms.

## E[R] per Trade %

Probability-weighted expected return per trade.

## Strategy Heatmap

Compare strategies by performance metrics. There are 5 values for x, y, and z, totaling 5*5*5=125 strategies. Click a cell to select a strategy and update the visuals.

## Equity Curve

Growth of the portfolio indexed to start from 1. Index = 10 means the final equity is 10x compared to the initial equity.

## Drawdown

Peak-to-trough decline in portfolio equity. Drawdown = -20 means the portfolio equity has dropped by 20% from its peak.

## Strategy Table

Compare strategies by performance metrics. There are 5 values for x, y, and z, totaling 5*5*5=125 strategies. Click a checkbox to select a strategy and update the visuals.

## Selected Strategy

Strategy buys when price crosses above Entry Band = μ + x · σ.
Strategy sells when price crosses below Exit Band = μ + y · σ.
μ = Simple Moving Average of close prices over last z days.
σ = Standard Deviation of close prices over last z days.
See further details in FAQ.

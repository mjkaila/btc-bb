## Key takeaways

**Best strategy:** Strategy #33 — shown as default and selected by highest Calmar Ratio over the backtest period (2021-2025) (see Strategy Heatmap or Table).

**Return vs benchmark:** Strategy total return 768.5% vs. buy-and-hold Bitcoin 197.9% over the same period (see Strategy Table).

**Risk:** Strategy maximum drawdown 34.5% vs. buy-and-hold Bitcoin 76.6% (see Drawndown chart).

The "best" strategy depends on user preferences. E.g, if a drawdown of 34.5% was too steep, Strategy #125 (second highest Calmar Ratio) would offer a maximum drawdown of 18.7%. As the tradeoff, strategy return would drop to 196.8% (vs. 768.5%).

The user can explore 125 strategy variants in the app using various *(x,y,z)* parameter combinations and KPIs.

## What's the purpose of this application?

The application presents a systematic, rules-based trading strategy. The purpose is to explore whether active, rules-based trading can improve risk-adjusted returns compared to a simple buy-and-hold approach. 

The app is developed using agentic AI tools (Perplexity Computer and Cursor).

## What's the trading strategy?

The core idea is to participate in upward market moves while avoiding prolonged drawdowns.

**Bollinger Bands**

The strategy is inspired by Bollinger Bands, volatility bands built around a moving average. Standard Bollinger Bands use a 20-day simple moving average of close prices as the Middle. Upper and Lower Bands are defined as Middle ± 2 standard deviations.

The application has parameters for the entry *(x)* and exit *(y)* band multipliers as well as the moving average window length in days *(z)*.

- Rolling mean: $\mu_t$ over window $z$ days.
- Rolling standard deviation: $\sigma_t$ over window $z$ days.
- Entry band: $\mu_t + x\sigma_t$
- Exit band: $\mu_t + y\sigma_t$

**Entry & Exit Criteria**

Buy signal (day T): 

* Close price crosses above the entry band and
* Open price of the next day (T+1) is above the low price.

Sell signal (day T): 

* Close price crosses below the exit band or
* Close price falls below the stop loss.

Execution (day T+1):

* Both entries and exits execute at the next-day open price, avoiding look-ahead bias.

Stop loss:

* When entering the trade at the open of day T+1, the stop loss is set to the low of previous day T. The stop loss remains fixed for the duration of trade.

&nbsp;

## What do the KPIs (risk and performance metrics) mean?

**Risk and Performance Analysis**

The user can explore various KPIs on the Strategies and Trades tabs.

There are 125 strategy variants, ie., combinations of *x*, *y*, and *z* parameters. 

*x*, *y*, and *z* each can get 5 values, totaling 5 * 5 * 5 = 125 strategies.

The user can optimize for various KPIs such as annualized returns (CAGR), risk-adjusted returns (Calmar Ratio), and Expected Return per Trade according to her preferences, e.g., risk tolerance.

&nbsp;  

**Strategy Return (%)**

Definition: Compounded total return of the strategy (2021-2025).

Example: 500% means starting equity of 100,000 USD grew to 600,000 USD.

$R_{\text{strategy}}(\%) = \left(\frac{V_T}{V_0} - 1\right)\times 100$

&nbsp;

**Benchmark Return (%)**

Definition: Compounded total return of Bitcoin (2021-2025).

Example: 197.9% means the value of Bitcoin nearly tripled.

$R_{\text{benchmark}}(\%) = \left(\frac{P_T}{P_0} - 1\right)\times 100$

&nbsp;

**Beta**

Definition: Sensitivity of strategy returns to benchmark returns. Measures how much the strategy moves when the benchmark moves.

Example: Beta = 0.5 means when Bitcoin moves 1%, the strategy tends to move 0.5%.

$\beta = \frac{\operatorname{Cov}(r_s, r_b)}{\operatorname{Var}(r_b)}$

&nbsp;

**Alpha**

Definition: Annualized excess return unexplained by benchmark exposure. Measures the strategy's value-add over passive benchmark exposure.

Example: Alpha = 0.48 means 48% annualized excess return.

$\alpha_{\text{ann}} = \left(1 + \overline{(r_s-r_f)-\beta(r_b-r_f)}\right)^N - 1$

&nbsp;

**CAGR (%)**

Definition: Compounded Annual Growth Rate, ie., annualized geometric growth rate of the portfolio.

Example: CAGR = 62.8% means the portfolio grew at 62.8% per year on average.

$\operatorname{CAGR}(\%) = \left[\left(\frac{V_T}{V_0}\right)^{1/Y} - 1\right]\times 100$

&nbsp;

**Max Drawdown (%)**

Definition: Worst peak-to-trough decline in portfolio equity (2021-2025).

Example: Max DD = 35.3 means the portfolio fell 35.3% from its highest point.

$\operatorname{MDD}(\%) = \min_t\left(\frac{V_t - \max_{\tau \le t}V_{\tau}}{\max_{\tau \le t}V_{\tau}}\right)\times 100$

&nbsp;

**Calmar Ratio**

Definition: Risk-adjusted return ratio. Higher values indicate better return per unit of drawdown risk.

Example: Calmar = 1.78 means the annual return is 1.78× the max drawdown.

$\operatorname{Calmar} = \frac{\operatorname{CAGR}}{|\operatorname{MDD}|}$

&nbsp;

**Trades**

Definition: Total number of completed round-trip trades (2021-2025).

Example: Trades = 106 means 106 buy-then-sell cycles.

$N_{\text{trades}} = \sum_{i=1}^{n}\mathbf{1}_{\{\text{trade } i \text{ closed}\}}$

&nbsp;

**Win Rate (%)**

Definition: Percentage of trades with positive return.

Example: Win Rate = 57.5% means 57.5 out of 100 trades were profitable.

$\operatorname{WinRate}(\%) = \frac{N_{\text{wins}}}{N_{\text{trades}}}\times 100$

&nbsp;

**Win/Loss Ratio**

Definition: Ratio of average winning return to average losing return.

Example: Win/Loss = 1.94 means average winners are 1.94× larger than average losers.

$\operatorname{W/L} = \frac{|\overline{r}_{\text{win}}|}{|\overline{r}_{\text{loss}}|}$

&nbsp;

**Profit Factor**

Definition: Ratio of gross profit to gross loss in dollar terms.

Example: Profit Factor = 2.31 means gross profits are 2.31 times gross losses (same currency terms).

$\operatorname{PF} = \frac{\sum \text{Profit}_i^{+}}{\left|\sum \text{Loss}_j^{-}\right|}$

&nbsp;

**E[R] per Trade (%)**

Definition: Expected Return per Trade.

Example: E[R] = 2.8% means each trade is expected to return 2.8% on average.

$\mathbb{E}[R](\%) = p_{\text{win}}\overline{r}_{\text{win}} + p_{\text{loss}}\overline{r}_{\text{loss}}$

## Limitations and assumptions

- **Not investment advice.** Educational demo only; past performance does not predict future returns.
- **No fees, slippage, or funding.** Results assume frictionless execution at stated prices; real trading would reduce net returns.
- **Parameter search is exploratory.** The study explores in-sample performance, it's not a claim of out-of-sample performance.
- **Capital:** Fixed 100 000 USD initial equity; long-only; no leverage; no partial sizing.
- **Execution:** Entries and exits at next-day open after signal; no look-ahead bias.
- **Benchmark:** Buy-and-hold Bitcoin.
- **Data:** Daily BTC-USD OHLCV data from Yahoo Finance. Total 1,826 daily bars from 2021-01-01 to 2025-12-31.

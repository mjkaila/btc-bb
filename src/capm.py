"""
CAPM alpha and beta aligned with quantopian/empyrical (daily, rf=0).

The ``empyrical`` package does not build on Python 3.12+ (e.g. Streamlit Cloud
on 3.14). These functions reproduce ``empyrical.beta`` and
``empyrical.alpha(..., period=\"daily\")`` for pandas Series.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

# Matches empyrical's default for period="daily"
DAILY_ANNUALIZATION = 252


def capm_beta(returns: pd.Series, factor_returns: pd.Series, risk_free: float = 0.0) -> float:
    """Covariance(strategy, factor) / variance(factor) with NaN handling like empyrical."""
    s, f = returns.align(factor_returns, join="inner")
    s = s - risk_free
    f = f - risk_free
    sv, fv = s.values.astype(float), f.values.astype(float)
    if len(sv) < 2:
        return float("nan")
    independent = np.where(np.isnan(sv), np.nan, fv)
    ind_residual = independent - np.nanmean(independent)
    covariances = np.nanmean(ind_residual * sv)
    ind_var = np.nanmean(ind_residual**2)
    if ind_var < 1.0e-30:
        return float("nan")
    return float(covariances / ind_var)


def capm_alpha(
    returns: pd.Series,
    factor_returns: pd.Series,
    risk_free: float = 0.0,
    *,
    annualization: int = DAILY_ANNUALIZATION,
    beta_val: float | None = None,
) -> float:
    """Annualized alpha: (1 + mean(excess - beta * factor_excess))^N - 1."""
    s, f = returns.align(factor_returns, join="inner")
    sa = s - risk_free
    fa = f - risk_free
    if len(sa) < 2:
        return float("nan")
    b = capm_beta(returns, factor_returns, risk_free) if beta_val is None else beta_val
    alpha_series = sa.values - b * fa.values
    m = np.nanmean(alpha_series)
    return float((1.0 + m) ** annualization - 1.0)

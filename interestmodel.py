"""
Interest income backtest & forecast for GameStop (GME)

Overview
--------
This script backtests and forecasts GME's quarterly "interest (income) expense, net"
by simulating ACT/365 daily interest accruals on investable liquidity
(cash & cash equivalents + marketable securities), while time-weighting balances
for dated capital flows (ATMs, convertible notes) and modeling a specific Bitcoin
purchase program. It reconciles each reported quarter to the exact end-of-quarter
liquidity (from press releases/10-Qs/10-K) via a straight-line residual drift so
the terminal cash balance matches filings.

For forecast quarters (i.e., any quarter after the last known anchor in
`quarter_end_liquidity()`), the script:
  * sets end-of-quarter liquidity = start_liq + dated_events + BTC cash flows (drift = 0),
  * accrues modeled interest daily,
  * **adds modeled interest to the quarter’s ending liquidity when carrying into
    the next quarter** so interest compounds through the forecast horizon.

Data inputs (hard-coded anchors & events)
-----------------------------------------
• Quarter-end liquidity anchors (cash & equivalents + marketable securities), USD millions:
  See `quarter_end_liquidity()`. These are the authoritative quarter-end values
  used to calibrate reported quarters.

• Dated events (ATM equity offerings, convertible notes, etc.), USD millions:
  See `dated_events()`. Positive = inflow, negative = outflow. Events are applied
  on exact calendar days and affect daily balances.

• Bitcoin purchase window (default 2025-05-04 … 2025-06-10):
  Modeled as evenly distributed unit purchases across the window, priced by
  Yahoo Finance BTC-USD daily closes (plus a fee uplift).

Market data & offline fallbacks
-------------------------------
• Rates: FRED DGS3MO (3-Month Treasury Constant Maturity, percent).
  - Daily series pulled via `pandas_datareader`.
  - Reindexed to a complete daily range and forward/back-filled so **no NaNs remain**.
  - If FRED fails, the script uses a constant `DEFAULT_OFFLINE_RATE_PCT`.

• BTC-USD:
  - Daily prices fetched with `yfinance`.
  - If download fails, the BTC outflow falls back to an evenly spread USD total
    (`BTC_USD_TOTAL_MM`) across the window (units/price left NaN for diagnostics).

Core mechanics
--------------
1) Build quarter calendar: `build_quarter_frame_with_forecast(forecast_quarters, quarter_days)`
   creates historical quarters from anchors and appends N forecast quarters (~13 weeks each).

2) For each quarter:
   - Start liquidity = prior quarter’s carry (reported end_liq for historical,
     **end_liq + modeled interest** for forecasts).
   - Apply dated events and daily BTC cash flows.
   - Apply a constant "residual drift" so the day-by-day path exactly hits the known
     `end_liq` on quarter end for reported quarters. For forecasts, drift = 0 by design.
   - Join daily rates and accrue interest = ending_balance * daily_rate; sum to quarter.

3) BTC diagnostics:
   - Track units purchased within the BTC window, end-of-quarter holdings, end-of-quarter
     fair value, and quarterly BTC earnings = FV_end − (FV_beg + cost_of_new_purchases).
   - Prefetch BTC closes once for all quarter ends (`prefetch_btc_closes`) to value holdings.

4) Output rows (one per quarter) are accumulated in `results` and converted into a
   DataFrame with additional diagnostics and error metrics.

Forecast carry & totals
-----------------------
• For reported quarters:
  - Carry = reported `end_liq` (interest is already embedded in the reported figure).
  - `total_end_liq_mm` = end_liq + BTC fair value (no double counting of interest).

• For forecast quarters:
  - Carry = end_liq + modeled_interest_mm (so interest compounds).
  - `total_end_liq_mm` = (end_liq + modeled_interest_mm) + BTC fair value.

Key functions
-------------
• `quarter_end_liquidity() -> Dict[str, float]`
    Quarter-end liquidity anchors (USD mm).

• `dated_events(net_to_gross=ATM_NET_TO_GROSS) -> pd.DataFrame`
    Dated inflows/outflows (USD mm). Positive = cash in.

• `build_quarter_frame_with_forecast(forecast_quarters=1, quarter_days=91) -> pd.DataFrame`
    Quarter start/end dates (adds N forecast quarters).

• `fetch_rates(start, end) -> pd.DataFrame`
    DGS3MO (%), reindexed to full daily range with no NaNs, plus `daily_rate`.

• `btc_outflow_series(start, end, ...) -> pd.DataFrame`
    Daily BTC cash outflows (USD mm negative), units/day, price, fee multiplier.

• `prefetch_btc_closes(q_end_dates) -> pd.Series`
    BTC-USD close mapped to each quarter end (for holdings valuation).

• `build_daily_path(QuarterInputs, rates) -> (pd.DataFrame, float)`
    Daily path with events/BTC/drift, then daily interest accrual; returns daily detail
    and the quarter’s modeled interest (USD mm).

• `simulate_all(..., forecast_quarters=1) -> pd.DataFrame`
    Full backtest + multi-quarter forecast, returns the per-quarter results DataFrame
    and writes a CSV to `OUT_DIR`.

Configuration knobs
-------------------
• `FRED_SERIES`, `DAYCOUNT`, `DEFAULT_OFFLINE_RATE_PCT`
• `ATM_NET_TO_GROSS` (scales gross ATM proceeds to approximate net)
• `BTC_FEE_BPS`, `BTC_PRICE_BASIS`, `BTC_USD_TOTAL_MM`
• `MAKE_DAILY_PARQUETS`, `OUT_DIR`
• `forecast_quarters` (how far ahead to extend)

Outputs
-------
• CSV: `gme_interest_backtest_results.csv` in `OUT_DIR`
• Optional per-quarter daily parquet files (if `MAKE_DAILY_PARQUETS=True`)
• Console summary:
  - Backtest MAPE/sMAPE
  - Implied annualized yields vs 3M (recent reported quarters)
  - Forecast quarter implied yield vs 3M

Limitations & notes
-------------------
• Quarter lengths: all quarters are 13 weeks (~91 days) except known exceptions
  (e.g., historical 14-week quarters are captured by the anchors; `quarter_days`
  controls length for appended forecast quarters).
• BTC fallback path leaves units/price NaN; cash outflow is respected.
• This is a stylized treasury model (no intraday timing, hedging, or working
  capital seasonality beyond the linear drift).
• Ensure anchors and events are maintained as new filings arrive.

Usage
-----
Run from a terminal:
  python interest_model.py
or call `simulate_all(forecast_quarters=N)` from another script or notebook.

Dependencies
------------
pandas, numpy, pandas_datareader, yfinance, python-dateutil
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

# External data sources (fetched at runtime)
from pandas_datareader import data as pdr  # FRED
import yfinance as yf                      # BTC-USD
from pathlib import Path
import traceback

# -----------------------------
# Configuration
# -----------------------------

FRED_SERIES = "DGS3MO"   # 3M T-bill yield (%)
DAYCOUNT = 365.0         # ACT/365F
ATM_NET_TO_GROSS = 0.995 # Scale gross ATM proceeds to approximate net (set 1.0 to use gross)
MAKE_DAILY_PARQUETS = False
OUT_DIR = Path(r"")
DEFAULT_OFFLINE_RATE_PCT = 5.0                       # fallback if FRED blocked
BTC_USD_TOTAL_MM = 510.0                             # fallback total spend if Yahoo blocked (USD millions)

# -----------------------------
# Utility functions
# -----------------------------

def to_dt(s: str) -> pd.Timestamp:
    return pd.Timestamp(s).normalize()

# -----------------------------
# Domain data
# -----------------------------

def quarter_end_liquidity() -> Dict[str, float]:
    """
    Quarter-end liquidity = cash & cash equivalents + marketable securities, USD millions.
    These anchor terminal balances per quarter.
    """
    return {
        "2022-04-30": 1035.0,
        "2022-07-30":  908.9,
        "2022-10-29": 1042.1,
        "2023-01-28": 1390.6,
        "2023-04-29": 1310.1,
        "2023-07-29": 1194.7,
        "2023-10-28": 1209.5,
        "2024-02-03": 1199.3,
        "2024-05-04": 1082.9,
        "2024-08-03": 4204.2,
        "2024-11-02": 4616.2,
        "2025-02-01": 4774.9,
        "2025-05-03": 6385.8,
    }

def reported_interest_income() -> Dict[str, float]:
    """
    Reported quarterly interest (income) expense, net — USD millions.
    Positive = income. Keys are quarter-end dates (YYYY-MM-DD).
    """
    return {
        # FY2022
        "2022-04-30":  0.7,  # "Interest expense, net 0.1"
        "2022-07-30":  0.3,  # "Interest (income) expense, net (0.3)"
        "2022-10-29":  3.7,  # "Interest (income) expense, net (3.7)"
        "2023-01-28":  4.8,  # derived: FY22 total 9.5 minus Q1–Q3
        # FY2023
        "2023-04-29":  9.7,
        "2023-07-29": 11.6,
        "2023-10-28": 12.9,
        "2024-02-03": 15.3,  # 14-week quarter
        # FY2024
        "2024-05-04": 14.9,
        "2024-08-03": 39.5,
        "2024-11-02": 54.2,
        "2025-02-01": 54.8,  # 13-week quarter
        # FY2025
        "2025-05-03": 56.9,
    }

# -----------------------------
# Optional future policy path (rate cuts/hikes)
# -----------------------------
# Each dict applies from that date forward.
# Use EITHER "delta_bps" (relative) OR "to_pct" (absolute level).
# Example:
# FUTURE_RATE_EVENTS = [
#     {"date": "2025-09-17", "delta_bps": -25},
#     {"date": "2025-11-05", "delta_bps": -25},
#     {"date": "2026-01-28", "to_pct": 3.50},
# ]
FUTURE_RATE_EVENTS: List[Dict[str, float]] = [
      {"date": "2025-09-17", "delta_bps": -25},
      {"date": "2025-10-29", "delta_bps": -25},
]



def dated_events(net_to_gross: float = ATM_NET_TO_GROSS) -> pd.DataFrame:
    """
    Dated capital flows (USD millions). Positive = cash inflow, Negative = outflow.
    BTC purchases are modeled separately (because they span a range of days).
    """
    rows = [
        # ATMs (2024)
        {"date": "2024-05-24", "amount":  933.4 * net_to_gross, "label": "ATM (45M shares) gross~net"},
        {"date": "2024-06-11", "amount": 2137.0 * net_to_gross, "label": "ATM (75M shares) gross~net"},
        {"date": "2024-09-23", "amount":  398.1,                "label": "ATM (20M shares) NET per 10-Q"},
        # Convertibles
        {"date": "2025-04-01", "amount": 1480.7,                "label": "Convertible notes 2030 (NET)"},
        {"date": "2025-06-17", "amount": 2230.0,                "label": "Convertible notes 2032 (NET est.)"},
        # Greenshoe on 2032 converts – exercised in full; ~$446.6m net on 2025-06-24 per 8-K
        {"date": "2025-06-24", "amount":  446.6,                "label": "Convertible notes 2032 GREENSHOE (NET ~ per 8-K)"},
        # (BTC handled separately)
    ]
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"]).dt.normalize()
    return df.sort_values("date").reset_index(drop=True)

def build_quarter_frame_with_forecast(forecast_quarters: int = 1,
                                      quarter_days: int = 91) -> pd.DataFrame:
    """
    Build quarter frames from the liquidity anchors and append `forecast_quarters`
    additional quarters (default ≈13 weeks each via `quarter_days`).
    """
    ends = sorted([to_dt(k) for k in quarter_end_liquidity().keys()])

    # append N forecast quarter-ends
    for _ in range(max(int(forecast_quarters), 0)):
        next_end = (ends[-1] + pd.Timedelta(days=quarter_days)).normalize()
        ends.append(next_end)

    rows = []
    prev = None
    for i, e in enumerate(ends):
        # for the first row, approximate start as 90 days prior (91-day quarter);
        # otherwise start the day after the previous quarter end
        start = (prev + pd.Timedelta(days=1)) if prev is not None else (e - pd.Timedelta(days=quarter_days-1))
        rows.append({"iq": i+1, "q_end": e, "q_start": start})
        prev = e

    qdf = pd.DataFrame(rows).assign(days=lambda d: (d["q_end"] - d["q_start"]).dt.days + 1)
    return qdf


# -----------------------------
# Market data fetchers
# -----------------------------

def fetch_rates(start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    """FRED DGS3MO (%). Returns a daily index from start..end with no NaNs."""
    try:
        r = pdr.DataReader(FRED_SERIES, "fred", start, end).rename(columns={FRED_SERIES: "rate_pct"})
    except Exception as e:
        print(f"[WARN] FRED fetch failed: {e}\n{traceback.format_exc()}")
        r = pd.DataFrame({"rate_pct": []})

    all_days = pd.date_range(start.normalize(), end.normalize(), freq="D")
    r = r.reindex(all_days)

    r["rate_pct"] = (
        r["rate_pct"]
        .ffill()
        .bfill()
        .fillna(DEFAULT_OFFLINE_RATE_PCT)
        .astype(float)
    )
    r["daily_rate"] = (r["rate_pct"] / 100.0) / DAYCOUNT
    return r

def apply_future_rate_events(rates: pd.DataFrame,
                             events: List[Dict[str, float]]) -> pd.DataFrame:
    """
    Modify 'rate_pct' for scheduled future cuts/hikes.
    Events are chronological and cumulative.
    - 'delta_bps': add/subtract basis points from event date forward
    - 'to_pct': set absolute percent level from event date forward
    """
    if not events:
        return rates

    out = rates.copy()
    out["rate_pct"] = pd.to_numeric(out.get("rate_pct"), errors="coerce") \
                        .fillna(DEFAULT_OFFLINE_RATE_PCT)

    def _to_dt(x: str) -> pd.Timestamp:
        return pd.Timestamp(x).normalize()

    for ev in sorted(events, key=lambda e: _to_dt(e["date"])):
        eff = _to_dt(ev["date"])
        mask = out.index >= eff
        if not mask.any():
            continue
        has_delta = "delta_bps" in ev and ev["delta_bps"] is not None
        has_abs   = "to_pct" in ev and ev["to_pct"] is not None
        if has_delta and has_abs:
            raise ValueError("Specify either 'delta_bps' or 'to_pct', not both.")
        if has_abs:
            out.loc[mask, "rate_pct"] = float(ev["to_pct"])
        elif has_delta:
            out.loc[mask, "rate_pct"] = out.loc[mask, "rate_pct"] + float(ev["delta_bps"]) / 100.0

    out["daily_rate"] = (out["rate_pct"] / 100.0) / DAYCOUNT
    return out

# --- BTC execution assumptions ---
BTC_FEE_BPS = 150          # uplift on spend in basis points (≈1.30%); tweak to match "just over $500m"
BTC_PRICE_BASIS = "close"  # "close" or "hlc3" (avg of High/Low/Close) to approximate intraday execution

def btc_outflow_series(
    start: pd.Timestamp,
    end: pd.Timestamp,
    total_btc: float = 4710.0,
    *,
    units_per_day_override: float | None = None,
    fallback_per_day_mm_override: float | None = None,
    fee_bps: float = BTC_FEE_BPS,
    price_basis: str = BTC_PRICE_BASIS,
) -> pd.DataFrame:
    """
    DAILY cash outflow for BTC buys in [start, end]. Tries Yahoo prices; if that fails,
    falls back to spreading a fixed USD total (BTC_USD_TOTAL_MM) evenly across days.
    """
    dates = pd.date_range(start, end, freq="D")
    if len(dates) == 0:
        return pd.DataFrame(index=pd.DatetimeIndex([], name="date"), columns=["cash_flow"]).fillna(0.0)
    try:
        btc = yf.download(
            "BTC-USD",
            start=(start - pd.Timedelta(days=3)).date(),
            end=(end + pd.Timedelta(days=3)).date(),
            progress=False,
            auto_adjust=False,
        )
        if btc.empty:
            raise RuntimeError("Empty Yahoo response")
        # --- choose price basis: "close" (default) or "hlc3" (avg High/Low/Close) ---
        basis = (price_basis or "close").lower()
        if basis == "hlc3" and all(k in btc.columns for k in ["High","Low","Close"]):
            px = (btc["High"] + btc["Low"] + btc["Close"]) / 3.0
        else:
            # robust close extraction fallback
            if "Close" in btc.columns:
                px = btc["Close"]
            else:
                if isinstance(btc.columns, pd.MultiIndex):
                    if ("Close", "BTC-USD") in btc.columns:
                        px = btc[("Close","BTC-USD")]
                    elif "Adj Close" in btc.columns.get_level_values(0):
                        tmp = btc.xs("Adj Close", axis=1, level=0)
                        px = tmp.iloc[:,0] if isinstance(tmp, pd.DataFrame) else tmp
                    else:
                        px = btc.iloc[:,0]
                else:
                    px = btc["Adj Close"] if "Adj Close" in btc.columns else btc.squeeze("columns")

        if isinstance(px, pd.DataFrame) and px.shape[1] == 1:
            px = px.iloc[:, 0]
        px = pd.to_numeric(px, errors="coerce").reindex(dates).ffill()
        units_per_day = (
            float(units_per_day_override) if units_per_day_override is not None
            else float(total_btc) / len(dates)
        )
        fee_mult = 1.0 + (float(fee_bps) / 10_000.0)
        usd_outflow = px.to_numpy() * units_per_day * fee_mult
        outflow_mm = -(usd_outflow / 1_000_000.0).astype(float)
        # also return units and price for diagnostics
        return pd.DataFrame({
            "cash_flow": outflow_mm,             # USD millions (negative)
            "btc_units": np.full(len(dates), units_per_day, dtype=float),
            "btc_price_usd": px.to_numpy().astype(float),
            "btc_fee_mult": np.full(len(dates), fee_mult, dtype=float),
        }, index=dates)
    except Exception as e:
        print(f"[WARN] BTC price fetch failed: {e}\n{traceback.format_exc()}")
        fee_mult = 1.0 + (float(fee_bps) / 10_000.0)
        per_day_mm = -((fallback_per_day_mm_override if fallback_per_day_mm_override is not None
                        else (BTC_USD_TOTAL_MM / len(dates))) * fee_mult)
        # price/units unknown in fallback; keep NaN so downstream calcs handle gracefully
        return pd.DataFrame({
            "cash_flow": np.full(len(dates), per_day_mm, dtype=float),
            "btc_units": np.full(len(dates), np.nan),
            "btc_price_usd": np.full(len(dates), np.nan),
            "btc_fee_mult": np.full(len(dates), fee_mult, dtype=float),
        }, index=dates)
def prefetch_btc_closes(q_end_dates: List[pd.Timestamp]) -> pd.Series:
    """
    Fetch BTC-USD closes for all quarter-end dates in one call, robustly.
    Returns a Series indexed by normalized q_end (Timestamp) with a USD close.
    Falls back to NaNs if download fails.
    """
    if len(q_end_dates) == 0:
        return pd.Series(dtype=float)

    start = (min(q_end_dates) - pd.Timedelta(days=5)).date()
    end   = (max(q_end_dates) + pd.Timedelta(days=2)).date()  # yfinance 'end' is exclusive

    try:
        df = yf.download("BTC-USD", start=start, end=end, progress=False, auto_adjust=False)
        if df is None or df.empty:
            raise RuntimeError("empty BTC-USD frame")

        # --- Normalize whatever yfinance returned into a 1-D Series ---
        if isinstance(df.columns, pd.MultiIndex):
            px = None
            if ("Close", "BTC-USD") in df.columns:
                px = df[("Close", "BTC-USD")]
            elif "Close" in df.columns.get_level_values(0):
                tmp = df.xs("Close", axis=1, level=0)
                px = tmp.iloc[:, 0] if isinstance(tmp, pd.DataFrame) else tmp
            elif "Adj Close" in df.columns.get_level_values(0):
                tmp = df.xs("Adj Close", axis=1, level=0)
                px = tmp.iloc[:, 0] if isinstance(tmp, pd.DataFrame) else tmp
            else:
                px = df.iloc[:, 0]
        else:
            if "Close" in df.columns:
                px = df["Close"]
            elif "Adj Close" in df.columns:
                px = df["Adj Close"]
            else:
                px = df.squeeze("columns")

        # If still a DataFrame, squeeze to first column; if ndarray, wrap as Series
        if isinstance(px, pd.DataFrame):
            px = px.iloc[:, 0]
        if not isinstance(px, pd.Series):
            px = pd.Series(np.asarray(px).reshape(-1), index=pd.to_datetime(df.index).normalize())

        # --- Clean, align, and map to quarter ends ---
        px = pd.to_numeric(px, errors="coerce")
        px.index = pd.to_datetime(px.index).normalize()

        all_days = pd.date_range(px.index.min(), px.index.max(), freq="D")
        px = px.reindex(all_days).ffill()

        want = pd.to_datetime(pd.Index(q_end_dates)).normalize()
        out = px.reindex(want, method="ffill")
        out.index = want
        return out.astype(float)

    except Exception as e:
        print(f"[WARN] BTC prefetch failed: {e}\n{traceback.format_exc()}")
        want = pd.to_datetime(pd.Index(q_end_dates)).normalize()
        return pd.Series(index=want, data=np.nan, dtype=float)

# -----------------------------
# Simulation
# -----------------------------



@dataclass
class QuarterInputs:
    q_start: pd.Timestamp
    q_end: pd.Timestamp
    start_liq: float      # USD mm
    end_liq: float        # USD mm
    events: pd.DataFrame  # rows within quarter (date, amount, label)
    btc_out: pd.DataFrame # 'cash_flow' daily (USD mm negative); may be empty

def build_daily_path(inputs: QuarterInputs, rates: pd.DataFrame) -> Tuple[pd.DataFrame, float]:
    """
    Construct daily balance path that:
      - Starts at start_liq
      - Applies dated events and BTC purchase outflows on exact days
      - Adds a linear "residual drift" so that terminal equals end_liq
    Then accrues daily interest using 'rates' (joined by date).
    Returns (daily_df, interest_mm) where interest_mm is in USD millions.
    """
    days = pd.date_range(inputs.q_start, inputs.q_end, freq="D")
    df = pd.DataFrame(index=days)
    df.index.name = "date"

    # Events (point flows) and BTC (daily)
    e = inputs.events.set_index("date")["amount"] if not inputs.events.empty else pd.Series(dtype=float)
    df["events"] = e.reindex(df.index, fill_value=0.0).astype(float)
    df["btc"] = (inputs.btc_out.reindex(df.index)["cash_flow"].fillna(0.0)
                 if not inputs.btc_out.empty else 0.0)

    # Residual drift per day to reconcile to end_liq
    mech_flows_total = (df["events"] + df["btc"]).sum()
    n_days = len(df)
    drift_per_day = (inputs.end_liq - inputs.start_liq - mech_flows_total) / n_days
    df["drift"] = drift_per_day

    # Daily ending balance
    balance = []
    bal = inputs.start_liq
    for d in df.itertuples():
        bal += d.events + d.btc + d.drift
        balance.append(bal)
    df["ending_balance_mm"] = balance

    # Rates & interest (rates are already dense & non-NaN from fetch_rates)
    df = df.join(rates.reindex(df.index)[["daily_rate"]])
    df["interest_mm"] = df["ending_balance_mm"] * df["daily_rate"]

    return df, float(df["interest_mm"].sum())


def simulate_all(net_to_gross: float = ATM_NET_TO_GROSS,
                 btc_units: float = 4710.0,
                 btc_window: Tuple[str, str] = ("2025-05-04", "2025-06-10"),
                 save_daily: bool = MAKE_DAILY_PARQUETS,
                 forecast_quarters: int = 1) -> pd.DataFrame:
    """
    Backtest all reported quarters and **forecast exactly one quarter ahead**.
    """
    qdf = build_quarter_frame_with_forecast(forecast_quarters=forecast_quarters)
    q_liq = quarter_end_liquidity()
    q_rep = reported_interest_income()
    events = dated_events(net_to_gross=net_to_gross)

    # Rates covering the whole span, incl. the appended forecast quarter
    start_all = qdf["q_start"].min() - pd.Timedelta(days=5)
    end_all = qdf["q_end"].max() + pd.Timedelta(days=5)
    rates = fetch_rates(start_all, end_all)
    rates = apply_future_rate_events(rates, FUTURE_RATE_EVENTS)

    results = []
    prev_end_liq = None
    # ---- Track BTC position across quarters ----
    cum_btc_units = 0.0       # units held at the end of the prior quarter
    cum_btc_cost_mm = 0.0     # cumulative USD cost basis (millions)
    prev_q_end = None         # previous quarter-end Timestamp (for qtr P&L)

    # Prefetch BTC closes for every q_end to avoid per-row downloads
    btc_closes_by_qend = prefetch_btc_closes(qdf["q_end"].tolist())

    # Global BTC purchase schedule (constant units/day across the full window)
    btc_window_start = pd.to_datetime(btc_window[0])
    btc_window_end   = pd.to_datetime(btc_window[1])
    btc_global_days = pd.date_range(btc_window_start, btc_window_end, freq="D")
    units_per_day_global = (btc_units / len(btc_global_days)) if len(btc_global_days) else 0.0
    fallback_per_day_mm_global = (BTC_USD_TOTAL_MM / len(btc_global_days)) if len(btc_global_days) else 0.0



    for _, row in qdf.iterrows():
        q_end = row["q_end"]
        q_start = row["q_start"]
        end_key = q_end.strftime("%Y-%m-%d")

        # Start liquidity = previous quarter end liquidity
        if prev_end_liq is None:
            reported_end = q_liq.get(end_key, np.nan)
            start_liq = float(reported_end) if not np.isnan(reported_end) else 0.0
        else:
            start_liq = float(prev_end_liq)

        # Quarter’s dated events & BTC window overlap
        ev_q = events[(events["date"] >= q_start) & (events["date"] <= q_end)].copy()
        btc_start, btc_end = pd.to_datetime(btc_window[0]), pd.to_datetime(btc_window[1])
        overlap_start = max(q_start, btc_start)
        overlap_end = min(q_end, btc_end)
        if overlap_start <= overlap_end:
            btc_df = btc_outflow_series(
                overlap_start, overlap_end,
                total_btc=btc_units,
                units_per_day_override=units_per_day_global,
                fallback_per_day_mm_override=fallback_per_day_mm_global,
                fee_bps=BTC_FEE_BPS,
                price_basis=BTC_PRICE_BASIS,
            )
        else:
            btc_df = pd.DataFrame(index=pd.DatetimeIndex([], name="date"), columns=["cash_flow"])

        # ---- BTC diagnostics (compute once, reuse) ----
        btc_spent_mm = float(-btc_df["cash_flow"].sum()) if not btc_df.empty else 0.0  # +USD mm
        if not btc_df.empty and "btc_units" in btc_df:
            btc_units_executed = float(pd.to_numeric(btc_df["btc_units"], errors="coerce").sum())
        else:
            btc_units_executed = 0.0
        btc_avg_price_usd = (btc_spent_mm * 1_000_000.0 / btc_units_executed) if btc_units_executed > 0 else np.nan


        # Determine end_liq and forecast flag
        reported_end = q_liq.get(end_key, np.nan)
        is_forecast = False
        if np.isnan(reported_end):
            is_forecast = True
            ev_sum = float(ev_q["amount"].sum()) if not ev_q.empty else 0.0
            btc_sum = float(btc_df["cash_flow"].sum()) if not btc_df.empty else 0.0
            end_liq = float(start_liq + ev_sum + btc_sum)  # drift=0 by construction
        else:
            end_liq = float(reported_end)

        q_inputs = QuarterInputs(
            q_start=q_start, q_end=q_end,
            start_liq=start_liq, end_liq=end_liq,
            events=ev_q, btc_out=btc_df
        )

        daily, modeled_interest_mm = build_daily_path(q_inputs, rates)
        if save_daily:
            OUT_DIR.mkdir(parents=True, exist_ok=True)
            daily.to_parquet(str(OUT_DIR / f"gme_quarter_{q_end.date()}_daily.parquet"))

        reported = q_rep.get(end_key)
        abs_err = np.nan
        pct_err = np.nan
        if reported is not None:
            abs_err = modeled_interest_mm - reported
            pct_err = abs_err / reported if reported != 0 else np.nan

        # ---- Drift diagnostics ----
        drift_per_day_mm = float(daily["drift"].iloc[0]) if not daily.empty else np.nan
        total_drift_mm = float(daily["drift"].sum()) if not daily.empty else np.nan
 
        # ---- Yield diagnostics: average balance and implied annualized yields ----
        days_in_q = len(daily)
        avg_balance_mm = float(daily["ending_balance_mm"].mean())
        # quarter-average 3M T-bill annual yield (%), from fetched FRED series
        ref_3m_ann_yield_pct = float(rates.loc[q_start:q_end, "rate_pct"].mean())
        # implied annualized yields (%)
        implied_ann_yield_modeled_pct = (
            (modeled_interest_mm / (avg_balance_mm * days_in_q)) * 365.0 * 100.0
            if avg_balance_mm > 0 and days_in_q > 0 else np.nan
        )
        implied_ann_yield_reported_pct = (
            (reported / (avg_balance_mm * days_in_q)) * 365.0 * 100.0
            if (reported is not None and not np.isnan(reported) and avg_balance_mm > 0 and days_in_q > 0)
            else np.nan
        )
        # spreads vs 3M (basis points)
        modeled_minus_3m_bps = (
            round((implied_ann_yield_modeled_pct - ref_3m_ann_yield_pct) * 100.0)
            if not np.isnan(implied_ann_yield_modeled_pct) else np.nan
        )
        reported_minus_3m_bps = (
            round((implied_ann_yield_reported_pct - ref_3m_ann_yield_pct) * 100.0)
            if not np.isnan(implied_ann_yield_reported_pct) else np.nan
        )


        # ---- Quarterly BTC holdings, valuation & P&L (single source of truth) ----
        # Prices at begin/end of quarter
        btc_px_qbeg_usd = float(btc_closes_by_qend.get(prev_q_end, np.nan)) if prev_q_end is not None else np.nan
        btc_px_qend_usd = float(btc_closes_by_qend.get(q_end, np.nan))

        # Holdings at beginning (carry from prior quarter)
        btc_units_beg = float(cum_btc_units)
        fv_beg_mm = (btc_units_beg * btc_px_qbeg_usd) / 1_000_000.0 if (btc_units_beg > 0.0 and np.isfinite(btc_px_qbeg_usd)) else 0.0

        # End holdings and valuation
        btc_units_end = btc_units_beg + btc_units_executed
        fv_end_mm = (btc_units_end * btc_px_qend_usd) / 1_000_000.0 if (btc_units_end > 0.0 and np.isfinite(btc_px_qend_usd)) else 0.0

        # Quarterly P&L = FV_end − (FV_beg + cost_of_new_purchases)
        btc_earnings_mm = fv_end_mm - (fv_beg_mm + btc_spent_mm)
        # Roll cumulative state to next quarter
        cum_btc_units = btc_units_end
        cum_btc_cost_mm += btc_spent_mm  # track basis if you want it elsewhere

        # Liquidity & carry rules:
        # - For reported quarters: reported end_liq already embeds interest → carry = end_liq
        # - For forecast quarters: add modeled interest so it compounds → carry = end_liq + modeled_interest_mm
        end_liq_carry_mm = float(end_liq) + (modeled_interest_mm if is_forecast else 0.0)
        # Total liquidity view (cash+securities + BTC FV); for forecasts this also includes modeled interest
        total_end_liq_mm = end_liq_carry_mm + fv_end_mm

        results.append({
            "q_end": pd.Timestamp(q_end).normalize(),
            "is_forecast": is_forecast,
            "days": len(daily),
            "modeled_interest_mm": round(float(modeled_interest_mm), 2),
            "reported_interest_mm": reported,
            "abs_error_mm": round(float(abs_err), 2) if not math.isnan(abs_err) else np.nan,
            "pct_error": round(float(pct_err), 4) if not math.isnan(pct_err) else np.nan,
            "start_liq_mm": round(float(start_liq), 2),
            "end_liq_mm": round(float(end_liq), 2),
            "events_mm": round(float(ev_q["amount"].sum()), 2) if not ev_q.empty else 0.0,
            "btc_units_window": (btc_units if (overlap_start <= overlap_end) else 0.0),
            # BTC diagnostics
            "btc_spent_mm": round(btc_spent_mm, 2),
            "btc_units_executed": round(btc_units_executed, 6),
            "btc_avg_price_usd": round(btc_avg_price_usd, 2) if np.isfinite(btc_avg_price_usd) else np.nan,
            "btc_px_qbeg_usd": round(btc_px_qbeg_usd, 2) if np.isfinite(btc_px_qbeg_usd) else np.nan,
            "btc_px_qend_usd": round(btc_px_qend_usd, 2) if np.isfinite(btc_px_qend_usd) else np.nan,
            "btc_units_holdings": round(btc_units_end, 6),
            "btc_fair_value_mm": round(fv_end_mm, 2),
            "btc_earnings_mm": round(btc_earnings_mm, 2),
            "end_liq_carry_mm": round(end_liq_carry_mm, 2),
            "total_end_liq_mm": round(total_end_liq_mm, 2),
            # New diagnostics
            "avg_balance_mm": round(avg_balance_mm, 2),
            "implied_ann_yield_modeled_pct": round(implied_ann_yield_modeled_pct, 2) if not np.isnan(implied_ann_yield_modeled_pct) else np.nan,
            "implied_ann_yield_reported_pct": round(implied_ann_yield_reported_pct, 2) if not np.isnan(implied_ann_yield_reported_pct) else np.nan,
            "ref_3m_ann_yield_pct": round(ref_3m_ann_yield_pct, 2) if not np.isnan(ref_3m_ann_yield_pct) else np.nan,
            "modeled_minus_3m_bps": modeled_minus_3m_bps,
            "reported_minus_3m_bps": reported_minus_3m_bps,
            "drift_per_day_mm": round(drift_per_day_mm, 6) if not math.isnan(drift_per_day_mm) else np.nan,
            "total_drift_mm": round(total_drift_mm, 2) if not math.isnan(total_drift_mm) else np.nan,

        })

        # Carry forward for next quarter start_liq (compounds interest only for forecasts)
        prev_end_liq = end_liq_carry_mm
        prev_q_end = q_end


    # Build results frame
    res = pd.DataFrame(results)

    # Ensure types that downstream math expects
    res["reported_interest_mm"] = pd.to_numeric(res["reported_interest_mm"], errors="coerce")

    # Normalize q_end once (keep NaT if any)
    res["q_end"] = pd.to_datetime(res["q_end"], errors="coerce").dt.normalize()

    # ------ Operating drift (non-interest plug) ------
    res["operating_drift_mm"] = (res["total_drift_mm"] - res["modeled_interest_mm"]).round(2)
    # Forecast rows: by design we show NaN for operating drift
    res.loc[res["is_forecast"], "operating_drift_mm"] = np.nan

    # (Backwards-compat: drop legacy forecast-only column if it exists from old runs)
    if "total_end_liq_forecast_mm" in res.columns: res = res.drop(columns=["total_end_liq_forecast_mm"])


    # ------ Fiscal quarter (FY ends in March) ------
    res.insert(1, "qtr", pd.PeriodIndex(res["q_end"], freq="Q-MAR").quarter.astype("Int64"))

    # Error metrics (for backtest rows only)
    with np.errstate(invalid="ignore", divide="ignore"):
        res["ape"] = np.abs(res["modeled_interest_mm"] - res["reported_interest_mm"]) / np.abs(res["reported_interest_mm"])
        res["smape"] = np.abs(res["modeled_interest_mm"] - res["reported_interest_mm"]) / (
            (np.abs(res["modeled_interest_mm"]) + np.abs(res["reported_interest_mm"])) / 2
        )
    mask = res["reported_interest_mm"].abs() >= 5.0
    mape_clean = np.nanmean(res.loc[mask, "ape"])
    smape_all = np.nanmean(res["smape"])
    print(f"Backtest MAPE (|reported|≥$5m): {mape_clean:.2%} | sMAPE (all): {smape_all:.2%}")

    # Pretty print: implied yield vs 3M for the most recent reported quarters
    cols = ["q_end","qtr","avg_balance_mm","implied_ann_yield_reported_pct",
            "implied_ann_yield_modeled_pct","ref_3m_ann_yield_pct",
            "reported_minus_3m_bps","modeled_minus_3m_bps"]
    rep_view = res[res["reported_interest_mm"].notna()][cols].tail(8)
    if not rep_view.empty:
        print("\nImplied annualized yield vs 3M T-bill — reported & modeled (last 8 reported quarters):")
        print(rep_view.to_string(index=False))
    # Forecast quarter view (if present)
    fc_view = res[res["is_forecast"]][["q_end","qtr","avg_balance_mm",
                "implied_ann_yield_modeled_pct","ref_3m_ann_yield_pct","modeled_minus_3m_bps"]]
    if not fc_view.empty:
        print("\nForecast quarter — implied annualized yield (modeled) vs 3M:")
        print(fc_view.to_string(index=False))


    # Save results
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "gme_interest_backtest_results.csv"
    res.to_csv(out_path, index=False)
    print(f"Saved results to: {out_path.resolve()}")

    return res

if __name__ == "__main__":
    # Run with default settings
    df = simulate_all(forecast_quarters=3)
    # Show last rows (includes the forecast quarter with is_forecast=True)
    print(df.tail(8).to_string(index=False))
    print("\nSaved per-quarter results to gme_interest_backtest_results.csv")

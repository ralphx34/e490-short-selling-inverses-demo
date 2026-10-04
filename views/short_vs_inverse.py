import sqlite3
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import numpy as np


# ---------------------------------------------------------
# PRESENTATION STYLING
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    .stMarkdown p,
    .stMarkdown li {
        font-size: 1.15rem;
        line-height: 1.6;
    }

    [data-testid="stExpander"] summary p {
        font-size: 1.15rem;
    }

    [data-testid="stCaptionContainer"] p {
        font-size: 1.05rem;
        line-height: 1.5;
    }

    [data-testid="stMetricLabel"] p {
        font-size: 1.05rem;
    }

    [data-testid="stMetricValue"] {
        font-size: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
PAIR_MAP = {
    "S&P 500 — SPY vs. SH": {
        "underlying": "SPY",
        "inverse": "SH",
    },
    "Russell 2000 — IWM vs. RWM": {
        "underlying": "IWM",
        "inverse": "RWM",
    },
    "NASDAQ-100 — QQQ vs. PSQ": {
        "underlying": "QQQ",
        "inverse": "PSQ",
    },
}


# Change this only if your database has a different filename.
DB_PATH = Path("data/all_inverse_data.db")


# ---------------------------------------------------------
# DATA
# ---------------------------------------------------------
@st.cache_data
def load_pair_data(db_path, underlying, inverse):
    with sqlite3.connect(db_path) as conn:
        query = """
            SELECT
                Date,
                Contract,
                Close
            FROM historical_bars
            WHERE Contract IN (?, ?)
            ORDER BY Date
        """

        data = pd.read_sql_query(
            query,
            conn,
            params=(underlying, inverse),
        )

    data["Date"] = pd.to_datetime(data["Date"])
    data["Close"] = pd.to_numeric(data["Close"])

    prices = (
        data.pivot(
            index="Date",
            columns="Contract",
            values="Close",
        )
        .dropna(subset=[underlying, inverse])
        .sort_index()
    )

    return prices


# ---------------------------------------------------------
# PAGE
# ---------------------------------------------------------
st.title("Short Selling vs. Inverse ETFs")


# =========================================================
# CONCEPTUAL COMPARISON
# =========================================================
st.header("Two Ways to Take a Bearish Position")

with st.expander("How are short selling and inverse ETFs different?"):
    st.markdown(
        """
        Both a direct short position and an inverse ETF can be used to
        obtain exposure that benefits when the underlying asset declines.

        They are not, however, the same financial position.

        A **short position** is created by borrowing and selling shares of
        the underlying security. The number of shares shorted does not
        automatically reset each day.

        A **−1× inverse ETF** instead targets the opposite of the
        underlying asset's **daily return**. Its exposure is rebalanced
        as part of the fund's daily reset.

        Because these positions evolve differently through time, their
        performance can diverge over multi-day holding periods.
        """
    )


# =========================================================
# WHAT IS THE COMPARISON SHOWING?
# =========================================================
with st.expander("What is this comparison showing?"):
    st.markdown(
        """
        The comparison places two bearish strategies on the same normalized
        starting value of **$100** so their performance paths can be compared
        directly.

        The **short-position** series is constructed from the negative of the
        underlying ETF's close-to-close log return.

        The **inverse ETF** series uses the historical closing prices of the
        actual inverse ETF and is normalized to the same starting value.

        The purpose of the comparison is to show that two strategies that both
        provide bearish exposure can evolve differently over multi-day holding
        periods.
        """
    )


# =========================================================
# HISTORICAL COMPARISON
# =========================================================
st.header("Historical Comparison")

control1, control2, control3 = st.columns([1.6, 1, 1])

with control1:
    pair_name = st.selectbox(
        "Market",
        list(PAIR_MAP.keys()),
    )

pair = PAIR_MAP[pair_name]
underlying = pair["underlying"]
inverse = pair["inverse"]


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
if not DB_PATH.exists():
    st.error(
        f"Database not found at: {DB_PATH}\n\n"
        "Place the historical ETF database in the data folder or "
        "change DB_PATH at the top of this file."
    )
    st.stop()


prices = load_pair_data(
    str(DB_PATH),
    underlying,
    inverse,
)


if prices.empty:
    st.error(
        f"No overlapping observations were found for "
        f"{underlying} and {inverse}."
    )
    st.stop()


min_date = prices.index.min().date()
max_date = prices.index.max().date()


with control2:
    start_date = st.date_input(
        "Start date",
        value=min_date,
        min_value=min_date,
        max_value=max_date,
    )

with control3:
    end_date = st.date_input(
        "End date",
        value=max_date,
        min_value=min_date,
        max_value=max_date,
    )


if start_date >= end_date:
    st.warning("The end date must be later than the start date.")
    st.stop()


sample = prices.loc[
    (prices.index.date >= start_date)
    & (prices.index.date <= end_date)
].copy()


if len(sample) < 2:
    st.warning(
        "The selected period does not contain enough overlapping "
        "trading days."
    )
    st.stop()


# ---------------------------------------------------------
# CONSTRUCT THE TWO STRATEGIES
# ---------------------------------------------------------

# ---------------------------------------------------------
# CONSTRUCT CUMULATIVE RETURN SERIES
# ---------------------------------------------------------

# Compute close-to-close log returns.
log_returns = np.log(
    sample[[underlying, inverse]]
).diff()

# Synthetic short return:
# negative of the underlying ETF's log return.
log_returns["Short Position"] = -log_returns[underlying]

# Keep only observations for which both return series exist.
strategy_returns = log_returns[
    ["Short Position", inverse]
].dropna()

# Cumulate log returns and convert to an index beginning at 100.
cumulative_log_returns = strategy_returns.cumsum()

short_value = (
    100
    * np.exp(cumulative_log_returns["Short Position"])
)

inverse_value = (
    100
    * np.exp(cumulative_log_returns[inverse])
)

# Explicitly normalize the first plotted observation.
short_value.iloc[0] = 100.0
inverse_value.iloc[0] = 100.0


comparison = pd.DataFrame(
    {
        "Short Position": short_value,
        f"{inverse} Inverse ETF": inverse_value,
    },
    index=sample.index,
)


# ---------------------------------------------------------
# MAIN CHART
# ---------------------------------------------------------
st.subheader(
    f"{underlying} Short Position vs. {inverse}"
)

st.caption(
    "Both strategies begin at an illustrative value of $100. "
    "The chart compares how their values evolve over the selected "
    "historical period."
)


fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=comparison.index,
        y=comparison["Short Position"],
        mode="lines",
        name=f"Short {underlying}",
        line=dict(width=3),
    )
)

fig.add_trace(
    go.Scatter(
        x=comparison.index,
        y=comparison[f"{inverse} Inverse ETF"],
        mode="lines",
        name=inverse,
        line=dict(width=3),
    )
)

fig.add_hline(
    y=100,
    line_dash="dot",
    opacity=0.5,
)

fig.update_layout(
    height=480,
    margin=dict(
        l=20,
        r=20,
        t=30,
        b=20,
    ),
    xaxis_title=None,
    yaxis_title="Strategy Value ($)",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0,
    ),
    hovermode="x unified",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)


# ---------------------------------------------------------
# FINAL RESULTS
# ---------------------------------------------------------
short_final = comparison["Short Position"].iloc[-1]
inverse_final = comparison[f"{inverse} Inverse ETF"].iloc[-1]

short_return = short_final / 100 - 1
inverse_return = inverse_final / 100 - 1

difference = inverse_final - short_final

underlying_return = (
    sample[underlying].iloc[-1]
    / sample[underlying].iloc[0]
    - 1
)


metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric(
    f"{underlying} Return",
    f"{underlying_return:.2%}",
)

metric2.metric(
    f"Short {underlying}",
    f"${short_final:,.2f}",
    f"{short_return:.2%}",
)

metric3.metric(
    inverse,
    f"${inverse_final:,.2f}",
    f"{inverse_return:.2%}",
)

metric4.metric(
    "Final Difference",
    f"${difference:,.2f}",
)


# =========================================================
# IMPORTANT SIMULATION ASSUMPTIONS
# =========================================================
with st.expander("What does the simulation leave out?"):
    st.markdown(
        """
        The direct short-position calculation is intentionally simplified.

        It does **not** currently include:

        - stock-borrow fees,
        - payments in lieu of dividends,
        - financing or margin costs,
        - changes in borrow availability,
        - transaction costs.

        The inverse-ETF series uses the historical market price of the
        actual fund, so its realized path can also reflect features of the
        fund beyond the idealized daily-reset mechanism.

        These simplifications allow the visualization to focus on the
        difference between a fixed-share short position and an actual
        inverse ETF.
        """
    )
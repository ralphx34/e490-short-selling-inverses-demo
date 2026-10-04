import streamlit as st
import pandas as pd


# ---------------------------------------------------------
# PRESENTATION STYLING
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    /* General body text */
    .stMarkdown p,
    .stMarkdown li {
        font-size: 1.15rem;
        line-height: 1.6;
    }

    /* Expander labels */
    [data-testid="stExpander"] summary p {
        font-size: 1.15rem;
    }

    /* Widget labels */
    [data-testid="stWidgetLabel"] p {
        font-size: 1.1rem;
    }

    /* Captions */
    [data-testid="stCaptionContainer"] p {
        font-size: 1.05rem;
        line-height: 1.5;
    }

    /* Metric labels */
    [data-testid="stMetricLabel"] p {
        font-size: 1.05rem;
    }

    /* Metric values */
    [data-testid="stMetricValue"] {
        font-size: 2.25rem;
    }

    /* Input text */
    input {
        font-size: 1.1rem !important;
    }

    /* Selectbox text */
    [data-baseweb="select"] {
        font-size: 1.1rem;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        font-size: 1.05rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.title("Short Selling & Dividends")


# ---------------------------------------------------------
# INTRODUCTION TO SHORT SELLING
# ---------------------------------------------------------
st.header("Introduction to Short Selling")

with st.expander("What is short selling?"):
    st.markdown(
        """
        A **short sale** occurs when an investor sells shares that they do
        not currently own. The shares are borrowed and delivered to the
        buyer, while the investor assumes an obligation to eventually
        return an equivalent number of shares.

        In Trader Workstation (TWS), there is no separate *short sell*
        order direction. If a sell order causes your position in a security
        to fall below zero, the resulting negative position represents a
        short position.

        Short selling therefore introduces considerations that do not arise
        in an ordinary long position, including:

        - whether shares are available to borrow,
        - the cost of borrowing those shares, and
        - payments in lieu of dividends when applicable.
        """
    )


# ---------------------------------------------------------
# BORROW FEES AND SHORTABILITY
# ---------------------------------------------------------
st.header("Borrow Fees and Shortability")

with st.expander("Borrow fees, shortable shares, and utilization"):
    st.markdown(
        r"""
        **Shortable shares** are the shares that a broker currently has
        available to lend for short selling.

        **Utilization** measures how much of the available lending supply
        is already being borrowed. Securities with high utilization are
        generally more difficult to borrow.

        **Borrow fees** compensate the lender for making shares available.
        Borrow rates can vary substantially across securities and can
        change over time.

        For an illustrative constant share price, the daily borrow fee is

        $$
        \text{Daily Borrow Fee}
        =
        (N \cdot P)\frac{r_b}{360},
        $$

        where \(N\) is the number of shares shorted, \(P\) is the share
        price, and \(r_b\) is the annualized borrow rate. IBKR calculates the daily borrow fee using 
        a 360-day basis. 

        Borrow fees accrue on each calendar day that a settled short position is held.
        Over \(d\) days, assuming the share price and borrow rate remain constant,

        $$
        \text{Total Borrow Fee}
        =
        (N \cdot P)\frac{r_b}{360}d.
        $$
        """
    )


st.subheader("Illustrative Borrow-Fee Ranges")

# Temporary values. We will replace these after settling on
# defensible illustrative categories/ranges.
borrow_table = pd.DataFrame(
    {
        "Borrow Category": [
            "Very Easy to Borrow",
            "Easy to Borrow",
            "Moderately Difficult",
            "Hard to Borrow/Special",
        ],
        "Illustrative Borrow-Fee Range": [
            "0.1%-0.5%",
            "0.5%-1%",
            "1%-5%",
            "5%-20%+",
        ],
        "Typical Example": [
            "Broad-market ETFs, highly liquid large caps",
            "Many liquid U.S. stocks",
            "Securities with elevated borrow demand",
            "Scarce or heavily shorted securities",
        ],
    }
)

st.dataframe(
    borrow_table,
    hide_index=True,
    use_container_width=True,
)

st.caption(
    "These categories are intended only as general illustrations. "
    "Actual borrow availability and fees vary by security and over time."
)


# ---------------------------------------------------------
# BORROW-FEE SIMULATOR
# ---------------------------------------------------------
st.subheader("Borrow-Fee Simulator")

col1, col2, col3, col4 = st.columns(4)

with col1:
    security_type = st.selectbox(
        "Security type",
        [
            "Large-Cap Stock",
            "Mid-Cap Stock",
            "Small-Cap Stock",
            "Broad-Market ETF",
        ],
    )

with col2:
    share_price = st.number_input(
        "Share price ($)",
        min_value=0.01,
        value=100.00,
        step=1.00,
    )

with col3:
    shares = st.number_input(
        "Shares shorted",
        min_value=1,
        value=100,
        step=1,
    )

with col4:
    holding_period = st.selectbox(
        "Holding period",
        {
            "1 Week": 7,
            "1 Month": 30,
            "3 Months": 90,
            "6 Months": 180,
            "1 Year": 360,
        }.keys(),
    )

holding_days = {
    "1 Week": 7,
    "1 Month": 30,
    "3 Months": 90,
    "6 Months": 180,
    "1 Year": 360,
}[holding_period]

# Temporary illustrative rates until we settle the table.
illustrative_rates = {
    "Large-Cap Stock": 0.50,
    "Mid-Cap Stock": 1.00,
    "Small-Cap Stock": 2.00,
    "Broad-Market ETF": 0.25,
}

borrow_rate_percent = illustrative_rates[security_type]
borrow_rate = borrow_rate_percent / 100

position_value = shares * share_price
daily_fee = position_value * borrow_rate / 360
total_fee = daily_fee * holding_days

st.caption(
    "Simulation assumption: the share price and illustrative borrow rate "
    "remain constant over the selected holding period. You may enter a "
    "security's actual price or an arbitrary price for illustration. "
    "The borrow rate is not a current IBKR quote."
)

metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric(
    "Position Value",
    f"${position_value:,.2f}",
)

metric2.metric(
    "Illustrative Annual Rate",
    f"{borrow_rate_percent:.2f}%",
)

metric3.metric(
    "Daily Borrow Fee",
    f"${daily_fee:,.2f}",
)

metric4.metric(
    "Total Borrow Fee",
    f"${total_fee:,.2f}",
)


# ---------------------------------------------------------
# DIVIDENDS AND SHORT POSITIONS
# ---------------------------------------------------------
st.header("Dividends and Short Positions")

with st.expander("Understanding dividend dates"):
    st.markdown(
        """
        A dividend involves several dates that serve different purposes.

        **Declaration date:**  
        The company announces the dividend.

        **Ex-dividend date:**  
        The date on which the stock begins trading without entitlement to
        the upcoming dividend.

        **Record date:**  
        The company identifies shareholders entitled to receive the
        dividend.

        **Payment date:**  
        The dividend is distributed to eligible shareholders.

        The important distinction is that the order in which these dates
        are **announced** is not the same as their eventual order on the
        calendar.

        **Announcement timeline**

        Declaration → Record & Payment announced → Ex-dividend determined

        **Calendar timeline**

        Declaration → Ex-dividend → Record → Payment
        """
    )


# ---------------------------------------------------------
# DIVIDEND / PIL SIMULATOR
# ---------------------------------------------------------
st.subheader("Dividend & Short-Sale Simulator")

st.caption(
    "Choose when the short position is opened relative to the ex-dividend "
    "date. The simulator shows whether a payment in lieu is owed and why."
)

col1, col2, col3 = st.columns(3)

with col1:
    short_timing = st.radio(
        "When is the short position opened?",
        options=[
            "Before the ex-dividend",
            "On/after ex-dividend",
        ],
        index=0,
        horizontal=True,
    )

with col2:
    dividend_shares = st.number_input(
        "Shares shorted",
        min_value=1,
        value=100,
        step=1,
        key="dividend_shares",
    )

with col3:
    dividend_per_share = st.number_input(
        "Dividend per share ($)",
        min_value=0.01,
        value=0.50,
        step=0.05,
    )


# ---------------------------------------------------------
# DETERMINE SCENARIO
# ---------------------------------------------------------
pil_owed = short_timing == "Before the ex-dividend"

pil_amount = (
    dividend_shares * dividend_per_share
    if pil_owed
    else 0.0
)

# Position the short-opening marker according to the selected scenario.
# These are conceptual positions rather than calendar dates.
short_position = 32 if pil_owed else 55


# ---------------------------------------------------------
# VISUAL TIMELINE
# ---------------------------------------------------------
events = [
    ("Declaration", 5, "event"),
    ("Ex-Dividend", 45, "event"),
    ("Record", 70, "event"),
    ("Payment", 95, "event"),
    ("Short Opened", short_position, "short"),
]

timeline_markers = ""

for label, position, marker_type in events:
    marker_class = "short-event" if marker_type == "short" else "regular-event"

    timeline_markers += f"""
    <div class="timeline-event {marker_class}"
         style="left: {position}%;">
        <div class="event-label">{label}</div>
        <div class="event-dot"></div>
    </div>
    """

st.markdown(
    f"""
    <style>
    .timeline {{
        position: relative;
        height: 90px;
        margin: 28px 25px 12px 25px;
    }}

    .timeline-track {{
        position: absolute;
        left: 5%;
        right: 5%;
        top: 50px;
        height: 4px;
        background: #6b7280;
        border-radius: 4px;
    }}

    .timeline-event {{
        position: absolute;
        top: 0;
        transform: translateX(-50%);
        width: 170px;
        text-align: center;
    }}

    .event-label {{
        height: 34px;
        display: flex;
        align-items: flex-end;
        justify-content: center;
        font-size: 1.05rem;
        font-weight: 600;
        white-space: nowrap;
    }}

    .event-dot {{
        width: 16px;
        height: 16px;
        margin: 8px auto 0 auto;
        border-radius: 50%;
        background: #d1d5db;
    }}

    .short-event .event-label {{
        color: #ff4b4b;
        font-weight: 700;
    }}

    .short-event .event-dot {{
        width: 20px;
        height: 20px;
        margin-top: 6px;
        background: #ff4b4b;
    }}
    </style>

    <div class="timeline">
        <div class="timeline-track"></div>
        {timeline_markers}
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# RESULTS
# ---------------------------------------------------------
result1, result2 = st.columns(2)

result1.metric(
    "Payment in Lieu Owed?",
    "Yes" if pil_owed else "No",
)

result2.metric(
    "Payment in Lieu",
    f"${pil_amount:,.2f}",
)


# ---------------------------------------------------------
# EXPLANATION
# ---------------------------------------------------------
if pil_owed:
    st.success(
        f"Because the short position was opened before the ex-dividend date, the lender is entitled to compensation for the dividend they would otherwise have received. With {dividend_shares:,} shares short and a \${dividend_per_share:,.2f} dividend per share, the short seller owes a \${pil_amount:,.2f} payment in lieu."
    )
else:
    st.info(
        "Because the short position was opened on or after the ex-dividend date, the short seller does not owe the lender a payment in lieu for this dividend."
    )
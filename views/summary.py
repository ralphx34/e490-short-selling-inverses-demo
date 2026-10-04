import streamlit as st


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

    .summary-box {
        padding: 14px 18px;
        margin: 14px 0;
        border-radius: 8px;
        background: rgba(59, 130, 246, 0.10);
        border: 1px solid rgba(59, 130, 246, 0.30);
        font-size: 1.15rem;
        line-height: 1.6;
    }

    .takeaway-box {
        padding: 14px 18px;
        margin: 18px 0 4px 0;
        border-radius: 8px;
        background: rgba(34, 197, 94, 0.10);
        border: 1px solid rgba(34, 197, 94, 0.30);
        font-size: 1.15rem;
        line-height: 1.6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.title("Summary")

st.markdown(
    """
    This page reviews the main concepts from the demonstration. Use the
    sections below to revisit the mechanics of short selling, margin and
    financing, leveraged and inverse ETFs, and the comparison between direct
    short exposure and inverse ETFs.
    """
)


# =========================================================
# FINAL TAKEAWAYS
# =========================================================
st.header("Key Takeaways")

st.markdown(
    """
    <div class="takeaway-box">
    <b>1. Short selling has mechanics and costs beyond simply taking the
    negative of a stock's return.</b><br>
    Shares must be borrowed, borrow fees may apply, dividend obligations can
    arise, and the position must satisfy margin requirements.
    </div>

    <div class="takeaway-box">
    <b>2. Borrowing shares and borrowing cash are different.</b><br>
    Borrow fees compensate for borrowed securities, while margin-loan interest
    is the financing cost of borrowed cash.
    </div>

    <div class="takeaway-box">
    <b>3. Inverse ETFs provide bearish exposure without directly shorting the
    underlying.</b><br>
    Their exposure is implemented through the fund and targets a multiple of
    the underlying's daily return.
    </div>

    <div class="takeaway-box">
    <b>4. Daily reset and compounding matter over multi-day horizons.</b><br>
    Leveraged and inverse ETF performance is path dependent, so long-horizon
    returns need not equal the leverage factor times the underlying's
    cumulative return.
    </div>

    <div class="takeaway-box">
    <b>5. A direct short position and an inverse ETF are not interchangeable
    strategies.</b><br>
    Both can provide bearish exposure, but their mechanics, costs, and
    performance paths differ.
    </div>
    """,
    unsafe_allow_html=True,
)

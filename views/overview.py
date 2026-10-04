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

    [data-testid="stCaptionContainer"] p {
        font-size: 1.05rem;
        line-height: 1.5;
    }

    .module-card {
        padding: 16px 18px;
        margin-bottom: 14px;
        border: 1px solid rgba(128, 128, 128, 0.30);
        border-radius: 8px;
        min-height: 230px;
    }

    .module-number {
        font-size: 0.95rem;
        font-weight: 700;
        opacity: 0.70;
        margin-bottom: 4px;
    }

    .module-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .module-text {
        font-size: 1.08rem;
        line-height: 1.55;
    }

    .flow-box {
        padding: 14px 18px;
        margin: 8px 0;
        border: 1px solid rgba(128, 128, 128, 0.30);
        border-radius: 8px;
        text-align: center;
        font-size: 1.05rem;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.title("Short Selling and Inverse ETFs")

st.markdown(
    """
    This interactive demonstration explores two ways to obtain bearish
    exposure: **direct short selling** and **inverse ETFs**.

    The pages begin with the mechanics and costs of short selling, then
    introduce margin requirements and financing. The demonstration then
    explains how leveraged and inverse ETFs work before bringing the two
    approaches together in a historical comparison.
    """
)


# =========================================================
# OVERVIEW
# =========================================================
st.header("Overview")

row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.markdown(
        """
        <div class="module-card">
            <div class="module-number">SECTION 1</div>
            <div class="module-title">Short Selling & Dividends</div>
            <div class="module-text">
                Introduces the mechanics of short selling, shortable shares,
                utilization, and borrow fees. It also explains dividend dates
                and when a short seller may owe a payment in lieu of a
                dividend.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with row1_col2:
    st.markdown(
        """
        <div class="module-card">
            <div class="module-number">SECTION 2</div>
            <div class="module-title">Margin Requirements & Financing</div>
            <div class="module-text">
                Explains margin, margin-loan financing, initial and
                maintenance requirements, Reg T end-of-day requirements, and
                margin deficiencies. An integrated simulation shows how these
                mechanics interact for the same position.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown(
        """
        <div class="module-card">
            <div class="module-number">SECTION 3</div>
            <div class="module-title">Leveraged & Inverse ETFs</div>
            <div class="module-text">
                Introduces leveraged and inverse ETFs, the daily reset,
                compounding, path dependence, and volatility decay. A
                two-day example illustrates how leveraged daily returns
                compound over time.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with row2_col2:
    st.markdown(
        """
        <div class="module-card">
            <div class="module-number">SECTION 4</div>
            <div class="module-title">Short Selling vs. Inverse ETFs</div>
            <div class="module-text">
                Brings the two approaches together. The final section explains
                why direct short exposure and a −1× inverse ETF are not the
                same position and compares their historical performance paths.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# DEMONSTRATION FLOW
# =========================================================
st.header("Demonstration Flow")

flow1, arrow1, flow2, arrow2, flow3, arrow3, flow4 = st.columns(
    [1.6, 0.3, 1.6, 0.3, 1.6, 0.3, 1.6],
    vertical_alignment="center",
)

with flow1:
    st.markdown(
        '<div class="flow-box">Short-Sale<br>Mechanics</div>',
        unsafe_allow_html=True,
    )

with arrow1:
    st.markdown(
        "<div style='text-align:center; font-size:1.5rem;'>→</div>",
        unsafe_allow_html=True,
    )

with flow2:
    st.markdown(
        '<div class="flow-box">Margin &<br>Financing</div>',
        unsafe_allow_html=True,
    )

with arrow2:
    st.markdown(
        "<div style='text-align:center; font-size:1.5rem;'>→</div>",
        unsafe_allow_html=True,
    )

with flow3:
    st.markdown(
        '<div class="flow-box">Inverse ETF<br>Mechanics</div>',
        unsafe_allow_html=True,
    )

with arrow3:
    st.markdown(
        "<div style='text-align:center; font-size:1.5rem;'>→</div>",
        unsafe_allow_html=True,
    )

with flow4:
    st.markdown(
        '<div class="flow-box">Historical<br>Comparison</div>',
        unsafe_allow_html=True,
    )


# =========================================================
# BEFORE YOU BEGIN
# =========================================================
with st.expander("What should I know before starting?"):
    st.markdown(
        """
        The demonstration assumes basic familiarity with stock prices,
        percentage returns, and long positions.

        The short-selling, margin, leveraged-ETF, and inverse-ETF mechanics
        needed for the demonstration are introduced within the pages
        themselves.

        Use the sidebar to move through the sections in order or return to a
        specific section as needed.
        """
    )

import streamlit as st


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
        font-size: 2.1rem;
    }

    /* Teaching callout */
    .concept-box {
        padding: 14px 18px;
        margin: 16px 0 4px 0;
        border-radius: 8px;
        background: rgba(59, 130, 246, 0.10);
        border: 1px solid rgba(59, 130, 246, 0.30);
        font-size: 1.15rem;
    }

    /* Final takeaway */
    .takeaway-box {
        padding: 14px 18px;
        margin: 16px 0 4px 0;
        border-radius: 8px;
        background: rgba(34, 197, 94, 0.10);
        border: 1px solid rgba(34, 197, 94, 0.30);
        font-size: 1.15rem;
    }

    /* Return arrows in two-day example */
    .return-arrow {
        text-align: center;
        padding-top: 34px;
        font-size: 1.15rem;
        font-weight: 600;
        white-space: nowrap;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.title("Leveraged & Inverse ETFs")


# =========================================================
# WHAT ARE LEVERAGED AND INVERSE ETFS?
# =========================================================
st.header("Leveraged & Inverse ETFs")

with st.expander("What is a leveraged ETF?"):
    st.markdown(
        r"""
        A **leveraged ETF** is designed to deliver a multiple of the
        **daily return** of an underlying asset or index.

        The leverage factor is denoted by \(L\).

        - \(L = 2\): targets twice the underlying's daily return.
        - \(L = 3\): targets three times the underlying's daily return.
        - \(L = -1\): targets the opposite of the underlying's daily return.
        - \(L = -2\): targets twice the opposite of the underlying's daily
          return.

        An ETF with a negative leverage factor is an **inverse ETF**.

        The fund obtains this exposure through its portfolio, which may
        include instruments such as swaps, futures, options, and cash.
        Purchasing an inverse ETF therefore does **not** mean that the
        investor has directly opened a short position in the underlying.

        $$
        V_t = V_{t-1}(1 + LR_t)
        $$

        where $V_t$ is the net asset value per share of the leveraged ETF at time t.
        """
    )

    st.markdown(
        """
        <div class="concept-box">
            <b>Interpretation:</b> A leveraged or inverse ETF changes in
            response to a specified multiple of the underlying asset's
            daily return.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# THE DAILY RESET
# =========================================================
st.header("The Daily Reset")

with st.expander("Why does the ETF reset every day?"):
    st.markdown(
        r"""
        The leverage target applies to the **next daily return**, not to the
        return over an arbitrary holding period.

        After the underlying asset moves, the fund's exposure must therefore
        be adjusted so that it once again targets \(L\) times the
        underlying's return for the next trading day.

        This daily rebalancing is what is meant by the ETF's
        **daily reset**.

        As a result, a leveraged or inverse ETF should not generally be
        interpreted as promising \(L\) times the underlying's cumulative
        return over a week, month, year, or other multi-day horizon.
        """
    )

    st.markdown(
        """
        <div class="concept-box">
            <b>Daily target ≠ long-horizon target</b><br><br>

            A −1× inverse ETF targets −1× the underlying's
            daily return, not −1× its return over an arbitrary
            holding period.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# COMPOUNDING AND PATH DEPENDENCE
# =========================================================
st.header("Compounding & Path Dependence")

with st.expander("Why does the return path matter?"):
    st.markdown(
        r"""
        Daily leveraged returns are applied sequentially and therefore
        **compound over time**.

        Over multiple trading days, the ETF's value can be represented as

        $$
        V_T
        =
        V_0
        \prod_{t=1}^{T}(1 + LR_t).
        $$

        In plain language: start with the ETF's initial value and apply each
        day's leveraged return one after another.

        Because the daily returns are compounded, the final value depends on
        the sequence of returns experienced along the way. This is called
        **path dependence**.
        """
    )


# =========================================================
# VOLATILITY DECAY
# =========================================================
st.header("Volatility Decay")

with st.expander("Why can volatility reduce the ETF's value?"):
    st.markdown(
        """
        Percentage gains and losses compound multiplicatively.

        A loss therefore requires a larger percentage gain to recover. For
        example, after a 10% loss, a position must gain more than 10% to
        return to its original value.

        Leveraged and inverse ETFs magnify daily movements according to their
        leverage factor. Repeated back-and-forth movements can therefore
        reduce compounded wealth even when the underlying asset experiences
        relatively little net movement over the full period.

        This effect is commonly described as **volatility decay**.

        The important point is not that an inverse ETF must always lose
        value. Rather, volatility and the sequence of daily returns affect
        its multi-day performance because the fund targets leveraged returns
        one day at a time.
        """
    )

# ---------------------------------------------------------
# VOLATILITY DECAY EXAMPLE
# ---------------------------------------------------------
st.subheader("Volatility Decay Example")

st.markdown(
    """
    Consider two equal and opposite daily price movements in the underlying:

    - **Day 1:** +10%  
    - **Day 2:** −10%

    The underlying ends only slightly below where it started, while a
    **3× leveraged ETF** experiences much larger compounded losses.
    """
)

example_data = {
    "": ["Underlying", "3× Leveraged ETF"],
    "Start": ["$100.00", "$100.00"],
    "Day 1": ["$110.00", "$130.00"],
    "Day 2": ["$99.00", "$91.00"],
    "Two-Day Return": ["−1.00%", "−9.00%"],
}

st.dataframe(
    example_data,
    use_container_width=True,
    hide_index=True,
)

calc1, calc2 = st.columns(2)

with calc1:
    st.markdown(
        "<div style='text-align:center; font-size:1.2rem; font-weight:600;'>"
        "Underlying"
        "</div>",
        unsafe_allow_html=True,
    )
    st.latex(r"100(1.10)(0.90)=99")

with calc2:
    st.markdown(
        "<div style='text-align:center; font-size:1.2rem; font-weight:600;'>"
        "3× Leveraged ETF"
        "</div>",
        unsafe_allow_html=True,
    )
    st.latex(r"100(1.30)(0.70)=91")

st.markdown(
    """
    The underlying's +10% and −10% daily movements leave it **1% below**
    its starting value. The 3× leveraged ETF experiences +30% and −30%
    daily returns and ends **9% below** its starting value.

    This illustrates the basic intuition behind **volatility decay**:
    magnifying back-and-forth daily movements can produce substantially
    larger compounded losses even when the underlying's total change is small.
    """
)

st.markdown(
    """
    <div class="takeaway-box"><b>What is special about leveraged and inverse ETFs?</b><br><br>
    They provide leveraged or inverse exposure through a traded fund, reset
    their target exposure daily, and compound those daily returns over time.
    Their long-horizon return can therefore differ substantially from simply
    multiplying the underlying asset's cumulative return by the leverage
    factor.</div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# OPTIONAL MATHEMATICAL DETAIL
# =========================================================
st.header("Optional Mathematical Detail")

with st.expander(
    "Optional: Mathematical derivation of volatility decay"
):
    st.markdown(
        r"""
        **This derivation is not needed for the remainder of the
        demonstration.**

        Starting from the daily leveraged-return relationship,

        $$
        V_T
        =
        V_0
        \prod_{t=1}^{T}(1 + LR_t),
        $$

        take logarithms:

        $$
        \ln\left(\frac{V_T}{V_0}\right)
        =
        \sum_{t=1}^{T}\ln(1 + LR_t).
        $$

        For small daily returns, use the approximation

        $$
        \ln(1+x)
        \approx
        x-\frac{x^2}{2}.
        $$

        Applying this approximation gives

        $$
        \ln\left(\frac{V_T}{V_0}\right)
        \approx
        L\sum_{t=1}^{T}R_t
        -
        \frac{L^2}{2}
        \sum_{t=1}^{T}R_t^2.
        $$

        The second term is negative and becomes larger in magnitude when
        squared daily returns are larger. This provides the mathematical
        intuition for why greater volatility can reduce compounded
        leveraged-ETF performance.

        The approximation is included only to show the mathematical source
        of the effect. It is not necessary for understanding how leveraged
        and inverse ETFs operate.
        """
    )
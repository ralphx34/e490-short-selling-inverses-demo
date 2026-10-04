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

    [data-testid="stWidgetLabel"] p {
        font-size: 1.1rem;
    }

    [data-testid="stCaptionContainer"] p {
        font-size: 1.05rem;
        line-height: 1.5;
    }

    [data-testid="stMetricLabel"] p {
        font-size: 1.05rem;
    }

    [data-testid="stMetricValue"] {
        font-size: 2.25rem;
    }

    input {
        font-size: 1.1rem !important;
    }

    [data-baseweb="select"] {
        font-size: 1.1rem;
    }

    .financing-box {
        padding: 1rem 1.25rem;
        border: 1px solid rgba(128, 128, 128, 0.35);
        border-radius: 0.5rem;
        margin: 0.5rem 0 1rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.title("Margin Requirements & Financing")

st.markdown(
    """
    Review the definitions and mechanics below, then use the simulation to see
    how margin, margin-loan financing, and margin requirements interact for the
    same position.
    """
)

# =========================================================
# DEFINITIONS AND EXPLANATIONS
# =========================================================
st.header("Definitions & Explanations")

with st.expander("What is margin?"):
    st.markdown(
        """
        **Margin** is the portion of a financial position's value that must be
        financed using the investor's own capital, rather than borrowed funds,
        in order to support a leveraged position.

        A margin account can therefore allow an investor's capital to support
        a position whose total value is larger than the investor's own capital.

        IBKR allows short selling only on margin accounts.
        """
    )

with st.expander("What are margin-loan rates?"):
    st.markdown(
        r"""
        The **margin-loan interest rate** is the annualized interest rate paid
        on the borrowed cash balance in a margin account.

        Let \(L_t\) be the outstanding margin-loan balance on day \(t\) and
        \(r\) the annualized margin-loan interest rate. Daily interest is

        $$
        \text{Interest Payment}_t=L_t\frac{r}{360}.
        $$

        IBKR accrues margin interest daily and posts the accumulated interest
        monthly.

        A **borrow fee** is charged for borrowing shares to short. A
        **margin-loan rate** is charged for borrowing cash to finance trades.
        Short selling does not automatically create a margin loan.
        """
    )

with st.expander("What are margin requirements?"):
    st.markdown(
        """
        **Initial Margin** is the minimum amount of investor equity required
        to open a new position.

        **Maintenance Margin** is the minimum equity that must be maintained
        at all times after the position is opened.

        **Reg T End-of-Day Initial Margin** is the amount of equity the margin
        account must have at the market close to satisfy Regulation T initial
        margin rules.

        A **rules-based** system uses formulaic requirements and set
        percentages. A **risk-based** system considers the collective risk of
        the portfolio using simulated adverse scenarios.

        The presentation treats IBKR as operating under a rules-based system.
        """
    )

with st.expander("What are IBKR's margin requirements?"):

    long_col, short_col = st.columns(2)

    # -----------------------------------------------------
    # LONG POSITIONS
    # -----------------------------------------------------
    with long_col:
        st.markdown("### Long Positions")

        st.markdown(
            """
            | Requirement | IBKR Rule |
            |---|---|
            | Initial Margin | 25% × Stock Value |
            | Maintenance Margin | 25% × Stock Value |
            | Reg T End-of-Day Initial Margin | 50% × Stock Value |
            """
        )

    # -----------------------------------------------------
    # SHORT POSITIONS
    # -----------------------------------------------------
    with short_col:
        st.markdown("### Short Positions")

        st.markdown(
            r"""
            | Share Price | Initial / Maintenance Requirement |
            |---|---|
            | Above \$16.67 | 30% × Market Value of Stock |
            | Above \$5.00 and below \$16.67 | \$5.00 per share |
            | Below \$5.00 | 100% of Market Value of Stock |
            | At or below \$2.50 | \$2.50 per share |
            """
        )

        st.markdown(
            """
            **Reg T End-of-Day Initial Margin:** Same requirement as for a long position.
            """
        )

with st.expander("What is a margin deficiency?"):
    st.markdown(
        r"""
        Let \(V\) be the current market value of the securities, \(E\) investor
        equity, and \(m\) the maintenance-margin requirement.

        A margin deficiency occurs when

        $$
        E < mV.
        $$

        In general, a margin call requires the investor to restore equity to
        the required level. The presentation notes that IBKR instead uses
        real-time liquidation when an account has a margin deficiency.
        """
    )

# =========================================================
# ONE CONTINUOUS EXAMPLE
# =========================================================
st.header("Integrated Margin Simulation")

st.markdown(
    """
    The simulation below uses one position throughout so that the investment
    return, financing cost, and margin requirements all refer to the same
    example.
    """
)

st.subheader("Set Up the Position")

c1, c2, c3 = st.columns(3)
with c1:
    investor_capital = st.number_input(
        "Investor capital ($)", min_value=100.0, value=5000.0, step=500.0
    )
with c2:
    initial_margin_percent = st.number_input(
        "Initial margin requirement (%)",
        min_value=1.0, max_value=100.0, value=50.0, step=5.0
    )
with c3:
    annual_interest_rate_percent = st.number_input(
        "Annual margin-loan interest rate (%)",
        min_value=0.0, value=9.0, step=0.25
    )

position_value = investor_capital / (initial_margin_percent / 100)
borrowed_cash = max(position_value - investor_capital, 0.0)

st.markdown(
    f"""
    **Position financing**

    \${investor_capital:,.2f} investor capital
    + \${borrowed_cash:,.2f} borrowed cash
    = **\${position_value:,.2f} invested**
    """
)

st.subheader("Change the Stock Return")

stock_return_percent = st.slider(
    "Stock return (%)", min_value=-25, max_value=25, value=25, step=1
)

current_position_value = position_value * (1 + stock_return_percent / 100)
position_pnl = current_position_value - position_value
return_on_capital = position_pnl / investor_capital

r1, r2, r3 = st.columns(3)
r1.metric("Current Position Value", f"${current_position_value:,.2f}")
r2.metric("Profit / Loss", f"${position_pnl:,.2f}")
r3.metric("Return on Investor Capital", f"{return_on_capital * 100:,.2f}%")

st.markdown(
    f"""
    A **{stock_return_percent:+.0f}%** stock return changes the
    \${position_value:,.2f} position by \${position_pnl:,.2f}. Relative to the
    investor's ${investor_capital:,.2f} of capital, the return is
    **{return_on_capital * 100:,.2f}%**.
    """
)

st.subheader("Accrue Margin-Loan Interest")

holding_days = st.slider("Days held", min_value=1, max_value=30, value=1, step=1)
annual_interest_rate = annual_interest_rate_percent / 100

loan_balance = borrowed_cash
total_interest = 0.0
daily_rows = []

for day in range(1, holding_days + 1):
    starting_balance = loan_balance
    interest_payment = starting_balance * annual_interest_rate / 360
    ending_balance = starting_balance + interest_payment
    daily_rows.append({
        "Day": day,
        "Starting Loan Balance": starting_balance,
        "Interest Payment": interest_payment,
        "Ending Loan Balance": ending_balance,
    })
    total_interest += interest_payment
    loan_balance = ending_balance

day_one_interest = borrowed_cash * annual_interest_rate / 360

f1, f2, f3 = st.columns(3)
f1.metric("Initial Margin Loan", f"${borrowed_cash:,.2f}")
f2.metric("Day 1 Interest", f"${day_one_interest:,.2f}")
f3.metric("Total Interest Accrued", f"${total_interest:,.2f}")

st.markdown(
    f"After **{holding_days} day{'s' if holding_days != 1 else ''}**, "
    f"the margin-loan balance is **${loan_balance:,.2f}**."
)

with st.expander("Show daily loan-balance mechanics"):
    st.dataframe(
        [{
            "Day": row["Day"],
            "Starting Loan Balance": f"${row['Starting Loan Balance']:,.2f}",
            "Interest Payment": f"${row['Interest Payment']:,.2f}",
            "Ending Loan Balance": f"${row['Ending Loan Balance']:,.2f}",
        } for row in daily_rows],
        use_container_width=True,
        hide_index=True,
    )

st.subheader("Check the Margin Requirements")

m1, m2 = st.columns(2)
with m1:
    maintenance_margin_percent = st.number_input(
        "Maintenance margin requirement (%)",
        min_value=0.0, max_value=100.0, value=25.0, step=5.0
    )
with m2:
    reg_t_margin_percent = st.number_input(
        "Reg T end-of-day initial margin (%)",
        min_value=0.0, max_value=100.0, value=50.0, step=5.0
    )

account_equity = current_position_value - loan_balance
maintenance_required_equity = (
    current_position_value * maintenance_margin_percent / 100
)
reg_t_required_equity = current_position_value * reg_t_margin_percent / 100

maintenance_cushion = account_equity - maintenance_required_equity
reg_t_cushion = account_equity - reg_t_required_equity
maintenance_satisfied = maintenance_cushion >= 0
reg_t_satisfied = reg_t_cushion >= 0

q1, q2, q3 = st.columns(3)
q1.metric("Account Equity", f"${account_equity:,.2f}")
q2.metric("Required Maintenance Equity", f"${maintenance_required_equity:,.2f}")
q3.metric("Maintenance Margin Cushion", f"${maintenance_cushion:,.2f}")

if maintenance_satisfied:
    st.success(
        f"MAINTENANCE REQUIREMENT SATISFIED — Equity exceeds the requirement "
        f"by ${maintenance_cushion:,.2f}."
    )
else:
    st.error(
        f"MARGIN DEFICIENCY — Equity is ${abs(maintenance_cushion):,.2f} "
        "below the maintenance requirement."
    )

st.markdown("#### Reg T End-of-Day Status")

if reg_t_satisfied:
    st.success(
        f"REG T REQUIREMENT SATISFIED — Equity exceeds the requirement "
        f"by ${reg_t_cushion:,.2f}."
    )
else:
    st.warning(
        f"BELOW REG T REQUIREMENT — Equity is ${abs(reg_t_cushion):,.2f} "
        "below the Reg T end-of-day requirement."
    )

if not maintenance_satisfied:
    st.error(
        "Under the IBKR mechanics described in the presentation, a margin "
        "deficiency can result in real-time liquidation rather than a "
        "conventional margin call."
    )

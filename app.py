import streamlit as st


st.set_page_config(
    page_title="IBKR Short Selling Laboratory",
    layout="wide",
)


pages = {
    "": [
        st.Page(
            "views/overview.py",
            title="Overview",
        ),
        st.Page(
            "views/short_selling_dividends.py",
            title="Short Selling & Dividends",
        ),
        st.Page(
            "views/margin_financing.py",
            title="Margin Financing",
        ),
        st.Page(
                "views/leveraged_inverse_etfs.py",
                title="Leveraged & Inverse ETFs",
        ),
        st.Page(
                "views/short_vs_inverse.py",
                title="Short Selling vs. Inverse ETFs",
        ),
        st.Page(
                "views/summary.py",
                title="Summary",
        ),
    ]
}


navigation = st.navigation(pages)
navigation.run()
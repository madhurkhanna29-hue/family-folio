import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Set Page Config for Mobile
st.set_page_config(page_title="FamilyFolio Pro", layout="wide")

# --- 1. DATASET ---
PORTFOLIO_DATA = {
    "Mother (acc1)": [{"sym": "BAJFINANCE.NS", "qty": 480, "avg": 325.88, "cur": "INR", "sec": "Financials"}, {"sym": "GUJGASLTD.NS", "qty": 22, "avg": 446.50, "cur": "INR", "sec": "Energy"}, {"sym": "HDFCBANK.NS", "qty": 80, "avg": 684.94, "cur": "INR", "sec": "Financials"}, {"sym": "ICICIBANK.NS", "qty": 87, "avg": 487.88, "cur": "INR", "sec": "Financials"}, {"sym": "JIOFIN.NS", "qty": 231, "avg": 48.33, "cur": "INR", "sec": "Financials"}, {"sym": "RELIANCE.NS", "qty": 462, "avg": 492.16, "cur": "INR", "sec": "Energy"}, {"sym": "TATAELXSI.NS", "qty": 7, "avg": 5957.76, "cur": "INR", "sec": "IT"}, {"sym": "VENUSPIPES.NS", "qty": 47, "avg": 684.99, "cur": "INR", "sec": "Metals"}],
    "Madhur (acc2)": [{"sym": "TSLA", "qty": 10, "avg": 251.30, "cur": "USD", "sec": "EV/Tech"}, {"sym": "BNKS.L", "qty": 716, "avg": 5.475, "cur": "USD", "sec": "ETF"}, {"sym": "CNYA.L", "qty": 1400, "avg": 5.4954, "cur": "USD", "sec": "ETF"}, {"sym": "ISLN.L", "qty": 195, "avg": 74.9366, "cur": "USD", "sec": "ETF"}, {"sym": "NVDA", "qty": 131, "avg": 116.84, "cur": "USD", "sec": "Semis"}, {"sym": "EQQQ.L", "qty": 4.0833, "avg": 349.71, "cur": "GBP_PENCE", "sec": "ETF"}, {"sym": "GLEN.L", "qty": 1000, "avg": 5.222, "cur": "GBP_PENCE", "sec": "Commodities"}],
    "Sonakshi (acc3)": [{"sym": "AMD", "qty": 15, "avg": 231.70, "cur": "USD", "sec": "Semis"}, {"sym": "CRWV", "qty": 40, "avg": 98.62, "cur": "USD", "sec": "AI/Cloud"}, {"sym": "ISLN.L", "qty": 100, "avg": 54.442, "cur": "USD", "sec": "ETF"}, {"sym": "CIFR", "qty": 300, "avg": 20.05, "cur": "USD", "sec": "Crypto"}, {"sym": "RHM.DE", "qty": 3, "avg": 1736.00, "cur": "EUR", "sec": "Defence"}, {"sym": "MRVL", "qty": 90, "avg": 77.52, "cur": "USD", "sec": "Semis"}, {"sym": "AMZN", "qty": 50, "avg": 185.13, "cur": "USD", "sec": "E-Comm"}, {"sym": "IONQ", "qty": 310, "avg": 40.26, "cur": "USD", "sec": "Quantum"}],
    "Mother-in-law (acc4)": [{"sym": "SOUTHWEST.NS", "qty": 445, "avg": 147.38, "cur": "INR", "sec": "Energy"}, {"sym": "BRPL.BO", "qty": 650, "avg": 122.50, "cur": "INR", "sec": "Industrials"}, {"sym": "ORIENTCER.NS", "qty": 1750, "avg": 43.99, "cur": "INR", "sec": "Materials"}, {"sym": "AARVI.NS", "qty": 480, "avg": 132.50, "cur": "INR", "sec": "Industrials"}, {"sym": "ARIES.NS", "qty": 150, "avg": 322.14, "cur": "INR", "sec": "Agriculture"}, {"sym": "NAHARPOLY.NS", "qty": 200, "avg": 274.14, "cur": "INR", "sec": "Materials"}, {"sym": "ALUFLUOR.BO", "qty": 115, "avg": 479.78, "cur": "INR", "sec": "Chemicals"}, {"sym": "FLUIDOM.BO", "qty": 60, "avg": 854.79, "cur": "INR", "sec": "Industrials"}, {"sym": "RUBFILA.BO", "qty": 600, "avg": 79.89, "cur": "INR", "sec": "Materials"}, {"sym": "KAMDHENU.NS", "qty": 1825, "avg": 27.67, "cur": "INR", "sec": "Materials"}, {"sym": "SARLAPOLY.NS", "qty": 475, "avg": 104.00, "cur": "INR", "sec": "Textiles"}, {"sym": "AEL.BO", "qty": 270, "avg": 177.52, "cur": "INR", "sec": "Industrials"}, {"sym": "AJANTSOY.BO", "qty": 1500, "avg": 34.25, "cur": "INR", "sec": "Agriculture"}, {"sym": "GROBTEA.NS", "qty": 40, "avg": 1135.42, "cur": "INR", "sec": "FMCG"}],
    "Father (acc6)": [{"sym": "SUNPHARMA.NS", "qty": 7, "avg": 352.20, "cur": "INR", "sec": "Pharma"}, {"sym": "NELCO.NS", "qty": 100, "avg": 134.50, "cur": "INR", "sec": "Technology"}, {"sym": "DLF.NS", "qty": 50, "avg": 137.50, "cur": "INR", "sec": "Real Estate"}, {"sym": "GUJGASLTD.NS", "qty": 2005, "avg": 232.60, "cur": "INR", "sec": "Utilities"}, {"sym": "ELECON.NS", "qty": 100, "avg": 178.48, "cur": "INR", "sec": "Industrials"}, {"sym": "MOLDTECH.NS", "qty": 103, "avg": 247.45, "cur": "INR", "sec": "Industrials"}, {"sym": "ASTRAL.NS", "qty": 33, "avg": 1559, "cur": "INR", "sec": "Materials"}]
}

# --- 2. LOGIC & CACHING ---
st.title("📈 FamilyFolio Pro Dashboard")

# Selection controls
selection = st.sidebar.selectbox("Account", ["Combined"] + list(PORTFOLIO_DATA.keys()))
timeframe = st.sidebar.selectbox("Timeframe", ["1d", "5d", "1mo", "6mo", "1y", "max"], index=4)

@st.cache_data(ttl=600)
def get_data(tf):
    all_syms = list(set([h['sym'] for acc in PORTFOLIO_DATA.values() for h in acc]))
    # For '1d' timeframe, we need minute data for a smooth line
    interval = "1m" if tf == "1d" else "1h" if tf == "5d" else "1d"
    
    hist = yf.download(all_syms, period=tf, interval=interval)['Close']
    fx = yf.download(["USDINR=X", "GBPINR=X", "EURINR=X"], period="1d")['Close'].iloc[-1]
    rates = {"USD": fx["USDINR=X"], "GBP": fx["GBPINR=X"], "EUR": fx["EURINR=X"], "INR": 1.0}
    return hist, rates

try:
    hist, rates = get_data(timeframe)
    latest_prices = hist.iloc[-1]
    
    # Process Data
    rows = []
    daily_trend = pd.Series(0, index=hist.index)
    
    target_holdings = []
    if selection == "Combined":
        for acc in PORTFOLIO_DATA.values(): target_holdings.extend(acc)
    else:
        target_holdings = PORTFOLIO_DATA[selection]

    for h in target_holdings:
        inr_rate = rates["GBP"] if h['cur'] == "GBP_PENCE" else rates[h['cur']]
        raw_price = latest_prices[h['sym']]
        
        # Current Metrics
        cur_p = raw_price/100 if h['cur'] == "GBP_PENCE" else raw_price
        val_inr = h['qty'] * cur_p * inr_rate
        inv_inr = h['qty'] * h['avg'] * inr_rate
        pnl = val_inr - inv_inr
        
        rows.append({
            "Account": selection, "Symbol": h['sym'], "Sector": h['sec'],
            "Value (INR)": val_inr, "P&L": pnl, 
            "Gain %": (pnl/inv_inr*100) if inv_inr != 0 else 0
        })
        
        # Timeseries Logic
        price_series = hist[h['sym']]
        if h['cur'] == "GBP_PENCE": price_series = price_series / 100
        daily_trend += (price_series * h['qty'] * inr_rate)

    df = pd.DataFrame(rows)

    # --- 3. UI RENDERING ---
    
    # Summary Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Current Value", f"₹{df['Value (INR)'].sum():,.0f}")
    c2.metric("Total P&L", f"₹{df['P&L'].sum():,.0f}")
    c3.metric("Return", f"{(df['P&L'].sum()/(df['Value (INR)'].sum()-df['P&L'].sum())*100):.2f}%")

    # Trend Chart
    st.subheader(f"Performance Trend ({timeframe.upper()})")
    fig_line = px.line(daily_trend, labels={"value": "Portfolio Value (₹)", "index": "Time"})
    fig_line.update_layout(showlegend=False, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_line, use_container_width=True)

    # Allocation & Table
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.subheader("Allocation")
        fig_sun = px.sunburst(df, path=['Account', 'Sector', 'Symbol'], values='Value (INR)',
                              color='Gain %', color_continuous_scale='RdYlGn', range_color=[-15, 15])
        st.plotly_chart(fig_sun, use_container_width=True)

    with col_right:
        st.subheader("Top Holdings")
        st.dataframe(df.sort_values("Value (INR)", ascending=False)[["Symbol", "Value (INR)", "Gain %"]], 
                     use_container_width=True, hide_index=True)

except Exception as e:
    st.info("Fetching data from Yahoo Finance... please wait.")
    st.error(str(e))

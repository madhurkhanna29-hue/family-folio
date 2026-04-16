import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime

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
st.title("👨‍👩‍👧‍👦 FamilyFolio Pro Dashboard")

selection = st.sidebar.selectbox("Active View", ["Combined"] + list(PORTFOLIO_DATA.keys()))
timeframe = st.sidebar.selectbox("Performance Timeframe", ["5d", "1mo", "6mo", "1y", "YTD", "max"], index=3)

@st.cache_data(ttl=3600)
def get_historical_data(tf):
    all_syms = list(set([h['sym'] for acc in PORTFOLIO_DATA.values() for h in acc]))
    
    # Calculate YTD start if needed
    if tf == "YTD":
        start_date = f"{datetime.now().year}-01-01"
        hist = yf.download(all_syms, start=start_date)['Close']
    else:
        hist = yf.download(all_syms, period=tf)['Close']
        
    hist = hist.ffill().bfill()
    
    fx = yf.download(["USDINR=X", "GBPINR=X", "EURINR=X"], period="1d")['Close'].iloc[-1]
    rates = {"USD": fx["USDINR=X"], "GBP": fx["GBPINR=X"], "EUR": fx["EURINR=X"], "INR": 1.0}
    return hist, rates

try:
    hist, rates = get_historical_data(timeframe)
    latest_prices = hist.iloc[-1]
    
    # Process Current State
    rows = []
    performance_map = {} # Store normalized series for each account

    # 1. Calculate Individual & Combined Performance Series
    for acc_name, holdings in PORTFOLIO_DATA.items():
        acc_daily_val = pd.Series(0, index=hist.index)
        
        for h in holdings:
            inr_rate = rates["GBP"] if h['cur'] == "GBP_PENCE" else rates[h['cur']]
            
            # Timeseries for chart
            p_series = hist[h['sym']]
            if h['cur'] == "GBP_PENCE": p_series = p_series / 100
            acc_daily_val += (p_series * h['qty'] * inr_rate)
            
            # Metrics for current selection
            if selection == "Combined" or selection == acc_name:
                ltp = latest_prices[h['sym']]
                cur_p = ltp/100 if h['cur'] == "GBP_PENCE" else ltp
                val_inr = h['qty'] * cur_p * inr_rate
                inv_inr = h['qty'] * h['avg'] * inr_rate
                pnl = val_inr - inv_inr
                rows.append({"Account": acc_name, "Symbol": h['sym'], "Sector": h['sec'], "Value (INR)": val_inr, "P&L": pnl, "Gain %": (pnl/inv_inr*100) if inv_inr != 0 else 0})
        
        # Normalize account series to Base 100
        performance_map[acc_name] = (acc_daily_val / acc_daily_val.iloc[0]) * 100

    # Create Combined series
    combined_val = sum(performance_map.values()) / len(performance_map) # Simple average for trend
    performance_map["Combined"] = (combined_val / combined_val.iloc[0]) * 100
    
    df = pd.DataFrame(rows)

    # --- 3. UI RENDERING ---
    
    # Top Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Value", f"₹{df['Value (INR)'].sum():,.0f}")
    c2.metric("P&L", f"₹{df['P&L'].sum():,.0f}")
    c3.metric("Acc. Return", f"{(df['P&L'].sum()/(df['Value (INR)'].sum()-df['P&L'].sum())*100):.2f}%")

    # --- PERFORMANCE CHART (Base 100) ---
    st.subheader(f"Relative Performance Index ({timeframe})")
    
    if selection == "Combined":
        # Show all accounts as separate lines
        plot_df = pd.DataFrame(performance_map)
        fig_line = px.line(plot_df, labels={"value": "Index (Base 100)", "index": "Date"})
    else:
        # Show only selected account vs Combined Benchmark
        plot_df = pd.DataFrame({selection: performance_map[selection], "Combined": performance_map["Combined"]})
        fig_line = px.line(plot_df, labels={"value": "Index (Base 100)", "index": "Date"})

    fig_line.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_line, use_container_width=True)

    # Allocation & Table
    col_left, col_right = st.columns([1, 1.2])
    with col_left:
        st.subheader("Asset Split")
        fig_sun = px.sunburst(df, path=['Account', 'Sector', 'Symbol'], values='Value (INR)',
                              color='Gain %', color_continuous_scale='RdYlGn', range_color=[-15, 15])
        st.plotly_chart(fig_sun, use_container_width=True)

    with col_right:
        st.subheader("Holdings Details")
        st.dataframe(df.sort_values("Value (INR)", ascending=False), use_container_width=True, hide_index=True)

except Exception as e:
    st.info("Generating historical performance reports...")
    st.error(str(e))

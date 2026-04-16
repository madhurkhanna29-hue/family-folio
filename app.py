import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Set Page Config for Mobile
st.set_page_config(page_title="FamilyFolio", layout="wide")

# --- 1. DATASET ---
PORTFOLIO_DATA = {
    "Mother (acc1)": [{"sym": "BAJFINANCE.NS", "qty": 480, "avg": 325.88, "cur": "INR", "sec": "Financials"}, {"sym": "GUJGASLTD.NS", "qty": 22, "avg": 446.50, "cur": "INR", "sec": "Energy"}, {"sym": "HDFCBANK.NS", "qty": 80, "avg": 684.94, "cur": "INR", "sec": "Financials"}, {"sym": "ICICIBANK.NS", "qty": 87, "avg": 487.88, "cur": "INR", "sec": "Financials"}, {"sym": "JIOFIN.NS", "qty": 231, "avg": 48.33, "cur": "INR", "sec": "Financials"}, {"sym": "RELIANCE.NS", "qty": 462, "avg": 492.16, "cur": "INR", "sec": "Energy"}, {"sym": "TATAELXSI.NS", "qty": 7, "avg": 5957.76, "cur": "INR", "sec": "IT"}, {"sym": "VENUSPIPES.NS", "qty": 47, "avg": 684.99, "cur": "INR", "sec": "Metals"}],
    "Madhur (acc2)": [{"sym": "TSLA", "qty": 10, "avg": 251.30, "cur": "USD", "sec": "EV/Tech"}, {"sym": "BNKS.L", "qty": 716, "avg": 5.475, "cur": "USD", "sec": "ETF"}, {"sym": "CNYA.L", "qty": 1400, "avg": 5.4954, "cur": "USD", "sec": "ETF"}, {"sym": "ISLN.L", "qty": 195, "avg": 74.9366, "cur": "USD", "sec": "ETF"}, {"sym": "NVDA", "qty": 131, "avg": 116.84, "cur": "USD", "sec": "Semis"}, {"sym": "EQQQ.L", "qty": 4.0833, "avg": 349.71, "cur": "GBP_PENCE", "sec": "ETF"}, {"sym": "GLEN.L", "qty": 1000, "avg": 5.222, "cur": "GBP_PENCE", "sec": "Commodities"}],
    "Sonakshi (acc3)": [{"sym": "AMD", "qty": 15, "avg": 231.70, "cur": "USD", "sec": "Semis"}, {"sym": "CRWV", "qty": 40, "avg": 98.62, "cur": "USD", "sec": "AI/Cloud"}, {"sym": "ISLN.L", "qty": 100, "avg": 54.442, "cur": "USD", "sec": "ETF"}, {"sym": "CIFR", "qty": 300, "avg": 20.05, "cur": "USD", "sec": "Crypto"}, {"sym": "RHM.DE", "qty": 3, "avg": 1736.00, "cur": "EUR", "sec": "Defence"}, {"sym": "MRVL", "qty": 90, "avg": 77.52, "cur": "USD", "sec": "Semis"}, {"sym": "AMZN", "qty": 50, "avg": 185.13, "cur": "USD", "sec": "E-Comm"}, {"sym": "IONQ", "qty": 310, "avg": 40.26, "cur": "USD", "sec": "Quantum"}],
    "Mother-in-law (acc4)": [{"sym": "SOUTHWEST.NS", "qty": 445, "avg": 147.38, "cur": "INR", "sec": "Energy"}, {"sym": "BRPL.BO", "qty": 650, "avg": 122.50, "cur": "INR", "sec": "Industrials"}, {"sym": "ORIENTCER.NS", "qty": 1750, "avg": 43.99, "cur": "INR", "sec": "Materials"}, {"sym": "AARVI.NS", "qty": 480, "avg": 132.50, "cur": "INR", "sec": "Industrials"}, {"sym": "ARIES.NS", "qty": 150, "avg": 322.14, "cur": "INR", "sec": "Agriculture"}, {"sym": "NAHARPOLY.NS", "qty": 200, "avg": 274.14, "cur": "INR", "sec": "Materials"}, {"sym": "ALUFLUOR.BO", "qty": 115, "avg": 479.78, "cur": "INR", "sec": "Chemicals"}, {"sym": "FLUIDOM.BO", "qty": 60, "avg": 854.79, "cur": "INR", "sec": "Industrials"}, {"sym": "RUBFILA.BO", "qty": 600, "avg": 79.89, "cur": "INR", "sec": "Materials"}, {"sym": "KAMDHENU.NS", "qty": 1825, "avg": 27.67, "cur": "INR", "sec": "Materials"}, {"sym": "SARLAPOLY.NS", "qty": 475, "avg": 104.00, "cur": "INR", "sec": "Textiles"}, {"sym": "AEL.BO", "qty": 270, "avg": 177.52, "cur": "INR", "sec": "Industrials"}, {"sym": "AJANTSOY.BO", "qty": 1500, "avg": 34.25, "cur": "INR", "sec": "Agriculture"}, {"sym": "GROBTEA.NS", "qty": 40, "avg": 1135.42, "cur": "INR", "sec": "FMCG"}],
    "Father (acc6)": [{"sym": "SUNPHARMA.NS", "qty": 7, "avg": 352.20, "cur": "INR", "sec": "Pharma"}, {"sym": "NELCO.NS", "qty": 100, "avg": 134.50, "cur": "INR", "sec": "Technology"}, {"sym": "DLF.NS", "qty": 50, "avg": 137.50, "cur": "INR", "sec": "Real Estate"}, {"sym": "GUJGASLTD.NS", "qty": 2005, "avg": 232.60, "cur": "INR", "sec": "Utilities"}, {"sym": "ELECON.NS", "qty": 100, "avg": 178.48, "cur": "INR", "sec": "Industrials"}, {"sym": "MOLDTECH.NS", "qty": 103, "avg": 247.45, "cur": "INR", "sec": "Industrials"}, {"sym": "ASTRAL.NS", "qty": 33, "avg": 1559, "cur": "INR", "sec": "Materials"}]
}

# --- 2. LOGIC ---
st.title("👨‍👩‍👧‍👦 FamilyFolio Dashboard")

@st.cache_data(ttl=600) # Cache data for 10 minutes
def get_market_data():
    all_syms = list(set([h['sym'] for acc in PORTFOLIO_DATA.values() for h in acc]))
    
    # We fetch '2d' to ensure we have the previous close if today is empty
    data = yf.download(all_syms, period="2d", interval="1d")['Close']
    
    # Logic: Take the latest non-null price for every stock
    # This fills the "Today" gap with "Yesterday's" price for closed markets
    latest_prices = data.ffill().iloc[-1]
    
    fx = yf.download(["USDINR=X", "GBPINR=X", "EURINR=X"], period="1d")['Close'].iloc[-1]
    rates = {"USD": fx["USDINR=X"], "GBP": fx["GBPINR=X"], "EUR": fx["EURINR=X"], "INR": 1.0}
    
    return latest_prices, rates

try:
    prices, rates = get_market_data()
    selection = st.sidebar.selectbox("Select Account", ["Combined"] + list(PORTFOLIO_DATA.keys()))
    
    rows = []
    for acc, holdings in PORTFOLIO_DATA.items():
        if selection == "Combined" or selection == acc:
            for h in holdings:
                ltp = prices[h['sym']]
                inr_rate = rates["GBP"] if h['cur'] == "GBP_PENCE" else rates[h['cur']]
                
                # Correct Pence logic
                cur_ltp = ltp/100 if h['cur'] == "GBP_PENCE" else ltp
                
                val_inr = h['qty'] * cur_ltp * inr_rate
                inv_inr = h['qty'] * h['avg'] * inr_rate
                pnl = val_inr - inv_inr
                
                rows.append({
                    "Account": acc, "Symbol": h['sym'], "Sector": h['sec'],
                    "Value (INR)": val_inr, "P&L": pnl, 
                    "Gain %": (pnl/inv_inr*100) if inv_inr != 0 else 0
                })
    
    df = pd.DataFrame(rows)

    # UI Metrics
    col1, col2 = st.columns(2)
    col1.metric("Total Value", f"₹{df['Value (INR)'].sum():,.0f}")
    col2.metric("Total P&L", f"₹{df['P&L'].sum():,.0f}", f"{df['P&L'].sum()/(df['Value (INR)'].sum()-df['P&L'].sum())*100:.2f}%")

    # Sunburst Chart
    fig = px.sunburst(df, path=['Account', 'Sector', 'Symbol'], values='Value (INR)',
                      color='Gain %', color_continuous_scale='RdYlGn', range_color=[-15, 15])
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df.sort_values("Value (INR)", ascending=False), use_container_width=True)

except Exception as e:
    st.error(f"Syncing markets... {e}")

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime

# Set Page Config
st.set_page_config(page_title="FamilyFolio Pro Dashboard", layout="wide")

# --- 1. DATASET ---
PORTFOLIO_DATA = {
    "Mother (acc1)": [{"sym": "BAJFINANCE.NS", "qty": 480, "avg": 325.88, "cur": "INR", "sec": "Financials"}, {"sym": "GUJGASLTD.NS", "qty": 22, "avg": 446.50, "cur": "INR", "sec": "Energy"}, {"sym": "HDFCBANK.NS", "qty": 80, "avg": 684.94, "cur": "INR", "sec": "Financials"}, {"sym": "ICICIBANK.NS", "qty": 87, "avg": 487.88, "cur": "INR", "sec": "Financials"}, {"sym": "JIOFIN.NS", "qty": 231, "avg": 48.33, "cur": "INR", "sec": "Financials"}, {"sym": "RELIANCE.NS", "qty": 462, "avg": 492.16, "cur": "INR", "sec": "Energy"}, {"sym": "TATAELXSI.NS", "qty": 7, "avg": 5957.76, "cur": "INR", "sec": "IT"}, {"sym": "VENUSPIPES.NS", "qty": 47, "avg": 684.99, "cur": "INR", "sec": "Metals"}],
    "Madhur (acc2)": [
        {"sym": "TSLA", "qty": 10, "avg": 251.30, "cur": "USD", "sec": "EV/Tech"}, 
        {"sym": "BNKS.L", "qty": 716, "avg": 5.475, "cur": "USD", "sec": "ETF"}, 
        {"sym": "CNYA.L", "qty": 1400, "avg": 5.4954, "cur": "USD", "sec": "ETF"}, 
        {"sym": "ISLN.L", "qty": 195, "avg": 74.9366, "cur": "USD", "sec": "ETF"}, 
        {"sym": "NVDA", "qty": 131, "avg": 116.84, "cur": "USD", "sec": "Semis"}, 
        {"sym": "EQQQ.L", "qty": 4.0833, "avg": 349.71, "cur": "GBP_PENCE", "sec": "ETF"}, 
        {"sym": "GLEN.L", "qty": 1000, "avg": 5.222, "cur": "GBP_PENCE", "sec": "Commodities"},
        {"sym": "XRP-GBP", "qty": 3020.187964, "avg": 1.821, "cur": "GBP", "sec": "Crypto"},
        {"sym": "ABSI", "qty": 1000, "avg": 5.5593, "cur": "USD", "sec": "Tech-Bio"} # Added New Moonshot
    ],
    "Sonakshi (acc3)": [{"sym": "AMD", "qty": 15, "avg": 231.70, "cur": "USD", "sec": "Semis"}, {"sym": "CRWV", "qty": 40, "avg": 98.62, "cur": "USD", "sec": "AI/Cloud"}, {"sym": "ISLN.L", "qty": 100, "avg": 54.442, "cur": "USD", "sec": "ETF"}, {"sym": "CIFR", "qty": 300, "avg": 20.05, "cur": "USD", "sec": "Crypto"}, {"sym": "RHM.DE", "qty": 3, "avg": 1736.00, "cur": "EUR", "sec": "Defence"}, {"sym": "MRVL", "qty": 90, "avg": 77.52, "cur": "USD", "sec": "Semis"}, {"sym": "AMZN", "qty": 50, "avg": 185.13, "cur": "USD", "sec": "E-Comm"}, {"sym": "IONQ", "qty": 310, "avg": 40.26, "cur": "USD", "sec": "Quantum"}],
    "Mother-in-law (acc4)": [{"sym": "SOUTHWEST.NS", "qty": 445, "avg": 147.38, "cur": "INR", "sec": "Energy"}, {"sym": "BRPL.BO", "qty": 650, "avg": 122.50, "cur": "INR", "sec": "Industrials"}, {"sym": "ORIENTCER.NS", "qty": 1750, "avg": 43.99, "cur": "INR", "sec": "Materials"}, {"sym": "AARVI.NS", "qty": 480, "avg": 132.50, "cur": "INR", "sec": "Industrials"}, {"sym": "ARIES.NS", "qty": 150, "avg": 322.14, "cur": "INR", "sec": "Agriculture"}, {"sym": "NAHARPOLY.NS", "qty": 200, "avg": 274.14, "cur": "INR", "sec": "Materials"}, {"sym": "ALUFLUOR.BO", "qty": 115, "avg": 479.78, "cur": "INR", "sec": "Chemicals"}, {"sym": "FLUIDOM.BO", "qty": 60, "avg": 854.79, "cur": "INR", "sec": "Industrials"}, {"sym": "RUBFILA.BO", "qty": 600, "avg": 79.89, "cur": "INR", "sec": "Materials"}, {"sym": "KAMDHENU.NS", "qty": 1825, "avg": 27.67, "cur": "INR", "sec": "Materials"}, {"sym": "SARLAPOLY.NS", "qty": 475, "avg": 104.00, "cur": "INR", "sec": "Textiles"}, {"sym": "AEL.BO", "qty": 270, "avg": 177.52, "cur": "INR", "sec": "Industrials"}, {"sym": "AJANTSOY.BO", "qty": 1500, "avg": 34.25, "cur": "INR", "sec": "Agriculture"}, {"sym": "GROBTEA.NS", "qty": 40, "avg": 1135.42, "cur": "INR", "sec": "FMCG"}],
    "Father (acc6)": [{"sym": "SUNPHARMA.NS", "qty": 7, "avg": 352.20, "cur": "INR", "sec": "Pharma"}, {"sym": "NELCO.NS", "qty": 100, "avg": 134.50, "cur": "INR", "sec": "Technology"}, {"sym": "DLF.NS", "qty": 50, "avg": 137.50, "cur": "INR", "sec": "Real Estate"}, {"sym": "GUJGASLTD.NS", "qty": 2005, "avg": 232.60, "cur": "INR", "sec": "Utilities"}, {"sym": "ELECON.NS", "qty": 100, "avg": 178.48, "cur": "INR", "sec": "Industrials"}, {"sym": "MOLDTECH.NS", "qty": 103, "avg": 247.45, "cur": "INR", "sec": "Industrials"}, {"sym": "ASTRAL.NS", "qty": 33, "avg": 1559, "cur": "INR", "sec": "Materials"}]
}

# --- 2. CONTROLS ---
st.sidebar.title("App Settings")
selection = st.sidebar.selectbox("Active View", ["Combined"] + list(PORTFOLIO_DATA.keys()))
timeframe = st.sidebar.selectbox("Performance Range", ["5d", "1mo", "6mo", "1y", "YTD"], index=3)
display_currency = st.sidebar.selectbox("Display Currency", ["INR", "USD", "GBP"], index=0)
cur_symbols = {"INR": "₹", "USD": "$", "GBP": "£"}

@st.cache_data(ttl=3600)
def get_pro_data(tf):
    all_syms = list(set([h['sym'] for acc in PORTFOLIO_DATA.values() for h in acc]))
    fx_tickers = ["USDINR=X", "GBPINR=X", "EURINR=X"]
    full_hist = yf.download(all_syms + fx_tickers, period="5d", interval="1d")['Close']
    stock_hist = full_hist[all_syms].ffill().bfill()
    latest_fx = full_hist[fx_tickers].ffill().iloc[-1]
    rates = {"USD": latest_fx["USDINR=X"], "GBP": latest_fx["GBPINR=X"], "EUR": latest_fx["EURINR=X"], "INR": 1.0}
    
    if tf == "YTD":
        start_date = f"{datetime.now().year}-01-01"
        trend_hist = yf.download(all_syms, start=start_date)['Close']
    else:
        trend_hist = yf.download(all_syms, period=tf)['Close']
        
    return stock_hist, trend_hist.ffill().bfill(), rates

try:
    prices_df, trend_hist, rates = get_pro_data(timeframe)
    latest_prices = prices_df.iloc[-1]
    prev_prices = prices_df.iloc[-2]
    conversion_factor = 1 / rates[display_currency]
    rows, performance_map = [], {}

    for acc_name, holdings in PORTFOLIO_DATA.items():
        acc_daily_val_inr = pd.Series(0, index=trend_hist.index)
        for h in holdings:
            cur_code = h['cur'].replace("_PENCE", "")
            inr_rate = rates[cur_code]
            p_series = trend_hist[h['sym']]
            if h['cur'] == "GBP_PENCE": p_series = p_series / 100
            acc_daily_val_inr += (p_series * h['qty'] * inr_rate)
            
            if selection == "Combined" or selection == acc_name:
                ltp = latest_prices[h['sym']]
                prev = prev_prices[h['sym']]
                ltp_adj = ltp/100 if h['cur'] == "GBP_PENCE" else ltp
                prev_adj = prev/100 if h['cur'] == "GBP_PENCE" else prev
                val_display = (h['qty'] * ltp_adj * inr_rate) * conversion_factor
                inv_display = (h['qty'] * h['avg'] * inr_rate) * conversion_factor
                day_pnl = ((ltp_adj - prev_adj) * h['qty'] * inr_rate) * conversion_factor
                
                rows.append({
                    "Symbol": h['sym'], "Account": acc_name, "Shares": h['qty'], 
                    "Avg Price": round(h['avg'] * inr_rate * conversion_factor, 2),
                    "LTP": round(ltp_adj * inr_rate * conversion_factor, 4),
                    f"Value ({display_currency})": val_display, 
                    "Gain %": ((val_display - inv_display)/inv_display*100) if inv_display != 0 else 0,
                    f"Day P&L ({display_currency})": day_pnl,
                    "Total P&L": val_display - inv_display
                })
        performance_map[acc_name] = (acc_daily_val_inr / acc_daily_val_inr.iloc[0]) * 100

    df = pd.DataFrame(rows)
    sym = cur_symbols[display_currency]

    # --- TOP METRICS ---
    m1, m2, m3 = st.columns(3)
    total_val = df[f'Value ({display_currency})'].sum()
    m1.metric(f"Value ({display_currency})", f"{sym}{total_val:,.0f}")
    total_pnl = df["Total P&L"].sum()
    m2.metric("Unrealized P&L", f"{sym}{total_pnl:,.0f}", f"{(total_pnl/(total_val - total_pnl)*100):.2f}%")
    d_pnl = df[f"Day P&L ({display_currency})"].sum()
    m3.metric("Day's P&L", f"{sym}{d_pnl:,.0f}", f"{(d_pnl/total_val*100):.2f}%")

    st.write("---")
    f1, f2, f3 = st.columns(3)
    f1.metric("USD/INR", f"₹{rates['USD']:.2f}")
    f2.metric("GBP/INR", f"₹{rates['GBP']:.2f}")
    f3.metric("EUR/INR", f"₹{rates['EUR']:.2f}")

    # --- CHARTS & TABLE ---
    st.subheader(f"Growth Index ({timeframe})")
    fig_line = px.line(pd.DataFrame(performance_map), labels={"value": "Index", "index": "Date"})
    st.plotly_chart(fig_line, use_container_width=True)
    
    st.dataframe(df.sort_values(f"Value ({display_currency})", ascending=False), use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Market Syncing... Please refresh in 5 seconds. Error: {e}")

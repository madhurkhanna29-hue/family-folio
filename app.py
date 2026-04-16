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
    "Madhur (acc2)": [{"sym": "TSLA", "qty": 10, "avg": 251.30, "cur": "USD", "sec": "EV/Tech"}, {"sym": "BNKS.L", "qty": 716, "avg": 5.475, "cur": "USD", "sec": "ETF"}, {"sym": "CNYA.L", "qty": 1400, "avg": 5.4954, "cur": "USD", "sec": "ETF"}, {"sym": "ISLN.L", "qty": 195, "avg": 74.9366, "cur": "USD", "sec": "ETF"}, {"sym": "NVDA", "qty": 131, "avg": 116.84, "cur": "USD", "sec": "Semis"}, {"sym": "EQQQ.L", "qty": 4.0833, "avg": 349.71, "cur": "GBP_PENCE", "sec": "ETF"}, {"sym": "GLEN.L", "qty": 1000, "avg": 5.222, "cur": "GBP_PENCE", "sec": "Commodities"}],
    "Sonakshi (acc3)": [{"sym": "AMD", "qty": 15, "avg": 231.70, "cur": "USD", "sec": "Semis"}, {"sym": "CRWV", "qty": 40, "avg": 98.62, "cur": "USD", "sec": "AI/Cloud"}, {"sym": "ISLN.L", "qty": 100, "avg": 54.442, "cur": "USD", "sec": "ETF"}, {"sym": "CIFR", "qty": 300, "avg": 20.05, "cur": "USD", "sec": "Crypto"}, {"sym": "RHM.DE", "qty": 3, "avg": 1736.00, "cur": "EUR", "sec": "Defence"}, {"sym": "MRVL", "qty": 90, "avg": 77.52, "cur": "USD", "sec": "Semis"}, {"sym": "AMZN", "qty": 50, "avg": 185.13, "cur": "USD", "sec": "E-Comm"}, {"sym": "IONQ", "qty": 310, "avg": 40.26, "cur": "USD", "sec": "Quantum"}],
    "Mother-in-law (acc4)": [{"sym": "SOUTHWEST.NS", "qty": 445, "avg": 147.38, "cur": "INR", "sec": "Energy"}, {"sym": "BRPL.BO", "qty": 650, "avg": 122.50, "cur": "INR", "sec": "Industrials"}, {"sym": "ORIENTCER.NS", "qty": 1750, "avg": 43.99, "cur": "INR", "sec": "Materials"}, {"sym": "AARVI.NS", "qty": 480, "avg": 132.50, "cur": "INR", "sec": "Industrials"}, {"sym": "ARIES.NS", "qty": 150, "avg": 322.14, "cur": "INR", "sec": "Agriculture"}, {"sym": "NAHARPOLY.NS", "qty": 200, "avg": 274.14, "cur": "INR", "sec": "Materials"}, {"sym": "ALUFLUOR.BO", "qty": 115, "avg": 479.78, "cur": "INR", "sec": "Chemicals"}, {"sym": "FLUIDOM.BO", "qty": 60, "avg": 854.79, "cur": "INR", "sec": "Industrials"}, {"sym": "RUBFILA.BO", "qty": 600, "avg": 79.89, "cur": "INR", "sec": "Materials"}, {"sym": "KAMDHENU.NS", "qty": 1825, "avg": 27.67, "cur": "INR", "sec": "Materials"}, {"sym": "SARLAPOLY.NS", "qty": 475, "avg": 104.00, "cur": "INR", "sec": "Textiles"}, {"sym": "AEL.BO", "qty": 270, "avg": 177.52, "cur": "INR", "sec": "Industrials"}, {"sym": "AJANTSOY.BO", "qty": 1500, "avg": 34.25, "cur": "INR", "sec": "Agriculture"}, {"sym": "GROBTEA.NS", "qty": 40, "avg": 1135.42, "cur": "INR", "sec": "FMCG"}],
    "Father (acc6)": [{"sym": "SUNPHARMA.NS", "qty": 7, "avg": 352.20, "cur": "INR", "sec": "Pharma"}, {"sym": "NELCO.NS", "qty": 100, "avg": 134.50, "cur": "INR", "sec": "Technology"}, {"sym": "DLF.NS", "qty": 50, "avg": 137.50, "cur": "INR", "sec": "Real Estate"}, {"sym": "GUJGASLTD.NS", "qty": 2005, "avg": 232.60, "cur": "INR", "sec": "Utilities"}, {"sym": "ELECON.NS", "qty": 100, "avg": 178.48, "cur": "INR", "sec": "Industrials"}, {"sym": "MOLDTECH.NS", "qty": 103, "avg": 247.45, "cur": "INR", "sec": "Industrials"}, {"sym": "ASTRAL.NS", "qty": 33, "avg": 1559, "cur": "INR", "sec": "Materials"}]
}

# --- 2. CONTROLS & DATA FETCHING ---
st.sidebar.title("App Settings")
selection = st.sidebar.selectbox("Active View", ["Combined"] + list(PORTFOLIO_DATA.keys()))
timeframe = st.sidebar.selectbox("Performance Range", ["5d", "1mo", "6mo", "1y", "YTD"], index=3)

@st.cache_data(ttl=3600)
def get_pro_data(tf):
    all_syms = list(set([h['sym'] for acc in PORTFOLIO_DATA.values() for h in acc]))
    
    # Timeframe logic
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
    hist, rates = get_pro_data(timeframe)
    latest_prices = hist.iloc[-1]
    
    # 3. CALCULATE ANALYTICS
    rows = []
    performance_map = {}
    
    for acc_name, holdings in PORTFOLIO_DATA.items():
        acc_daily_val = pd.Series(0, index=hist.index)
        
        for h in holdings:
            cur_code = h['cur'].replace("_PENCE", "")
            inr_rate = rates[cur_code]
            
            # Historical Trend
            p_series = hist[h['sym']]
            if h['cur'] == "GBP_PENCE": p_series = p_series / 100
            acc_daily_val += (p_series * h['qty'] * inr_rate)
            
            # Table Data (Only for selected view)
            if selection == "Combined" or selection == acc_name:
                ltp = latest_prices[h['sym']]
                prev_close = hist[h['sym']].iloc[-2]
                
                ltp_adj = ltp/100 if h['cur'] == "GBP_PENCE" else ltp
                prev_adj = prev_close/100 if h['cur'] == "GBP_PENCE" else prev_close
                
                val_inr = h['qty'] * ltp_adj * inr_rate
                inv_inr = h['qty'] * h['avg'] * inr_rate
                total_pnl = val_inr - inv_inr
                day_pnl = (ltp_adj - prev_adj) * h['qty'] * inr_rate
                
                rows.append({
                    "Symbol": h['sym'], "Account": acc_name, "Shares": h['qty'], 
                    "Avg Price": h['avg'], "LTP": round(ltp_adj, 2), "Currency": h['cur'],
                    "Value (INR)": val_inr, "Total P&L (INR)": total_pnl, 
                    "Gain %": (total_pnl/inv_inr*100) if inv_inr != 0 else 0,
                    "Day P&L (INR)": day_pnl
                })
        
        # Normalize for Line Chart
        performance_map[acc_name] = (acc_daily_val / acc_daily_val.iloc[0]) * 100

    df = pd.DataFrame(rows)

    # --- 4. TOP METRIC PANE ---
    m1, m2, m3 = st.columns(3)
    m1.metric("Folio Value", f"₹{df['Value (INR)'].sum():,.0f}")
    
    total_pnl_sum = df['Total P&L (INR)'].sum()
    total_inv = df['Value (INR)'].sum() - total_pnl_sum
    m2.metric("Total Unrealized P&L", f"₹{total_pnl_sum:,.0f}", f"{(total_pnl_sum/total_inv*100):.2f}%")
    
    d_pnl = df["Day P&L (INR)"].sum()
    m3.metric("Today's P&L", f"₹{d_pnl:,.0f}", f"{(d_pnl/df['Value (INR)'].sum()*100):.2f}%")
    
    st.write("---")
    f1, f2, f3 = st.columns(3)
    f1.metric("USD/INR", f"₹{rates['USD']:.2f}")
    f2.metric("GBP/INR", f"₹{rates['GBP']:.2f}")
    f3.metric("EUR/INR", f"₹{rates['EUR']:.2f}")
    st.write("---")

    # --- 5. PERFORMANCE TREND (BASE 100) ---
    st.subheader(f"Relative Growth Index ({timeframe})")
    if selection == "Combined":
        fig_line = px.line(pd.DataFrame(performance_map), labels={"value": "Index", "index": "Date"})
    else:
        # Account vs Benchmark
        combined_benchmark = sum(performance_map.values()) / len(performance_map)
        bench_df = pd.DataFrame({selection: performance_map[selection], "Avg Benchmark": combined_benchmark})
        fig_line = px.line(bench_df, labels={"value": "Index", "index": "Date"})
    
    fig_line.update_layout(height=400, legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig_line, use_container_width=True)

    # --- 6. ALLOCATION & TABLE ---
    st.write("---")
    col_left, col_right = st.columns([1, 1.2])
    
    with col_left:
        st.subheader("Asset Allocation")
        fig_sun = px.sunburst(df, path=['Account', 'Symbol'], values='Value (INR)',
                              color='Gain %', color_continuous_scale='RdYlGn', range_color=[-15, 15])
        st.plotly_chart(fig_sun, use_container_width=True)

    with col_right:
        st.subheader("Holdings Detail")
        st.dataframe(df.sort_values("Value (INR)", ascending=False), use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Syncing market data... {e}")

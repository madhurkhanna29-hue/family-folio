import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Set Page Config
st.set_page_config(page_title="FamilyFolio Pro", layout="wide")

# --- 1. DATASET ---
PORTFOLIO_DATA = {
    "Mother (acc1)": [{"sym": "BAJFINANCE.NS", "qty": 480, "avg": 325.88, "cur": "INR", "sec": "Financials"}, {"sym": "GUJGASLTD.NS", "qty": 22, "avg": 446.50, "cur": "INR", "sec": "Energy"}, {"sym": "HDFCBANK.NS", "qty": 80, "avg": 684.94, "cur": "INR", "sec": "Financials"}, {"sym": "ICICIBANK.NS", "qty": 87, "avg": 487.88, "cur": "INR", "sec": "Financials"}, {"sym": "JIOFIN.NS", "qty": 231, "avg": 48.33, "cur": "INR", "sec": "Financials"}, {"sym": "RELIANCE.NS", "qty": 462, "avg": 492.16, "cur": "INR", "sec": "Energy"}, {"sym": "TATAELXSI.NS", "qty": 7, "avg": 5957.76, "cur": "INR", "sec": "IT"}, {"sym": "VENUSPIPES.NS", "qty": 47, "avg": 684.99, "cur": "INR", "sec": "Metals"}],
    "Madhur (acc2)": [{"sym": "TSLA", "qty": 10, "avg": 251.30, "cur": "USD", "sec": "EV/Tech"}, {"sym": "BNKS.L", "qty": 716, "avg": 5.475, "cur": "USD", "sec": "ETF"}, {"sym": "CNYA.L", "qty": 1400, "avg": 5.4954, "cur": "USD", "sec": "ETF"}, {"sym": "ISLN.L", "qty": 195, "avg": 74.9366, "cur": "USD", "sec": "ETF"}, {"sym": "NVDA", "qty": 131, "avg": 116.84, "cur": "USD", "sec": "Semis"}, {"sym": "EQQQ.L", "qty": 4.0833, "avg": 349.71, "cur": "GBP_PENCE", "sec": "ETF"}, {"sym": "GLEN.L", "qty": 1000, "avg": 5.222, "cur": "GBP_PENCE", "sec": "Commodities"}],
    "Sonakshi (acc3)": [{"sym": "AMD", "qty": 15, "avg": 231.70, "cur": "USD", "sec": "Semis"}, {"sym": "CRWV", "qty": 40, "avg": 98.62, "cur": "USD", "sec": "AI/Cloud"}, {"sym": "ISLN.L", "qty": 100, "avg": 54.442, "cur": "USD", "sec": "ETF"}, {"sym": "CIFR", "qty": 300, "avg": 20.05, "cur": "USD", "sec": "Crypto"}, {"sym": "RHM.DE", "qty": 3, "avg": 1736.00, "cur": "EUR", "sec": "Defence"}, {"sym": "MRVL", "qty": 90, "avg": 77.52, "cur": "USD", "sec": "Semis"}, {"sym": "AMZN", "qty": 50, "avg": 185.13, "cur": "USD", "sec": "E-Comm"}, {"sym": "IONQ", "qty": 310, "avg": 40.26, "cur": "USD", "sec": "Quantum"}],
    "Mother-in-law (acc4)": [{"sym": "SOUTHWEST.NS", "qty": 445, "avg": 147.38, "cur": "INR", "sec": "Energy"}, {"sym": "BRPL.BO", "qty": 650, "avg": 122.50, "cur": "INR", "sec": "Industrials"}, {"sym": "ORIENTCER.NS", "qty": 1750, "avg": 43.99, "cur": "INR", "sec": "Materials"}, {"sym": "AARVI.NS", "qty": 480, "avg": 132.50, "cur": "INR", "sec": "Industrials"}, {"sym": "ARIES.NS", "qty": 150, "avg": 322.14, "cur": "INR", "sec": "Agriculture"}, {"sym": "NAHARPOLY.NS", "qty": 200, "avg": 274.14, "cur": "INR", "sec": "Materials"}, {"sym": "ALUFLUOR.BO", "qty": 115, "avg": 479.78, "cur": "INR", "sec": "Chemicals"}, {"sym": "FLUIDOM.BO", "qty": 60, "avg": 854.79, "cur": "INR", "sec": "Industrials"}, {"sym": "RUBFILA.BO", "qty": 600, "avg": 79.89, "cur": "INR", "sec": "Materials"}, {"sym": "KAMDHENU.NS", "qty": 1825, "avg": 27.67, "cur": "INR", "sec": "Materials"}, {"sym": "SARLAPOLY.NS", "qty": 475, "avg": 104.00, "cur": "INR", "sec": "Textiles"}, {"sym": "AEL.BO", "qty": 270, "avg": 177.52, "cur": "INR", "sec": "Industrials"}, {"sym": "AJANTSOY.BO", "qty": 1500, "avg": 34.25, "cur": "INR", "sec": "Agriculture"}, {"sym": "GROBTEA.NS", "qty": 40, "avg": 1135.42, "cur": "INR", "sec": "FMCG"}],
    "Father (acc6)": [{"sym": "SUNPHARMA.NS", "qty": 7, "avg": 352.20, "cur": "INR", "sec": "Pharma"}, {"sym": "NELCO.NS", "qty": 100, "avg": 134.50, "cur": "INR", "sec": "Technology"}, {"sym": "DLF.NS", "qty": 50, "avg": 137.50, "cur": "INR", "sec": "Real Estate"}, {"sym": "GUJGASLTD.NS", "qty": 2005, "avg": 232.60, "cur": "INR", "sec": "Utilities"}, {"sym": "ELECON.NS", "qty": 100, "avg": 178.48, "cur": "INR", "sec": "Industrials"}, {"sym": "MOLDTECH.NS", "qty": 103, "avg": 247.45, "cur": "INR", "sec": "Industrials"}, {"sym": "ASTRAL.NS", "qty": 33, "avg": 1559, "cur": "INR", "sec": "Materials"}]
}

@st.cache_data(ttl=600)
def get_dashboard_data():
    all_syms = list(set([h['sym'] for acc in PORTFOLIO_DATA.values() for h in acc]))
    # Fetch 5 days of data to safely get current vs previous close
    data = yf.download(all_syms, period="5d", interval="1d")['Close']
    data = data.ffill()
    
    fx = yf.download(["USDINR=X", "GBPINR=X", "EURINR=X"], period="1d")['Close'].iloc[-1]
    rates = {"USD": fx["USDINR=X"], "GBP": fx["GBPINR=X"], "EUR": fx["EURINR=X"], "INR": 1.0}
    return data, rates

try:
    st.title("👨‍👩‍👧‍👦 FamilyFolio Live")
    hist_prices, rates = get_dashboard_data()
    
    selection = st.sidebar.selectbox("Account", ["Combined"] + list(PORTFOLIO_DATA.keys()))
    
    rows = []
    for acc_name, holdings in PORTFOLIO_DATA.items():
        if selection == "Combined" or selection == acc_name:
            for h in holdings:
                # Get current and previous close
                stock_series = hist_prices[h['sym']].dropna()
                ltp = stock_series.iloc[-1]
                prev_close = stock_series.iloc[-2]
                
                # High/Low for the table (last 5 days only in this view for speed)
                high_val = stock_series.max()
                low_val = stock_series.min()

                if h['cur'] == "GBP_PENCE":
                    ltp, prev_close, high_val, low_val = ltp/100, prev_close/100, high_val/100, low_val/100
                
                inr_rate = rates["GBP"] if h['cur'] == "GBP_PENCE" else rates[h['cur']]
                
                val_inr = h['qty'] * ltp * inr_rate
                inv_inr = h['qty'] * h['avg'] * inr_rate
                
                # Total P&L
                total_pnl = val_inr - inv_inr
                # Day's P&L (Current Value - Value at Yesterday's Close)
                day_pnl = (ltp - prev_close) * h['qty'] * inr_rate
                
                rows.append({
                    "Symbol": h['sym'],
                    "Shares": h['qty'],
                    "Avg Price": h['avg'],
                    "LTP": ltp,
                    "Day Change %": ((ltp - prev_close) / prev_close) * 100,
                    "Value (INR)": val_inr,
                    "Gain %": (total_pnl/inv_inr*100) if inv_inr != 0 else 0,
                    "Total P&L (INR)": total_pnl,
                    "Day's P&L (INR)": day_pnl,
                    "Account": acc_name
                })

    df = pd.DataFrame(rows)

    # --- TOP PANE METRICS ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Value", f"₹{df['Value (INR)'].sum():,.0f}")
    
    # Total P&L
    total_pnl_sum = df['Total P&L (INR)'].sum()
    total_inv_sum = df['Value (INR)'].sum() - total_pnl_sum
    m2.metric("Total P&L", f"₹{total_pnl_sum:,.0f}", f"{(total_pnl_sum/total_inv_sum*100):.2f}%")
    
    # Day's P&L
    day_pnl_sum = df["Day's P&L (INR)"].sum()
    m3.metric("Day's P&L", f"₹{day_pnl_sum:,.0f}", f"{(day_pnl_sum/(df['Value (INR)'].sum() - day_pnl_sum)*100):.2f}%")
    
    m4.metric("FX: USD/INR", f"{rates['USD']:.2f}")

    # Visuals
    st.divider()
    fig = px.sunburst(df, path=['Account', 'Symbol'], values='Value (INR)',
                      color='Gain %', color_continuous_scale='RdYlGn', range_color=[-15, 15])
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Holdings Detail")
    st.dataframe(df.sort_values("Value (INR)", ascending=False), use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Market sync in progress... {e}")

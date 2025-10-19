import streamlit as st
from coin import coin
import pandas as pd

st.set_page_config(page_title="DEX Token Tracker", page_icon="🧟‍♀️", layout="wide")

st.title("🧟‍♀️ DEX Token Tracker")
st.caption("Track token liquidity, volume, and price across DEXs")

token = st.text_input("Enter Token Address")

# Initialize session state
if "info" not in st.session_state:
    st.session_state.info = None
if "pools" not in st.session_state:
    st.session_state.pools = None

# --- FETCH DATA BUTTON ---
if st.button("Fetch Data"):
    c = coin()
    info = c.info(token)

    if info == {"Unreconized token"}:
        st.error("❌ Error: Unrecognized token. Please try again.")
    elif info == {"Server error"}:
    	st.error("❌ Error: Server error cannot connect. Please try again.")
    else:
        st.session_state.info = info
        st.session_state.c = c
        st.session_state.pools = None  # Reset pool details when fetching new token

# --- SHOW TOKEN INFO ---
if st.session_state.info:
    info = st.session_state.info
    c = st.session_state.c

    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(info["img"], width=150)
    with col2:
        st.subheader(f"{info['name']} ({info['symbol']})")
        st.write(f"💰 **Price:** {info['price']}")
        st.write(f"🎱 **Pools:** {len(c.all_pools(token))}")
        st.markdown(f"[🔗 View on DexScreener]({info['url']})")
        if "website" in info and info["website"]:
            st.markdown(f"[🌐 Website]({info['website']})")

    # --- SHOW POOLS BUTTON ---
    if st.button("Show Pool Details"):
        st.session_state.pools = c.detail(token)

# --- DISPLAY POOL DETAILS ---
# --- DISPLAY POOL DETAILS ---
if st.session_state.pools:
    st.markdown("### 💧 Liquidity Pools")

    for i, pool in enumerate(st.session_state.pools, 1):
        pool_html = f"""
        <div style="
            background-color: #111;
            border: 1px solid #333;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            color: white;
            font-family: 'Segoe UI', sans-serif;
        ">
            <h3 style="margin-bottom: 10px;">Pool {i} — {pool.get('Dex', 'Unknown').upper()}</h3>
            <p><b>🪙 Name:</b> {pool.get('name', 'N/A')}</p>
            <p><b>💰 Liquidity (USD):</b> ${pool.get('Liquidity (USD)', 'N/A'):,}</p>
            <p><b>📈 Market Cap:</b> {pool.get('Market Cap (USD)', 'N/A')}</p>
            <p><b>🔁 24h Volume:</b> {pool.get('24h Volume (USD)', 'N/A')}</p>
            <p><b>🟢 24h Price Change:</b> {pool.get('24 price change', 'N/A')}%</p>
            <p><b>📊 24h Buy/Sell:</b> {pool.get('24h buy/sell', 'N/A')}</p>
            <a href="{pool.get('url', '#')}" target="_blank" style="
                display:inline-block;
                margin-top:10px;
                padding:8px 14px;
                border-radius:8px;
                background-color:#007bff;
                color:white;
                text-decoration:none;
                font-weight:bold;
            ">View on DexScreener</a>
        </div>
        """
        st.markdown(pool_html, unsafe_allow_html=True)


st.caption("This is made by sigma TZL")

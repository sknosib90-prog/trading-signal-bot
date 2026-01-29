import streamlit as st
import google.generativeai as genai
from PIL import Image

# API কনফিগারেশন
API_KEY = "AIzaSyDTUBP0y998XnIOCN9b-Q25AIJkyS6MZ3E"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# পেজ সেটআপ
st.set_page_config(page_title="NOSIB TRADER - HYBRID AI", layout="wide")

# প্রফেশনাল ডার্ক থিম ডিজাইন
st.markdown("""
    <style>
    .main { background-color: #060d17; color: white; }
    .stButton>button { width: 100%; border-radius: 10px; background: linear-gradient(90deg, #00c6ff, #0072ff); color: white; border: none; height: 55px; font-weight: bold; font-size: 18px; }
    .nosib-header { background: #111b27; padding: 25px; border-radius: 15px; border-bottom: 4px solid #0072ff; text-align: center; margin-bottom: 20px; }
    .signal-box { background: #162431; padding: 25px; border-radius: 15px; border: 1px solid #2e3b4e; box-shadow: 0px 10px 30px rgba(0,0,0,0.5); }
    </style>
    """, unsafe_allow_html=True)

# লগইন সুরক্ষা
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="nosib-header"><h1 style="color:#00c6ff;">NOSIB TRADER VIP LOGIN</h1></div>', unsafe_allow_html=True)
    cols = st.columns([1,2,1])
    with cols[1]:
        pwd = st.text_input("Enter VIP Access Key:", type="password")
        if st.button("UNLOCK BOT"):
            if pwd == "NR77":
                st.session_state.auth = True
                st.rerun()
    st.stop()

# মেইন ইন্টারফেস
st.markdown('<div class="nosib-header"><h1 style="color:#00c6ff;">NOSIB TRADER HYBRID AI TERMINAL</h1><p>Status: ✅ PREMIUM ACCESS ACTIVE</p></div>', unsafe_allow_html=True)

# আপনার দেওয়া মার্কেটের তালিকা ক্যাটাগরি অনুযায়ী
currencies = ["USD/IDR (OTC)", "USD/PHP (OTC)", "NZD/USD (OTC)", "USD/PKR (OTC)", "USD/COP (OTC)", "USD/MXN (OTC)", "GBP/NZD (OTC)", "NZD/CHF (OTC)", "EUR/SGD (OTC)", "GBP/JPY", "USD/BRL (OTC)", "EUR/NZD (OTC)", "CAD/JPY", "USD/BDT (OTC)", "USD/INR (OTC)", "CAD/CHF (OTC)", "GBP/USD", "NZD/JPY (OTC)", "USD/ARS (OTC)", "USD/EGP (OTC)", "USD/NGN (OTC)", "USD/TRY (OTC)", "GBP/CAD", "AUD/JPY", "AUD/USD", "EUR/CAD", "CHF/JPY", "USD/ZAR (OTC)", "AUD/NZD (OTC)", "EUR/JPY", "EUR/CHF", "USD/CAD", "USD/CHF"]
cryptos = ["Arbitrum (OTC)", "Dash (OTC)", "Cardano (OTC)", "Chainlink (OTC)", "Cosmos (OTC)", "Zcash (OTC)", "Floki (OTC)", "Avalanche (OTC)", "Axie Infinity (OTC)", "Bitcoin (OTC)", "Ethereum (OTC)"]
commodities = ["UKBrent (OTC)", "Silver (OTC)", "USCrude (OTC)", "Gold (OTC)"]
stocks = ["Intel (OTC)", "Pfizer Inc (OTC)", "Johnson & Johnson (OTC)", "Microsoft (OTC)", "American Express (OTC)", "Boeing Company (OTC)", "FACEBOOK INC (OTC)", "McDonald's (OTC)", "Nikkei 225", "NASDAQ 100", "Dow Jones"]

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("⚙️ মার্কেট সিলেকশন")
    category = st.radio("ক্যাটাগরি বেছে নিন:", ["Currencies", "Crypto", "Commodities", "Stocks/Indices"])
    
    if category == "Currencies": market_list = currencies
    elif category == "Crypto": market_list = cryptos
    elif category == "Commodities": market_list = commodities
    else: market_list = stocks
    
    selected_asset = st.selectbox("ট্রেডিং পেয়ার বেছে নিন:", market_list)
    
    st.markdown("---")
    uploaded_file = st.file_uploader("চার্ট স্ক্রিনশট আপলোড করুন", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption=f"Analyzing {selected_asset}", use_container_width=True)

with col2:
    st.subheader("⚡ AI সিগন্যাল ডিরেকশন")
    if uploaded_file:
        if st.button("GET DEEP ANALYSIS SIGNAL"):
            with st.spinner(f"NOSIB AI {selected_asset} এনালাইসিস করছে..."):
                try:
                    # এআইকে ডিরেকশন দেওয়ার জন্য প্রম্পট
                    prompt = f"""You are a master trader for NOSIB TRADER. Analyze this {selected_asset} chart carefully. 
                    Based on indicators, price action, and candles, provide:
                    1. DIRECTION: (UP/DOWN) in large bold text.
                    2. ACCURACY: (e.g., 95%)
                    3. REASON: Logic behind the signal in Bengali.
                    4. DURATION: 1-minute."""
                    
                    response = model.generate_content([prompt, img])
                    
                    st.markdown('<div class="signal-box">', unsafe_allow_html=True)
                    st.markdown(f"### 🎯 SIGNAL FOR {selected_asset}")
                    st.write(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.info("আপনার চার্ট স্ক্রিনশট আপলোড করলে এখানে প্রফেশনাল এনালাইসিস আসবে।")

st.sidebar.markdown(f"### 🛡️ VIP DASHBOARD: NOSIB")
st.sidebar.write(f"🌐 **Asset:** {selected_asset}")
st.sidebar.write("🟢 **Status:** Ready to Analyze")



      


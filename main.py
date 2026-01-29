import streamlit as st
import google.generativeai as genai
from PIL import Image

# এপিআই এবং মডেল ফিক্স (গুগল জেমিনি লেটেস্ট আপডেট অনুযায়ী)
API_KEY = "AIzaSyDTUBP0y998XnIOCN9b-Q25AIJkyS6MZ3E"
genai.configure(api_key=API_KEY)

# লেটেস্ট জেমিনি মডেল ভার্সন সেটআপ
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# পেজ কনফিগারেশন
st.set_page_config(page_title="NOSIB TRADER VIP", layout="wide")

# প্রফেশনাল প্রিমিয়াম ডিজাইন
st.markdown("""
    <style>
    .main { background-color: #04080f; color: #e0e0e0; }
    .stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(90deg, #ff0055, #ff00aa); color: white; border: none; height: 60px; font-weight: bold; font-size: 20px; box-shadow: 0px 4px 15px rgba(255, 0, 85, 0.4); }
    .header-box { background: #0c1421; padding: 25px; border-radius: 15px; border-bottom: 5px solid #ff0055; text-align: center; margin-bottom: 25px; }
    .nosib-brand { font-size: 40px; color: #ff0055; font-weight: 800; letter-spacing: 2px; }
    .signal-output { background: #0f172a; padding: 30px; border-radius: 15px; border: 2px solid #ff0055; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

# পাসওয়ার্ড সুরক্ষা
if "nosib_access" not in st.session_state:
    st.session_state.nosib_access = False

if not st.session_state.nosib_access:
    st.markdown('<div class="header-box"><div class="nosib-brand">NOSIB TRADER</div><p>VIP ACCESS ONLY</p></div>', unsafe_allow_html=True)
    cols = st.columns([1,2,1])
    with cols[1]:
        key = st.text_input("Enter Passkey:", type="password")
        if st.button("UNLOCK VIP TERMINAL"):
            if key == "NR77":
                st.session_state.nosib_access = True
                st.rerun()
    st.stop()

# মেইন ড্যাশবোর্ড
st.markdown('<div class="header-box"><div class="nosib-brand">NOSIB TRADER HYBRID AI</div><p style="color:#00ff88;">✅ SYSTEM STATUS: CONNECTED (PRO)</p></div>', unsafe_allow_html=True)

# আপনার সব মার্কেটের তালিকা
currencies = ["USD/IDR (OTC)", "USD/PHP (OTC)", "NZD/USD (OTC)", "USD/PKR (OTC)", "USD/COP (OTC)", "USD/MXN (OTC)", "GBP/NZD (OTC)", "NZD/CHF (OTC)", "EUR/SGD (OTC)", "GBP/JPY", "USD/BRL (OTC)", "EUR/NZD (OTC)", "CAD/JPY", "USD/BDT (OTC)", "USD/INR (OTC)", "CAD/CHF (OTC)", "GBP/USD", "NZD/JPY (OTC)", "USD/ARS (OTC)", "USD/EGP (OTC)", "USD/NGN (OTC)", "USD/TRY (OTC)", "GBP/CAD", "AUD/JPY", "AUD/USD", "EUR/CAD", "CHF/JPY", "USD/ZAR (OTC)", "AUD/NZD (OTC)", "EUR/JPY", "EUR/CHF", "USD/CAD", "USD/CHF"]
cryptos = ["Bitcoin (OTC)", "Ethereum (OTC)", "Cardano (OTC)", "Arbitrum (OTC)", "Dash (OTC)", "Chainlink (OTC)", "Cosmos (OTC)", "Zcash (OTC)", "Floki (OTC)", "Avalanche (OTC)", "Axie Infinity (OTC)"]
commodities = ["Gold (OTC)", "Silver (OTC)", "UKBrent (OTC)", "USCrude (OTC)"]
stocks = ["Intel (OTC)", "Pfizer Inc (OTC)", "Johnson & Johnson (OTC)", "Microsoft (OTC)", "American Express (OTC)", "Boeing Company (OTC)", "FACEBOOK INC (OTC)", "McDonald's (OTC)", "Nikkei 225", "NASDAQ 100", "Dow Jones"]

col1, col2 = st.columns([1, 1.3])

with col1:
    st.subheader("🛠 MARKET SELECTION")
    cat = st.radio("ক্যাটাগরি:", ["Currencies", "Crypto", "Commodities", "Stocks"])
    if cat == "Currencies": m_list = currencies
    elif cat == "Crypto": m_list = cryptos
    elif cat == "Commodities": m_list = commodities
    else: m_list = stocks
    
    selected_asset = st.selectbox("ট্রেডিং পেয়ার বেছে নিন:", m_list)
    st.markdown("---")
    file = st.file_uploader("Upload Market Chart Screenshot", type=["jpg", "png", "jpeg"])
    if file:
        img = Image.open(file)
        st.image(img, caption="Live Data Received", use_container_width=True)

with col2:
    st.subheader("📡 HYBRID AI ANALYSIS")
    if file:
        if st.button("GENERATE UP/DOWN SIGNAL"):
            with st.spinner("NOSIB AI deeply analyzing the market..."):
                try:
                    # উন্নত প্রম্পট যা সরাসরি UP/DOWN ডিরেকশন দিবে
                    prompt = f"""You are an Expert Binary Options Trader for NOSIB TRADER.
                    Analyze this {selected_asset} chart image very carefully.
                    Determine the NEXT 1-MINUTE CANDLE direction based on Price Action, RSI, and Candlestick patterns.
                    Format your output exactly like this:
                    - **DIRECTION:** [UP or DOWN in big bold letters]
                    - **CONFIDENCE:** [e.g. 98%]
                    - **LOGIC:** [Bengali explanation of why this direction]"""
                    
                    response = model.generate_content([prompt, img])
                    
                    st.markdown('<div class="signal-output">', unsafe_allow_html=True)
                    st.markdown(f"### 📊 SIGNAL FOR: {selected_asset}")
                    st.write(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}. Please ensure API key is valid.")
    else:
        st.info("আপনার চার্ট আপলোড করলে এখানে এনালাইসিস আসবে।")

st.sidebar.markdown(f"### 🛡️ VIP LOGGED: NOSIB")
st.sidebar.write("🟢 Server: Active (Global)")
st.sidebar.write("🟢 Model: 1.5-Flash-Latest")




      


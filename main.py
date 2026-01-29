import streamlit as st
import google.generativeai as genai
from PIL import Image

# ১. API ফিক্স এবং মডেল কনফিগারেশন
API_KEY = "AIzaSyDTUBP0y998XnIOCN9b-Q25AIJkyS6MZ3E"
genai.configure(api_key=API_KEY)

# এখানে মডেলের নাম আপডেট করা হয়েছে যাতে এরর না আসে
model = genai.GenerativeModel('gemini-1.5-flash')

# ২. ড্যাশবোর্ড ডিজাইন (NOSIB TRADER VIP Look)
st.set_page_config(page_title="NOSIB TRADER - VIP BOT", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #04080f; color: white; }
    .stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(90deg, #ff0055, #ff00aa); color: white; border: none; height: 60px; font-weight: bold; font-size: 20px; box-shadow: 0px 4px 15px rgba(255, 0, 85, 0.4); }
    .header-box { background: #0c1421; padding: 25px; border-radius: 15px; border-bottom: 5px solid #ff0055; text-align: center; }
    .nosib-brand { font-size: 40px; color: #ff0055; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# ৩. পাসওয়ার্ড সুরক্ষা (NR77)
if "nosib_auth" not in st.session_state:
    st.session_state.nosib_auth = False

if not st.session_state.nosib_auth:
    st.markdown('<div class="header-box"><div class="nosib-brand">NOSIB TRADER VIP</div></div>', unsafe_allow_html=True)
    cols = st.columns([1,2,1])
    with cols[1]:
        pwd = st.text_input("Enter VIP Access Key:", type="password")
        if st.button("UNLOCK BOT"):
            if pwd == "NR77":
                st.session_state.nosib_auth = True
                st.rerun()
    st.stop()

# ৪. মেইন অ্যাপ ড্যাশবোর্ড
st.markdown('<div class="header-box"><div class="nosib-brand">NOSIB TRADER HYBRID AI</div><p style="color:#00ff88;">✅ SYSTEM ONLINE | PREMIUM VERSION</p></div>', unsafe_allow_html=True)

# আপনার দেওয়া সেই বিশাল মার্কেটের তালিকা
currencies = ["USD/IDR (OTC)", "USD/PHP (OTC)", "NZD/USD (OTC)", "USD/PKR (OTC)", "USD/COP (OTC)", "USD/MXN (OTC)", "GBP/NZD (OTC)", "NZD/CHF (OTC)", "EUR/SGD (OTC)", "GBP/JPY", "USD/BRL (OTC)", "EUR/NZD (OTC)", "CAD/JPY", "USD/BDT (OTC)", "USD/INR (OTC)", "CAD/CHF (OTC)", "GBP/USD", "NZD/JPY (OTC)", "USD/ARS (OTC)", "USD/EGP (OTC)", "USD/NGN (OTC)", "USD/TRY (OTC)", "GBP/CAD", "AUD/JPY", "AUD/USD", "EUR/CAD", "CHF/JPY", "USD/ZAR (OTC)", "AUD/NZD (OTC)", "EUR/JPY", "EUR/CHF", "USD/CAD", "USD/CHF"]
cryptos = ["Bitcoin (OTC)", "Ethereum (OTC)", "Cardano (OTC)", "Arbitrum (OTC)", "Dash (OTC)", "Chainlink (OTC)", "Cosmos (OTC)", "Zcash (OTC)", "Floki (OTC)", "Avalanche (OTC)", "Axie Infinity (OTC)"]
commodities = ["Gold (OTC)", "Silver (OTC)", "UKBrent (OTC)", "USCrude (OTC)"]
stocks = ["Intel (OTC)", "Pfizer Inc (OTC)", "Johnson & Johnson (OTC)", "Microsoft (OTC)", "American Express (OTC)", "Boeing Company (OTC)", "FACEBOOK INC (OTC)", "McDonald's (OTC)", "Nikkei 225", "NASDAQ 100", "Dow Jones"]

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("🛠 সেটিংস")
    category = st.radio("ক্যাটাগরি:", ["Currencies", "Crypto", "Commodities", "Stocks"])
    
    if category == "Currencies": market_list = currencies
    elif category == "Crypto": market_list = cryptos
    elif category == "Commodities": market_list = commodities
    else: market_list = stocks
    
    selected_asset = st.selectbox("ট্রেডিং পেয়ার বেছে নিন:", market_list)
    st.markdown("---")
    file = st.file_uploader("Upload Market Chart Screenshot", type=["jpg", "png", "jpeg"])
    if file:
        img = Image.open(file)
        st.image(img, caption="Live Data Received", use_container_width=True)

with col2:
    st.subheader("📡 HYBRID AI ANALYSIS")
    if file:
        if st.button("GENERATE UP/DOWN SIGNAL"):
            with st.spinner("NOSIB AI deeply analyzing market trends..."):
                try:
                    # উন্নত প্রম্পট যা সরাসরি UP/DOWN ডিরেকশন দিবে
                    prompt = f"As a pro trader for NOSIB TRADER, analyze this {selected_asset} chart. Determine the next 1-min direction. Provide: 1. DIRECTION (UP/DOWN) 2. ACCURACY % 3. LOGIC in Bengali."
                    response = model.generate_content([prompt, img])
                    
                    st.success(f"🎯 সিগন্যাল রিপোর্ট ফর {selected_asset}:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}. অনুগ্রহ করে মডেল ভার্সন চেক করুন।")
    else:
        st.info("আপনার চার্ট স্ক্রিনশট আপলোড করলে এখানে এনালাইসিস আসবে।")

st.sidebar.markdown(f"### 🛡️ VIP LOGGED: NOSIB")
st.sidebar.write("🟢 Server: Active")
st.sidebar.write("🟢 Model: 1.5-Flash (Updated)")

        




      


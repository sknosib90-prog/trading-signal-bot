import streamlit as st
import google.generativeai as genai
from PIL import Image
import pytz
from datetime import datetime

# --- এপিআই কনফিগারেশন (Error ফিক্সড) ---
GEMINI_KEY = "AIzaSyDTUBP0y998XnIOCN9b-Q25AIJkyS6MZ3E"

# মডেল সেটআপ (সরাসরি স্টেবল ভার্সন যাতে ৪.০.৪ এরর না আসে)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- প্রিমিয়াম ড্যাশবোর্ড ডিজাইন (Replit স্টাইল) ---
st.set_page_config(page_title="NOSIB TRADER VIP", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stSelectbox label { color: #58a6ff !important; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 8px; background: #238636; color: white; border: none; height: 50px; font-weight: bold; font-size: 18px; }
    .nosib-card { background: #161b22; padding: 25px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 20px; text-align: center; }
    .nosib-title { font-size: 32px; color: #58a6ff; font-weight: bold; }
    .signal-box { background: #1c2128; padding: 20px; border-radius: 10px; border-left: 5px solid #58a6ff; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- মেইন ড্যাশবোর্ড ---
st.markdown('<div class="nosib-card"><div class="nosib-title">AURATEX AI MASTER PRO</div><p style="color:#7d8590;">SYSTEM STATUS: ✅ ONLINE (NO GPT DELAY)</p></div>', unsafe_allow_html=True)

# বাংলাদেশি সময়
bd_tz = pytz.timezone('Asia/Dhaka')
now_bd = datetime.now(bd_tz).strftime('%I:%M:%S %p')

# মার্কেট তালিকা (ক্যাটাগরি অনুযায়ী)
MARKETS = {
    "OTC Markets": ["USD/IDR (OTC)", "USD/BRL (OTC)", "USD/BDT (OTC)", "USD/INR (OTC)", "NZD/USD (OTC)"],
    "Crypto": ["Bitcoin (OTC)", "Ethereum (OTC)", "Cardano (OTC)"],
    "Commodities": ["Gold (OTC)", "Silver (OTC)"]
}

col1, col2 = st.columns([1, 1.3])

with col1:
    st.markdown('<div class="nosib-card">', unsafe_allow_html=True)
    st.write(f"🕒 LOCAL TIME: **{now_bd} BD**")
    cat = st.selectbox("MARKET CATEGORY", list(MARKETS.keys()))
    asset = st.selectbox("SELECT ASSET", MARKETS[cat])
    
    st.markdown("---")
    uploaded_file = st.file_uploader("UPLOAD CHART SCREENSHOT", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="nosib-card">', unsafe_allow_html=True)
    st.subheader("📊 AI SIGNAL ANALYSIS")
    
    if uploaded_file:
        if st.button("🔥 GENERATE SURE SHOT SIGNAL"):
            with st.spinner("NOSIB AI deeply analyzing chart..."):
                try:
                    # জেমিনিকে সরাসরি ইনস্ট্রাকশন (একদম পরিষ্কার রেজাল্ট দিবে)
                    prompt = f"""
                    Analyze this {asset} trading chart image. 
                    1. Tell me the next 1-minute candle direction: UP or DOWN.
                    2. Provide the accuracy percentage (e.g., 95%).
                    3. Explain the logic in Bengali based on RSI, Support, and Candlesticks.
                    Format: 🎯 SIGNAL: [UP/DOWN], 📈 CONFIDENCE: [X%], 💡 LOGIC: [Bengali]
                    """
                    
                    response = model.generate_content([prompt, img])
                    
                    st.markdown('<div class="signal-box">', unsafe_allow_html=True)
                    st.markdown(f"### 🎯 SIGNAL FOR {asset}")
                    st.write(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    # এরর হলে সহজ বাংলায় মেসেজ দিবে
                    st.error("গুগল এপিআই কানেকশনে সমস্যা হচ্ছে। এপিআই কী চেক করুন বা কিছুক্ষণ পর চেষ্টা করুন।")
    else:
        st.info("আপনার চার্ট আপলোড করলে এখানে জেমিনি এআই এনালাইসিস দিবে।")
    st.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown("### 🛡️ VIP: NOSIB TRADER")
st.sidebar.write("🟢 AI Model: Gemini 1.5 Flash (Fixed)")
st.sidebar.write("🟢 Speed: Ultra Fast")


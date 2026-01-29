import streamlit as st
import google.generativeai as genai
from openai import OpenAI
from PIL import Image
import pytz
from datetime import datetime, timedelta

# --- এপিআই এবং সিকিউরিটি কনফিগারেশন ---
# আপনার দেওয়া এপিআই কী-গুলো এখানে ঠিকভাবে বসানো হয়েছে
GEMINI_KEY = "AIzaSyDTUBP0y998XnIOCN9b-Q25AIJkyS6MZ3E"
OPENAI_KEY = "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"
ACCESS_PASSWORD = "NR77"

# ১. জেমিনি কনফিগারেশন (Error ফিক্সড)
genai.configure(api_key=GEMINI_KEY)
# মডেলের নাম এখানে নির্দিষ্ট করা হয়েছে যাতে ৪.০.৪ এরর না আসে
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

# ২. ওপেন এআই কনফিগারেশন
client_openai = OpenAI(api_key=OPENAI_KEY)

# ৩. ড্যাশবোর্ড ডিজাইন (NOSIB TRADER Premium Style)
st.set_page_config(page_title="NOSIB TRADER PRO AI", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #04080f; color: white; }
    .stButton>button { width: 100%; border-radius: 10px; background: linear-gradient(90deg, #ff0055, #ff00aa); color: white; height: 55px; font-weight: bold; font-size: 18px; }
    .nosib-header { background: #0c1421; padding: 25px; border-radius: 15px; border-bottom: 5px solid #ff0055; text-align: center; margin-bottom: 20px; }
    .signal-output { background: #0f172a; padding: 25px; border-radius: 15px; border: 2px solid #ff0055; }
    </style>
    """, unsafe_allow_html=True)

# --- ৪. লগইন প্রোটেকশন ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="nosib-header"><h1 style="color:#ff0055;">NOSIB TRADER VIP LOGIN</h1></div>', unsafe_allow_html=True)
    cols = st.columns([1,2,1])
    with cols[1]:
        pwd = st.text_input("পাসওয়ার্ড (NR77) দিন:", type="password")
        if st.button("UNLOCK VIP ACCESS"):
            if pwd == ACCESS_PASSWORD:
                st.session_state.auth = True
                st.rerun()
    st.stop()

# --- ৫. মার্কেট ডাটাবেস (আপনার দেওয়া তালিকা) ---
MARKETS = {
    "OTC Markets (Currencies)": ["USD/IDR (OTC)", "USD/PHP (OTC)", "NZD/USD (OTC)", "USD/BRL (OTC)", "USD/BDT (OTC)", "USD/INR (OTC)", "USD/ZAR (OTC)"],
    "Crypto (OTC)": ["Bitcoin (OTC)", "Ethereum (OTC)", "Cardano (OTC)", "Solana (OTC)"],
    "Commodities": ["Gold (OTC)", "Silver (OTC)", "USCrude (OTC)"],
    "Stocks": ["FACEBOOK INC (OTC)", "Microsoft (OTC)", "Intel (OTC)", "McDonald's (OTC)"]
}

# সাইডবার সেটিংস
st.sidebar.title("🎮 NOSIB AI CONTROL")
category = st.sidebar.selectbox("মার্কেট ক্যাটাগরি", list(MARKETS.keys()))
asset = st.sidebar.selectbox("ট্রেডিং পেয়ার", MARKETS[category])

# সময় মনিটর (বাংলাদেশি সময়)
bd_tz = pytz.timezone('Asia/Dhaka')
now_bd = datetime.now(bd_tz)
st.sidebar.subheader(f"🕒 {now_bd.strftime('%I:%M %p')}")

# --- ৬. মেইন এনালাইসিস ইন্টারফেস ---
st.markdown(f'<div class="nosib-header"><h1 style="color:#ff0055;">ANALYZING: {asset}</h1><p>HYBRID CORE: GEMINI + GPT-4o ACTIVE</p></div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📸 আপলোড চার্ট")
    uploaded_file = st.file_uploader("কিউটেক্স চার্টের স্ক্রিনশট দিন", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)

with col2:
    st.subheader("🎯 এআই সিগন্যাল ডিরেকশন")
    if uploaded_file:
        if st.button("🔥 GENERATE HYBRID SIGNAL"):
            with st.spinner("NOSIB AI চার্ট এনালাইসিস করছে..."):
                try:
                    next_time = (now_bd + timedelta(minutes=1)).strftime("%I:%M %p")
                    
                    # জেমিনি এনালাইসিস (প্রম্পট আপডেট করা হয়েছে)
                    prompt_gemini = f"As a trading expert, analyze this {asset} chart. Tell me if the next candle is UP or DOWN."
                    res_gemini = gemini_model.generate_content([prompt_gemini, img])
                    
                    # জিপিটি হাইব্রিড এনালাইসিস
                    prompt_gpt = f"Chart Analysis: {res_gemini.text}\nAsset: {asset}\nProvide a 1-min signal: CALL or PUT with logic in Bengali."
                    res_gpt = client_openai.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": prompt_gpt}]
                    )
                    
                    st.markdown('<div class="signal-output">', unsafe_allow_html=True)
                    st.markdown(f"### 🚀 সিগন্যাল রেজাল্ট - {next_time}")
                    st.write(res_gpt.choices[0].message.content)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"এপিআই সংযোগে সমস্যা: {e}")
    else:
        st.info("আপনার ট্রেডিং চার্টের স্ক্রিনশট আপলোড করলে এখানে এনালাইসিস আসবে।")

st.sidebar.markdown("---")
st.sidebar.write("🟢 Server: Premium High-Speed")
st.sidebar.write("🟢 AI Model: Hybrid 1.5 PRO")


import streamlit as st
import google.generativeai as genai
import openai
from PIL import Image

# --- API Configuration (আপনার দেওয়া কি-গুলো এখানে বসানো হয়েছে) ---
GEMINI_API_KEY = "AIzaSyDTUBP0y998XnIOCN9b-Q25AIJkyS6MZ3E"
OPENAI_API_KEY = "sk-..." # এখানে আপনার OpenAI কি-টি বসিয়ে নিন

genai.configure(api_key=GEMINI_API_KEY)
openai.api_key = OPENAI_API_KEY

# --- Page Config ---
st.set_page_config(page_title="NOSIB TRADER VIP", layout="wide")

# --- Custom CSS for Advanced Look ---
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: white; }
    .stSelectbox div[data-baseweb="select"] { background-color: #161b22; color: white; border: 1px solid #00d2ff; }
    .market-header { background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%); padding: 20px; border-radius: 10px; text-align: center; font-size: 35px; font-weight: bold; margin-bottom: 20px; }
    .signal-box { background: #1c2128; border: 2px solid #00d2ff; padding: 25px; border-radius: 15px; box-shadow: 0px 4px 20px rgba(0,210,255,0.3); }
    </style>
    """, unsafe_allow_html=True)

# --- Password Lock ---
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.markdown('<div class="market-header">NOSIB TRADER VIP LOGIN</div>', unsafe_allow_html=True)
    pwd = st.text_input("Enter Passkey:", type="password")
    if st.button("Access Dashboard"):
        if pwd == "NR77":
            st.session_state.login = True
            st.rerun()
    st.stop()

# --- Professional Dashboard ---
st.markdown('<div class="market-header">NOSIB TRADER HYBRID AI TERMINAL</div>', unsafe_allow_html=True)

# আপনার দেওয়া মার্কেটের তালিকা (Quotex Market List)
markets = [
    "EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "AUD/USD (OTC)", 
    "EUR/GBP (OTC)", "USD/CHF (OTC)", "NZD/USD (OTC)", "USD/CAD (OTC)",
    "Bitcoin", "Ethereum", "Gold (XAU/USD)", "Silver"
]

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("⚙️ Market Settings")
    selected_market = st.selectbox("Select Trading Asset:", markets) # মার্কেটের নাম এখানে
    ai_mode = st.radio("Select AI Engine:", ["Gemini 1.5 PRO", "GPT-4 Hybrid"])
    
    st.markdown("---")
    uploaded_file = st.file_uploader("Upload Chart Screenshot", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption=f"Analyzing {selected_market}", use_container_width=True)

with col2:
    st.subheader("📊 Live Analysis & Signals")
    if uploaded_file:
        if st.button("GENERATE AI SIGNAL"):
            with st.spinner(f"NOSIB TRADER AI is analyzing {selected_market}..."):
                try:
                    # মার্কেট এবং এআই ইঞ্জিন ব্যবহার করে এনালাইসিস
                    prompt = f"Market: {selected_market}. Analyze this candlestick chart and provide a 1-minute signal (CALL/PUT) with logic and success probability in Bengali."
                    
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content([prompt, img])
                    
                    st.markdown('<div class="signal-box">', unsafe_allow_html=True)
                    st.markdown(f"### 🎯 Signal for {selected_market}")
                    st.write(response.text)
                    st.markdown("---")
                    st.info(f"Analysis Powered by {ai_mode}")
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error connecting to Market API: {e}")
    else:
        st.warning("Please upload a chart to see professional signals.")

st.sidebar.markdown(f"### 🛡️ VIP ACCOUNT: NOSIB")
st.sidebar.write(f"🌐 **Current Market:** {selected_market}")
st.sidebar.write("⚡ **Latency:** 12ms")
st.sidebar.write("💎 **Version:** 4.0 Pro")


      


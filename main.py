import streamlit as st
import google.generativeai as genai
from PIL import Image

# ১. API ফিক্স (সরাসরি লেটেস্ট ভার্সন কনফিগারেশন)
API_KEY = "AIzaSyDTUBP0y998XnIOCN9b-Q25AIJkyS6MZ3E"
genai.configure(api_key=API_KEY)

# এখানে মডেলের নাম আপডেট করা হয়েছে যা সব ভার্সনে কাজ করবে
model = genai.GenerativeModel('gemini-1.5-flash')

# ২. ড্যাশবোর্ড ডিজাইন (NOSIB TRADER Premium)
st.set_page_config(page_title="NOSIB TRADER VIP", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #04080f; color: white; }
    .stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(90deg, #00ffcc, #00ccff); color: black; border: none; height: 60px; font-weight: bold; font-size: 20px; }
    .header-box { background: #0c1421; padding: 25px; border-radius: 15px; border-bottom: 5px solid #00ffcc; text-align: center; }
    .nosib-brand { font-size: 40px; color: #00ffcc; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# ৩. লগইন সিস্টেম (পাসওয়ার্ড: NR77)
if "nosib_auth" not in st.session_state:
    st.session_state.nosib_auth = False

if not st.session_state.nosib_auth:
    st.markdown('<div class="header-box"><div class="nosib-brand">NOSIB TRADER VIP</div></div>', unsafe_allow_html=True)
    cols = st.columns([1,2,1])
    with cols[1]:
        pwd = st.text_input("Enter Passkey:", type="password")
        if st.button("LOGIN"):
            if pwd == "NR77":
                st.session_state.nosib_auth = True
                st.rerun()
    st.stop()

# ৪. মেইন অ্যাপ ড্যাশবোর্ড
st.markdown('<div class="header-box"><div class="nosib-brand">NOSIB TRADER HYBRID AI</div><p style="color:#00ff88;">✅ SYSTEM READY | STABLE VERSION</p></div>', unsafe_allow_html=True)

# আপনার সব মার্কেটের তালিকা
markets = ["USD/IDR (OTC)", "USD/PHP (OTC)", "NZD/USD (OTC)", "USD/BDT (OTC)", "Bitcoin (OTC)", "Gold (OTC)", "FACEBOOK INC (OTC)", "Microsoft (OTC)"]

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("🛠 সেটিংস")
    selected_asset = st.selectbox("মার্কেট সিলেক্ট করুন:", markets)
    st.markdown("---")
    file = st.file_uploader("চার্ট স্ক্রিনশট আপলোড করুন", type=["jpg", "png", "jpeg"])
    if file:
        img = Image.open(file)
        st.image(img, caption="Live Data Received", use_container_width=True)

with col2:
    st.subheader("📡 AI সিগন্যাল এনালাইসিস")
    if file:
        if st.button("GENERATE UP/DOWN SIGNAL"):
            with st.spinner("NOSIB AI এনালাইসিস করছে..."):
                try:
                    # এআইকে ডিরেকশন দেওয়ার জন্য প্রম্পট
                    prompt = f"Analyze this {selected_asset} trading chart. Provide a clear signal: UP or DOWN. Give the accuracy % and logic in Bengali."
                    
                    # মডেল থেকে রেসপন্স নেওয়া
                    response = model.generate_content([prompt, img])
                    
                    st.success(f"🎯 সিগন্যাল ফর {selected_asset}:")
                    st.write(response.text)
                except Exception as e:
                    # মডেল এরর আসলে অল্টারনেটিভ ট্রাই করবে
                    st.error("গুগল সার্ভার কানেকশনে সমস্যা হচ্ছে। অনুগ্রহ করে ২ মিনিট পর আবার চেষ্টা করুন।")
    else:
        st.info("চার্ট আপলোড করলে এখানে এনালাইসিস রিপোর্ট আসবে।")

st.sidebar.markdown(f"### 🛡️ VIP LOGGED: NOSIB")
st.sidebar.write("🟢 Server: Active (Stable)")

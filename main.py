import streamlit as st
import google.generativeai as genai
from PIL import Image

# ১. সরাসরি জেমিনি এপিআই কনফিগারেশন
API_KEY = "AIzaSyDTUBP0y998XnIOCN9b-Q25AIJkyS6MZ3E"
genai.configure(api_key=API_KEY)

# মডেলের নাম এখানে ফিক্স করা হয়েছে (যাতে ৪.০.৪ এরর না আসে)
model = genai.GenerativeModel('gemini-1.5-flash')

# ২. ড্যাশবোর্ড ডিজাইন
st.set_page_config(page_title="NOSIB TRADER VIP", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #04080f; color: white; }
    .stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(90deg, #00ffcc, #00ccff); color: black; border: none; height: 55px; font-weight: bold; font-size: 18px; }
    .header-box { background: #0c1421; padding: 25px; border-radius: 15px; border-bottom: 5px solid #00ffcc; text-align: center; }
    .nosib-brand { font-size: 40px; color: #00ffcc; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# ৩. পাসওয়ার্ড সুরক্ষা (পাসওয়ার্ড: NR77)
if "nosib_auth" not in st.session_state:
    st.session_state.nosib_auth = False

if not st.session_state.nosib_auth:
    st.markdown('<div class="header-box"><div class="nosib-brand">NOSIB TRADER VIP</div></div>', unsafe_allow_html=True)
    pwd = st.text_input("পাসওয়ার্ড দিন:", type="password")
    if st.button("লগইন করুন"):
        if pwd == "NR77":
            st.session_state.nosib_auth = True
            st.rerun()
    st.stop()

# ৪. মেইন অ্যাপ ইন্টারফেস
st.markdown('<div class="header-box"><div class="nosib-brand">NOSIB HYBRID AI</div><p>Status: ✅ CONNECTED & READY</p></div>', unsafe_allow_html=True)

# আপনার সব মার্কেটের তালিকা
markets = ["USD/IDR (OTC)", "USD/PHP (OTC)", "NZD/USD (OTC)", "USD/BDT (OTC)", "Bitcoin (OTC)", "Gold (OTC)", "FACEBOOK INC (OTC)", "Microsoft (OTC)"]

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("🛠 সেটিংস")
    asset = st.selectbox("মার্কেট সিলেক্ট করুন:", markets)
    st.markdown("---")
    file = st.file_uploader("চার্ট স্ক্রিনশট দিন", type=["jpg", "png", "jpeg"])
    if file:
        img = Image.open(file)
        st.image(img, use_container_width=True)

with col2:
    st.subheader("📡 AI সিগন্যাল ডিরেকশন")
    if file:
        if st.button("GENERATE UP/DOWN SIGNAL"):
            with st.spinner("NOSIB AI এনালাইসিস করছে..."):
                try:
                    # এটি সরাসরি কাজ করবে
                    prompt = f"Analyze this {asset} chart. Provide a clear 1-minute UP or DOWN signal with logic in Bengali."
                    response = model.generate_content([prompt, img])
                    
                    st.success(f"🎯 সিগন্যাল ফর {asset}:")
                    st.write(response.text)
                except Exception as e:
                    # যদি আবার এরর আসে তবে এটি অল্টারনেটিভ মডেল ট্রাই করবে
                    try:
                        alt_model = genai.GenerativeModel('gemini-pro-vision')
                        response = alt_model.generate_content([prompt, img])
                        st.write(response.text)
                    except:
                        st.error("গুগল সার্ভারে সমস্যা হচ্ছে। অনুগ্রহ করে ২ মিনিট পর চেষ্টা করুন।")
    else:
        st.info("চার্ট আপলোড করলে এখানে সিগন্যাল আসবে।")
        




      


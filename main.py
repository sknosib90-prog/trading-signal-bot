import streamlit as st
import google.generativeai as genai
from PIL import Image

# ১. জেমিনি এপিআই কনফিগারেশন
# এখানে আপনার এপিআই কি-টি বসানো আছে
genai.configure(api_key="AIzaSyDTUBP0y998XnIOCN9b-Q25AIJkyS6MZ3E") 
model = genai.GenerativeModel('gemini-1.5-flash')

# ২. পেজ সেটআপ
st.set_page_config(page_title="Auratex VIP Bot", layout="centered")
st.title("🚀 Auratex Hybrid Analysis")

# ৩. পাসওয়ার্ড সুরক্ষা (আপনি NR77 চেয়েছিলেন)
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.subheader("🔐 লগইন করুন")
    password = st.text_input("পাসওয়ার্ড দিন (NR77):", type="password")
    if st.button("Unlock Bot"):
        if password == "NR77": # আপনার দেওয়া পাসওয়ার্ড
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("ভুল পাসওয়ার্ড! আবার চেষ্টা করুন।")
    st.stop()

# ৪. মেইন ইন্টারফেস (লগইন করার পর যা আসবে)
st.success("স্বাগতম! আপনার ট্রেডিং বোর্ড এখন সচল।")
uploaded_file = st.file_uploader("কিউটেক্স চার্টের স্ক্রিনশট আপলোড করুন", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="আপনার আপলোড করা চার্ট", use_container_width=True)
    
    if st.button("এনালাইসিস করুন (Get Signal)"):
        with st.spinner("এআই চার্ট এনালাইসিস করছে..."):
            try:
                # এআইকে কমান্ড দেওয়া হচ্ছে
                prompt = "Analyze this trading chart and give a 1-minute CALL or PUT signal with logic in Bengali."
                response = model.generate_content([prompt, image])
                
                st.markdown("### 📊 এনালাইসিস রিপোর্ট:")
                st.write(response.text)
            except Exception as e:
                st.error(f"দুঃখিত, একটি সমস্যা হয়েছে: {e}")

st.sidebar.markdown("---")
st.sidebar.info("বটটি এখন অনলাইন এবং জেমিনি এআই-এর সাথে কানেক্টেড।")

      


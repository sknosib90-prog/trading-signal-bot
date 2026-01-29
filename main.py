import streamlit as st
import google.generativeai as genai
from PIL import Image

# Gemini API Key এখানে দিন
genai.configure(api_key="AIzaSyA_XXXXXXXXXXXXXXXX") 
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🚀 Auratex Analysis Bot")

# পাসওয়ার্ড সেকশন
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    pwd = st.text_input("পাসওয়ার্ড দিন (NR77):", type="password")
    if st.button("Unlock"):
        if pwd == "NR77":
            st.session_state.login = True
            st.rerun()
    st.stop()

# মেইন বোর্ড
uploaded_file = st.file_uploader("চার্ট স্ক্রিনশট দিন", type=["jpg", "png", "jpeg"])
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Scanning...", width=300)
    if st.button("Get Signal"):
        response = model.generate_content(["Analyze this chart and give CALL/PUT signal.", img])
        st.success("এনালাইসিস রিপোর্ট:")
        st.write(response.text)
      


import streamlit as st
from data_handler import load_excel, generate_data_profile
from mockup_generator import generate_text_mockup, generate_image_mockup
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="AI Business Mockup Chatbot", layout="wide")
st.title("💼 AI Business Mockup Chatbot with Visuals")

st.sidebar.header("⚙️ Settings")
role = st.sidebar.selectbox(
    "Select AI Role",
    ["Business Analyst", "Procurement Specialist", "Finance Planner", "Operations Manager"]
)

uploaded_file = st.sidebar.file_uploader("📂 Upload Excel file", type=["xlsx", "xls"])

if uploaded_file:
    excel_data = load_excel(uploaded_file)
    profile = generate_data_profile(excel_data)
else:
    st.info("No file uploaded — using demo dataset.")
    excel_data = {"Demo": pd.read_excel("demo_data.xlsx")}
    profile = generate_data_profile(excel_data)

user_prompt = st.text_area("💬 What do you want me to draft?", placeholder="e.g., Create a procurement performance dashboard...")

if st.button("🚀 Generate Mockup"):
    with st.spinner("🧠 Analyzing and generating..."):
        text_mockup = generate_text_mockup(user_prompt, profile, role)
        image_mockup = generate_image_mockup(user_prompt)

    st.subheader("📋 Draft Mockup (Text)")
    st.write(text_mockup)

    st.subheader("🖼️ Visual Mockup")
    st.image(image_mockup, caption=f"AI-generated visualization for: {user_prompt}", use_container_width=True)

    # Allow image download
    buf = BytesIO(image_mockup)
    st.download_button("⬇️ Download Image", data=buf, file_name="mockup.png", mime="image/png")

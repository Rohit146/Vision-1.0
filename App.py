import streamlit as st
import pandas as pd
from data_handler import load_excel, generate_data_profile
from mockup_generator import generate_text_mockup, generate_image_mockup
from visualizer import suggest_chart
from report_exporter import export_pdf
from io import BytesIO

st.set_page_config(page_title="AI Business Mockup Chatbot", layout="wide")
st.title("💼 AI Business Mockup Chatbot with Visual Mockups")

st.sidebar.header("⚙️ Settings")
role = st.sidebar.selectbox(
    "Select AI Role",
    ["Business Analyst", "Procurement Specialist", "Finance Planner", "Operations Manager"]
)

uploaded_file = st.sidebar.file_uploader("📂 Upload Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    # ✅ Load Excel
    excel_data = load_excel(uploaded_file)
    profile = generate_data_profile(excel_data)

    # ✅ Display data summary
    with st.expander("🔍 View Data Summary"):
        st.text(profile)

    # ✅ User prompt
    user_prompt = st.text_area(
        "💬 What do you want me to draft?",
        placeholder="e.g., Create a supplier risk dashboard mockup..."
    )

    if st.button("🚀 Generate Mockup"):
        with st.spinner("🧠 Generating AI mockup..."):
            # Generate text + image mockup
            text_mockup = generate_text_mockup(user_prompt, profile, role)
            image_mockup = generate_image_mockup(user_prompt)

        st.subheader("📋 Textual Business Mockup")
        st.write(text_mockup)

        st.subheader("🖼️ Visual Mockup (AI-Generated)")
        st.image(image_mockup, caption=f"Mockup visualization for: {user_prompt}", use_container_width=True)

        # Download image
        buf = BytesIO(image_mockup)
        st.download_button("⬇️ Download Image", data=buf, file_name="mockup_visual.png", mime="image/png")

        # Export text as PDF
        if st.button("📄 Export Mockup as PDF"):
            pdf_file = export_pdf(text_mockup)
            with open(pdf_file, "rb") as f:
                st.download_button("⬇️ Download PDF Report", f, "business_mockup_report.pdf")

    # ✅ Optional chart builder
    with st.expander("📊 Interactive Chart Builder"):
        sheet = st.selectbox("Select Sheet", list(excel_data.keys()))
        suggest_chart(excel_data[sheet])

else:
    st.info("📂 Please upload an Excel file to start generating business mockups.")

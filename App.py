import streamlit as st
from data_handler import load_excel, generate_data_profile
from mockup_generator import generate_text_mockup, generate_image_mockup
from visualizer import suggest_chart
from report_exporter import export_pdf
from io import BytesIO

st.set_page_config(page_title="AI Business Mockup Chatbot", layout="wide")
st.title("💼 AI Business Mockup Chatbot with Aligned Visuals")

st.sidebar.header("⚙️ Settings")
role = st.sidebar.selectbox(
    "Select AI Role",
    ["Business Analyst", "Procurement Specialist", "Finance Planner", "Operations Manager"]
)

uploaded_file = st.sidebar.file_uploader("📂 Upload Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    excel_data = load_excel(uploaded_file)
    profile = generate_data_profile(excel_data)

    with st.expander("🔍 View Data Summary"):
        st.text(profile)

    user_prompt = st.text_area(
        "💬 Describe what you want me to create",
        placeholder="e.g., Create a supplier performance dashboard with KPIs and charts..."
    )

    if st.button("🚀 Generate Mockup"):
        with st.spinner("🧠 Generating textual and visual mockup..."):
            # 1️⃣ Generate structured text mockup
            text_mockup = generate_text_mockup(user_prompt, profile, role)

            # 2️⃣ Generate image mockup based on the text output
            image_mockup = generate_image_mockup(text_mockup, role)

        # Display results
        st.subheader("📋 Textual Business Mockup")
        st.markdown(text_mockup)

        st.subheader("🖼️ Visual Mockup (Based on Textual Layout)")
        st.image(image_mockup, caption="AI-generated visual inspired by the textual mockup", use_container_width=True)

        # Download options
        buf = BytesIO(image_mockup)
        st.download_button("⬇️ Download Image", data=buf, file_name="mockup_visual.png", mime="image/png")

        if st.button("📄 Export Mockup as PDF"):
            pdf_file = export_pdf(text_mockup)
            with open(pdf_file, "rb") as f:
                st.download_button("⬇️ Download PDF Report", f, "business_mockup_report.pdf")

    with st.expander("📊 Interactive Chart Builder"):
        sheet = st.selectbox("Select Sheet", list(excel_data.keys()))
        suggest_chart(excel_data[sheet])

else:
    st.info("📂 Please upload an Excel file to start generating your mockup.")

import plotly.express as px
import streamlit as st

def suggest_chart(df):
    """Interactive visualization generator"""
    st.markdown("### 📈 Generate Your Own Chart")
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    if not numeric_cols:
        st.warning("No numeric columns found for visualization.")
        return

    x_col = st.selectbox("Select X-axis", df.columns)
    y_col = st.selectbox("Select Y-axis", numeric_cols)
    chart_type = st.radio("Select Chart Type", ["Bar", "Line", "Pie"], horizontal=True)

    if chart_type == "Bar":
        fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
    elif chart_type == "Line":
        fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} trend by {x_col}")
    else:
        fig = px.pie(df, names=x_col, values=y_col, title=f"{y_col} distribution by {x_col}")

    st.plotly_chart(fig, use_container_width=True)

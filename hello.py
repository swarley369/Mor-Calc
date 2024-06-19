import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Movie App",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🎬 Movie Explorer App")
st.write("## Explore your favorite movies and visualize data")

movie_name = st.text_input("Enter the name of a movie", "Star Wars")

if st.button("Submit"):
    st.success(f"Your favorite movie is `{movie_name}`")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("### Movie Data")
    st.dataframe(data)
    
    if st.checkbox("Show Data Summary"):
        st.write("### Data Summary")
        st.write(data.describe())

    columns = st.multiselect("Select columns to visualize", data.columns)

    if columns:
        chart_data = pd.DataFrame(np.random.randn(20, len(columns)), columns=columns)
        
        chart_type = st.selectbox("Select chart type", ["Bar Chart", "Line Chart", "Area Chart"])

        if chart_type == "Bar Chart":
            st.bar_chart(chart_data)
        elif chart_type == "Line Chart":
            st.line_chart(chart_data)
        else:
            st.area_chart(chart_data)
else:
    st.info("Please upload a CSV file to get started.")

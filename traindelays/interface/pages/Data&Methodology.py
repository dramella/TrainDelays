import streamlit as st
import os

# Set the page configuration
st.set_page_config(
    page_title="Data & Methodology",
    page_icon="https://t3.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://www.networkrail.co.uk/",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS + HTML for the header
background_style = """
.stApp {
    background-color: white;
    color: black;
}

# Styles for the enclosed box
.box {
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 20px;
    background-color: white;  # Change background color to white
    margin: 20px 0;
}
"""

# Page title and intro
box_style = "border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); padding: 20px; background-color: #F0F2F6;"
st.markdown(f"""
    <div style="{box_style}">
        <h1 style="font-family: 'Noto Sans', sans-serif; color: black; font-size: 36px; text-align: center;">
            Data & Methodology
        </h1>
    </div>
""", unsafe_allow_html=True)

st.header('Introduction')
st.markdown("""The primary objective of this project is to develop a predictive model for estimating the duration of
            delays for London Overground trains following an incident or unexpected occurrence. The dataset utilized for
            this study has been sourced from [Network Rail](https://www.networkrail.co.uk/who-we-are/transparency-and-ethics/transparency/open-data-feeds/),
            which provides daily delay data for passenger train services since 2018. The data includes information on various incidents, their corresponding impacts on train schedules,
            and the duration of resulting delays. Key variables encompass incident type, time of occurrence, location, and
            historical delay patterns.""")




st.header('Data Preprocessing')
st.markdown("""Prior to deploying the dataset for analysis, a data preprocessing phase was conducted. This encompassed
            handling missing data, standardizing formats, and encoding categorical variables. In addition, considering
            the relevance of location information, the raw dataset included location codes, necessitating the extraction
            of latitude and longitude coordinates.""")

st.header("Model Selection")
st.markdown("""Several machine learning models were assessed and a Random Forest Regressor model was selected as the final choice.""")

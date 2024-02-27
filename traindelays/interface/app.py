#################################### Libraries #################################
import streamlit as st
from st_pages import Page, show_pages

import numpy as np
import pandas as pd

#################################### Main Page #################################
# Set the page configuration
st.set_page_config(
    page_title="Train Delays",
    page_icon=":train:",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Create a styled container for the title
st.markdown("""
    <div style="background-color: #f0f0f0; padding: 20px; border-radius: 10px; text-align: center;">
        <h1 style="font-family: 'Noto Sans', sans-serif; color: #333333;">Will your train be delayed or canceled?</h1>
    </div>
""", unsafe_allow_html=True)

# Add some padding for better spacing
st.markdown("<br>", unsafe_allow_html=True)

# Create styled main page intro
st.markdown("""
    <div style="background-color: #f0f0f0; padding: 20px; border-radius: 10px; text-align: center;">
        <p style="font-family: 'Noto Sans', sans-serif; color: #333333; font-size: 18px;">
            Stay ahead of your journey! This dashboard provides real-time insights into
            delays, helping you forecast how much your train will be delayed.
        </p>
    </div>
""", unsafe_allow_html=True)

# Add more spacing
st.markdown("<br>", unsafe_allow_html=True)

# Specify what pages should be shown in the sidebar, and their titles and icons
show_pages(
    [
        Page("app.py", "Home", ":house:"),
        Page("pages/About.py", "About", ":information_source:"),
        Page("pages/Data&Methodology.py", "Data & Methodology", ":bar_chart:")
    ]
)

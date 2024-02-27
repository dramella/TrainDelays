import streamlit as st
from st_pages import Page, show_pages

import numpy as np
import pandas as pd

# Set the page configuration
st.set_page_config(
    page_title="Train Delays",
    page_icon=":train:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create a box with the specified width and padding
box_style = "border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); padding: 20px; background-color: #f5f5f5;"

# Enclose the title and main page intro in a box
st.markdown(f"""
    <div style="{box_style}">
        <h1 style="font-family: 'Noto Sans', sans-serif; color: black; font-size: 36px; text-align: center;">
            How long will your train be delayed?
        </h1>
        <p style="font-family: 'Noto Sans', sans-serif; color: black; font-size: 18px; text-align: center; line-height: 1.5;">
            Stay ahead on your journey! This dashboard provides real-time insights into delays, helping you forecast how much your train might be delayed.
        </p>
    </div>
""", unsafe_allow_html=True)

# Specify what pages should be shown in the sidebar, and their titles and icons
show_pages(
    [
        Page("app.py", "Home", ":house:"),
        Page("pages/About.py", "About us", ":information_source:"),
        Page("pages/Data&Methodology.py", "Data & Methodology", ":bar_chart:")
    ]
)

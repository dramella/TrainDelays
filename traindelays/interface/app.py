"""
This is the module for building a (tentative) web-interface of the Train Delays project.
"""
#################################### Libraries #################################
import streamlit as st
from st_pages import Page, show_pages, add_page_title
import numpy as np
import pandas as pd

#################################### Main Page #################################
# Set the page configuration:
# - page title, shown in the browser tab.
# - page favicon
# - how the page content should be laid out
# - how the sidebar should start out

st.set_page_config(page_title="Train Delays", page_icon=":train:", layout="centered",
                   initial_sidebar_state="expanded")

# create a title variable to contain the text and the CSS.
# CSS is required because streamlit does not allow to customize font family and color, text width, etc.
title_formatted = """<div
                class="stMarkdown" data-testid="stMarkdown" style="width:1000px;">
                <div data-testid="stMarkdownContainer" class="st-emotion-cache-5rimss e1nzilvr5">
                <p style="font-family: &quot;Noto Sans&quot;, sans-serif; color: black; font-size: 42px;">
                Will be your train delayed or canceled?
                </p>
                </div>
                </div>"""
st.markdown(title_formatted,unsafe_allow_html=True)


# create an intro variable to contain the text and the CSS.

main_page_intro = """
<p style="font-family: &quot;Noto Sans&quot;, sans-serif; color: black">
Stay ahead of your journey! This dashboard provides real-time insights into
potential delays and cancellations, helping you plan your travels more efficiently.
</p>
"""
st.markdown(main_page_intro,unsafe_allow_html=True)

# Define a function to hide selected pages --> ToDo: put in utils.py

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("app.py", "Home", ":technologist:"),
        Page("pages/About.py", "About", ":technologist:"),
        Page("pages/Data&Methodology.py", "Data & Methodology")

    ]
)

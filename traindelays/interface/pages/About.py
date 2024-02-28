import streamlit as st
import os

# Set the page configuration
st.set_page_config(
    page_title="About us",
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
            About us
        </h1>
    </div>
""", unsafe_allow_html=True)


css_header = """
@import url('https://fonts.googleapis.com/css?family=Noto+Sans:100,100i,200,200i,300,300i,400,400i,500,500i,600,600i,700,700i,800,800i,900,900i&display=swap');
body {
    font-family:"Noto Sans", sans-serif;
    line-height:1.15;
    font-size:14px;
}

# Rest of the styles...
"""

st.write(f'<style>{background_style}</style>', unsafe_allow_html=True)
st.write(f'<style>{css_header}</style>', unsafe_allow_html=True)

# set CSS style to round all images except the one with the "exclude-me" tag (i.e. LinkedIn icons)
st.markdown("""
<style>
    img:not(#exclude-me) {border-radius: 50%}
</style>
""", unsafe_allow_html=True)

# Lewis info
st.markdown('<div class="box">', unsafe_allow_html=True)
col1, mid, col2 = st.columns([1, 2, 20], gap="medium")
with col1:
    st.image(os.path.abspath('images/ltrudeau.jpeg'), width=105)

with col2:
    st.markdown("**Lewis Trudeau**")
    st.write("""
        <img src="https://github.githubassets.com/favicons/favicon.svg" width="20"> **Github profile**: https://github.com/LewisT1424

        <img id='exclude-me' src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" width="20"> **LinkedIn**: https://www.linkedin.com/in/lewis-trudeau-338a62201/
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Debora info
st.markdown('<div class="box">', unsafe_allow_html=True)
col1, mid, col2 = st.columns([1, 2, 20], gap="medium")
with col1:
    st.image(os.path.abspath('images/dramella.jpeg'), width=105)

with col2:
    st.markdown("**Debora Ramella**")
    st.markdown("""
        <img class="image backArrow" src="https://github.githubassets.com/favicons/favicon.svg" width="20"> **Github profile**: https://github.com/dramella

        <img id='exclude-me' src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" width="20"> **LinkedIn**: https://www.linkedin.com/in/debora-ramella/
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Ben info
st.markdown('<div class="box">', unsafe_allow_html=True)
col1, mid, col2 = st.columns([1, 2, 20], gap="medium")
with col1:
    st.image(os.path.abspath('images/ben.jpeg'), width=105)

with col2:
    st.markdown("**Ben Fairbairn**")
    st.write("""
        <img src="https://github.githubassets.com/favicons/favicon.svg" width="20"> **Github profile**: https://github.com/MathmoBen

        <img id='exclude-me' src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" width="20"> **LinkedIn**: https://www.linkedin.com/in/ben-fairbairn-b73a9030/
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Joel info
st.markdown('<div class="box">', unsafe_allow_html=True)
col1, mid, col2 = st.columns([1, 2, 20], gap="medium")
with col1:
    st.image(os.path.abspath('images/joel.jpeg'), width=105)

with col2:
    st.markdown("**Joel Okwuchukwu**")
    st.write("""
        <img src="https://github.githubassets.com/favicons/favicon.svg" width="20"> **Github profile**: https://github.com/YvngJoey101

        <img id='exclude-me' src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" width="20"> **LinkedIn**: https://www.linkedin.com/in/joel-okwuchukwu-808880229/
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

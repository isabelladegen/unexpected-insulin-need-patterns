import streamlit as st
from streamlit.components.v1 import html

from constants import expected_colour, unexpected_colour, key_findings, explore_patterns, individual_variations, why_this_matters
from explore_patterns import display_explore_patterns
from inividual_variations import display_individual_variations
from key_findings import display_main_findings
from why_this_matters import display_why_this_matters

UNI_BRISTOL_LOGO_WIDE = "images/uni_bristol_logo.png"
UNI_BRISTOL_ICON = "images/uni_bristol_icon.png"
QR_CODE = "images/qr_code.png"

# other content
content_title = "Beyond Expected Patterns in Type 1 Diabetes"

# Get the config values
secondary_bg_color = st.get_option("theme.secondaryBackgroundColor")
text_colour = st.get_option("theme.textColor")

# Inject the CSS variable into the root
css_variables = f"""
<style>
:root {{
    --secondary-bg-color: {secondary_bg_color};
    --text-colour: {text_colour};
    --expected-colour: {expected_colour};
    --unexpected-colour: {unexpected_colour};
}}
</style>
"""


def local_css(file_name):
    st.markdown(css_variables, unsafe_allow_html=True)
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def load_custom_js(file_name):
    with open(file_name, 'r') as file:
        js_content = file.read()
        html(f"<script>{js_content}</script>", height=0)


def main():
    # Set page config
    st.set_page_config(
        page_title="Unexpected insulin needs",
        page_icon=UNI_BRISTOL_ICON,
        layout="wide",
    )

    # Load css and js
    local_css("style/style.css")
    load_custom_js("scripts/style_metrics.js")

    # Sidebar
    st.logo(
        UNI_BRISTOL_LOGO_WIDE,
        size="large",
        link=None,
        icon_image=UNI_BRISTOL_ICON)

    st.sidebar.title(content_title)

    page_1 = key_findings
    page_2 = explore_patterns
    # page_3 = ":clock1: Time of Day Analysis"
    page_4 = individual_variations
    page_5 = why_this_matters
    page = st.sidebar.radio(
        "Select...",
        [page_1, page_2, page_4, page_5]
    )

    # Main body content
    st.title(content_title)
    st.caption("*Isabella Degen | Kate Robson Brown | Henry W. J. Reeve | Zahraa S. Abdallah*")
    with st.container(border=False, key='main-callout'):
        st.markdown("AI as a research tool to improve our understanding of complex biological systems.")

    # Content based on selection
    if page == page_1:
        display_main_findings()

    if page == page_2:
        display_explore_patterns()

    if page == page_4:
        display_individual_variations()

    if page == page_5:
        display_why_this_matters()

    st.divider()

    with st.expander("Details on method"):
        st.markdown("""
        We analysed time series data on insulin on board (IOB), carbohydrates on board (COB) and 
        interstitial glucose (IG) from 29 participants using the OpenAPS AID system. 

        **Pattern frequency** in hours, days 
        (grouped via K-means clustering), weekdays, and months were determined by comparing the 95% CI of the mean 
        differences between temporal units.

        **Associations** between pattern frequency and demographic variables were examined. Significant differences in 
        IOB, COB and IG for various time categories were assessed using Mann-Whitney U tests. 
        Effect sizes and Euclidean distances between variables were calculated. Finally, the forecastability of IOB, COB, 
        and IG for the clustered days was analysed using Granger causality. 
        """)

    st.markdown("[Full paper](https://dx.doi.org/10.2196/44384)")


if __name__ == "__main__":
    main()

import streamlit as st
from streamlit.components.v1 import html

from additional_information import display_additional_information
from constants import expected_colour, unexpected_colour, key_findings, explore_patterns, individual_variations, \
    why_this_matters, additional_information
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

    st.sidebar.image(QR_CODE, use_container_width=True)
    st.sidebar.markdown("Scan QR code to explore on your device")

    display_header()

    page_tabs = st.tabs([
        key_findings,
        explore_patterns,
        individual_variations,
        why_this_matters,
        additional_information
    ])

    # Content based on selection
    with page_tabs[0]:
        display_main_findings()

    with page_tabs[1]:
        display_explore_patterns()

    with page_tabs[2]:
        display_individual_variations()

    with page_tabs[3]:
        display_why_this_matters()

    with page_tabs[4]:
        display_additional_information()


def display_header():
    # Main body content
    st.title(content_title)
    st.caption("*Isabella Degen | Kate Robson Brown | Henry W. J. Reeve | Zahraa S. Abdallah*")
    with st.container(border=False, key='main-callout'):
        st.markdown("""##### AI as a research tool to improve our understanding of complex biological systems.""")


if __name__ == "__main__":
    main()

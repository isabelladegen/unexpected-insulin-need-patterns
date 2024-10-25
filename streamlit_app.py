import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

UNI_BRISTOL_LOGO_WIDE = "images/uni_bristol_logo.png"
UNI_BRISTOL_ICON = "images/uni_bristol_icon.png"

# Set page config
st.set_page_config(page_title="Unexpected insulin needs", layout="wide")

# Sidebar
st.logo(
        UNI_BRISTOL_LOGO_WIDE,
        size="large",
        link="https://www.bristol.ac.uk/cdt/interactive-ai/",
        icon_image=UNI_BRISTOL_ICON)
st.sidebar.markdown('''
# Content	
:clipboard: [Background](#background)

:dart: [Objective](#objective)

:microscope: [Methods](#methods)

:bar_chart: [Results](#results)

:bulb: [Conclusions](#conclusions)

:mailbox: [Contact us](#contact-us)
''', unsafe_allow_html=True)

# Main body
st.title("Patterns in insulin needs of people with Type 1 Diabetes")
st.markdown('''
**Isabella Degen, Kate Robson Brown, Henry W. J. Reeve, Zahraa S. Abdallah**

An interactive dashboard exploring  patterns in insulin needs, carbohydrate intake, and glucose levels from automated 
insulin delivery systems. You can read the full paper on JMIRx Med: http://dx.doi.org/10.2196/44384.

:warning: *This site is under construction and the figures are completely fictional. The text is the abstract from the paper
that needs updating and shortening for this format.* :warning:
''')

st.header(':clipboard: Background', anchor='background')
st.markdown(
    '''
    Type 1 Diabetes (T1D) is a chronic condition in which the body produces too little insulin, a hormone needed to 
    regulate blood glucose. Various factors such as carbohydrates, exercise and hormones impact insulin needs. Beyond 
    carbohydrates, most factors remain under-explored. Regulating insulin is a complex control task that can go wrong 
    and cause blood glucose levels to fall outside a range that protects people from adverse health effects. Automated 
    insulin delivery (AID) has been shown to maintain blood glucose levels within a narrow range. Beyond clinical 
    outcomes, data from AID systems is little researched and promises new data-driven insights to improve the 
    understanding and treatment of T1D.
    ''')

st.header(':dart: Objective', anchor='objective')
st.markdown(
    '''
    The aim is to discover unexpected temporal patterns in insulin needs and to analyse how frequently these occur. 
    Unexpected patterns are situations where increased insulin does not result in lower glucose, or increased 
    carbohydrate intake does not raise glucose levels. Such situations suggest that factors beyond carbohydrates 
    influence insulin needs.    
    
    *TODO: Add visualisation for expected and unexpected patterns*
    
    ''')

st.header(':microscope: Methods', anchor='methods')
st.markdown(
    '''
    We analysed time series data on insulin on board (IOB), carbohydrates on board (COB) and interstitial glucose 
    (IG) from 29 participants using the OpenAPS AID system. Pattern frequency in hours, days 
    (grouped via K-means clustering), weekdays, and months were determined by comparing the 95% CI of the mean 
    differences between temporal units. Associations between pattern frequency and demographic variables were examined. 
    Significant differences in IOB, COB and IG for various time categories were assessed using Mann-Whitney U tests. 
    Effect sizes and Euclidean distances between variables were calculated. Finally, the forecastability of IOB, COB, 
    and IG for the clustered days was analysed using Granger causality.
    ''')

st.header(':bar_chart: Results', anchor='results')
st.markdown(
    '''
    On average, 13.5 participants had unexpected patterns and 9.9 had expected patterns. 
    The patterns were more pronounced (d>0.94) when comparing hours of the day and similar days than when comparing 
    days of the week or months (0.3<d<0.52). Notably, 11 participants exhibited a higher IG overnight despite 
    concurrently higher IOB (10 of 11). Additionally, 17 participants experienced an increase in IG after COB 
    decreased post-meals. The significant associations between pattern frequency and demographics 
    were moderate (0.31≤\tau≤0.48). 
    Between clusters, mean IOB (P=.03, d=0.7) and IG (P=.02, d=0.67) differed significantly, 
    but not COB (P=.08, d=0.55). IOB and IG were most similar (mean distance 5.08, SD 2.25), 
    while COB and IG were most different (mean distance 11.43, SD 2.6), suggesting that AID attempts to counteract both 
    observed and unobserved factors that impact IG.
    ''')

st.markdown('''
:warning: *These graphs are currently fictional. Just to give an idea of how the results could be 
presented in an interactive way.*
''')

pattern_type = st.selectbox(
    "Choose pattern to explore:",
    ["Overnight Patterns", "Post-Meal Patterns", "Daily Clusters"]
)


# Function to load your data
@st.cache_data  # This caches the data to improve performance
def load_data():
    # Replace this with your actual data loading logic
    # Example format of what your data might look like:
    df = pd.DataFrame({
        'time': pd.date_range(start='2024-01-01', periods=24, freq='H'),
        'glucose': [140, 145, 150, 160, 165, 170, 165, 160] * 3,
        'insulin': [2.5, 2.7, 3.0, 3.2, 3.3, 3.4, 3.2, 3.0] * 3,
        'carbs': [0, 0, 0, 0, 0, 0, 0, 0] * 3
    })
    return df


# Load the data
df = load_data()

# Create different visualizations based on pattern type
if pattern_type == "Overnight Patterns":
    st.header("Overnight Glucose Patterns")
    st.markdown("""
    ### Key Finding
    11 participants exhibited higher glucose levels overnight despite higher insulin on board.
    """)

    # Create subplot with shared x-axis
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True)

    # Add glucose trace
    fig.add_trace(
        go.Scatter(x=df['time'], y=df['glucose'], name="Glucose"),
        row=1, col=1
    )

    # Add insulin trace
    fig.add_trace(
        go.Scatter(x=df['time'], y=df['insulin'], name="Insulin"),
        row=2, col=1
    )

    fig.update_layout(height=600, title_text="Glucose vs Insulin Overnight")
    st.plotly_chart(fig, use_container_width=True)

elif pattern_type == "Post-Meal Patterns":
    st.header("Post-Meal Response Patterns")
    st.markdown("""
    ### Key Finding
    17 participants showed increased glucose levels after carbohydrates decreased post-meals.
    """)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['time'], y=df['glucose'], name="Glucose"))
    fig.add_trace(go.Scatter(x=df['time'], y=df['carbs'], name="Carbs"))
    fig.update_layout(title="Post-Meal Glucose and Carbohydrate Patterns")
    st.plotly_chart(fig, use_container_width=True)

else:  # Daily Clusters
    st.header("Daily Pattern Clusters")
    st.markdown("""
    ### Key Finding
    Significant differences in insulin on board (P=.03, d=0.7) and glucose (P=.02, d=0.67) 
    between clusters.
    """)

    # Add your clustering visualization here
    # Example: showing different clusters
    cluster_fig = px.scatter(df, x='insulin', y='glucose',
                             title="Clusters of Daily Patterns")
    st.plotly_chart(cluster_fig, use_container_width=True)

# Add statistical insights
st.header("Statistical Insights")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Average Participants with Unexpected Patterns",
        value="13.5"
    )

with col2:
    st.metric(
        label="Effect Size for Hour Patterns",
        value="d > 0.94"
    )

with col3:
    st.metric(
        label="IOB-IG Distance",
        value="5.08 ± 2.25"
    )

st.header(':bulb: Conclusions', anchor='conclusions')
st.markdown(
    '''Our study shows that unexpected patterns in the insulin needs of people with T1D are as common as expected 
    patterns. Unexpected patterns cannot be explained by carbohydrates alone. 
    Our results highlight the complexity of glucose regulation and emphasise the need for personalised treatment 
    approaches. Further research is needed to identify and quantify the factors that cause these patterns.''')

st.header(":mailbox: Contact us", anchor='contact-us')

# <form action="https://formsubmit.co/3d80f75bd493b7edbca0a868b9c6dbe6" method="POST">
contact_form = """
<form action="https://formsubmit.co/3d80f75bd493b7edbca0a868b9c6dbe6" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your name" required>
     <input type="email" name="email" placeholder="Your email" required>
     <input type="hidden" name="_subject" value="Streamline Contact for insulin need demo app">
     <input type="hidden" name="_next" value="https://insulin-need-patterns.streamlit.app/?embed=true">
     <input type="hidden" name="_captcha" value="true">
     <textarea name="message" placeholder="Your message here"></textarea>
     <button type="submit" class="sendbutton">
        <span class="sendbutton__text">Send</span>
     </button>
</form>
"""

st.markdown(contact_form, unsafe_allow_html=True)


# Use Local CSS File
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")

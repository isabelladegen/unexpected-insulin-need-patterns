import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

UNI_BRISTOL_LOGO_WIDE = "images/uni_bristol_logo.png"
UNI_BRISTOL_ICON = "images/uni_bristol_icon.png"
QR_CODE = "images/qr_code.png"

# other content
content_title = "Beyond Expected Patterns in Type 1 Diabetes"

# Get the config values
secondary_bg_color = st.get_option("theme.secondaryBackgroundColor")
text_colour = st.get_option("theme.textColor")
expected_colour = '#cfe2f3'  # Light blue
unexpected_colour = '#46bdc6'  # Turquoise

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


# Function to load your data
@st.cache_data  # This caches the data to improve performance
def load_data():
    # Replace this with your actual data loading logic
    # Example format of what your data might look like:
    df = pd.DataFrame({
        'time': pd.date_range(start='2024-01-01', periods=24, freq='h'),
        'glucose': [140, 145, 150, 160, 165, 170, 165, 160] * 3,
        'insulin': [2.5, 2.7, 3.0, 3.2, 3.3, 3.4, 3.2, 3.0] * 3,
        'carbs': [0, 0, 0, 0, 0, 0, 0, 0] * 3
    })
    return df


pattern_frequency_df = pd.read_csv("data/pattern_frequency.csv", index_col=0)

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


def main():
    # Set page config
    st.set_page_config(
        page_title="Unexpected insulin needs",
        page_icon=UNI_BRISTOL_ICON,
        layout="wide",
    )

    # Load css
    local_css("style/style.css")

    # Sidebar
    st.logo(
        UNI_BRISTOL_LOGO_WIDE,
        size="large",
        link="https://www.bristol.ac.uk/cdt/interactive-ai/",
        icon_image=UNI_BRISTOL_ICON)

    st.sidebar.title(content_title)

    page_1 = "📊 Key Findings"
    page_2 = "🔍 Explore Patterns"
    page_3 = "⏰ Time of Day Analysis"
    page_4 = "👤 Individual Variations"
    page_5 = "🎯 Why This Matters"
    page = st.sidebar.radio(
        "Explore...",
        [page_1, page_2, page_3, page_4, page_5]
    )

    # old sidebar
    # st.sidebar.markdown('''
    # ### UKRI Center for Doctoral Training in Interactive AI

    # Main body content
    st.title(content_title)

    # Content based on selection
    if page == page_1:
        display_main_findings()

    if page == page_2:
        display_page2()

    if page == page_3:
        display_page3()

    if page == page_4:
        display_page4()

    if page == page_5:
        display_page5()

    # old_page_content()

    # Footer
    footer = """<div class='footer'>
    <p><a href="https://dx.doi.org/10.2196/44384)">Full Paper</a> | Isabella Degen | Kate Robson Brown | Henry W. J. Reeve | Zahraa S. Abdallah</p>
    </div>"""
    st.markdown(footer, unsafe_allow_html=True)


def old_page_content():
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
    # Contact us
    st.header(":mailbox: Contact us", anchor='contact-us')
    st.markdown(contact_form, unsafe_allow_html=True)


def display_page5():
    st.header("Page 5")


def display_page4():
    st.header("Page 4")


def display_page3():
    st.header("Page 3")


def display_page2():
    st.header("Explore Patterns")
    # Split view layout
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Pattern Animation")
        # Placeholder for animation
        st.image("images/placeholder_img.jpg")
    with col2:
        st.subheader("Pattern Details")
        # Example pattern details
        st.markdown("""
            ### Pattern Description
            This section shows detailed information about the selected pattern.

            - Type: Unexpected
            - Frequency: Common
            - Time of occurrence: Night
            """)
    # Controls section
    st.subheader("Interactive Controls")
    col3, col4 = st.columns(2)
    with col3:
        pattern_select = st.selectbox(
            "Select Pattern",
            ["Night High Glucose", "Post-meal Rise", "Other"]
        )
    with col4:
        time_period = st.selectbox(
            "Time Period",
            ["24 hours", "1 week", "1 month"]
        )


def create_pattern_plot(df, selected_patterns):
    # filter data by selected patterns, 1, 2, 3
    filtered_df = df[df['pattern_number'].isin(selected_patterns)]
    pattern_types = df['pattern_type'].unique().tolist()

    fig = go.Figure()

    # Colors matching your image
    colors = {
        'Expected': expected_colour,  # Light blue
        'Unexpected': unexpected_colour  # Turquoise
    }
    order = ['Months of the year', 'Days of the week', 'Clusters', 'Hours of the day']

    # Add traces for each pattern type
    for pattern_type in pattern_types:
        pattern_data = filtered_df[filtered_df['pattern_type'] == pattern_type]

        # Calculate mean values when multiple patterns are selected
        grouped_data = (
            pattern_data.groupby('timeframe').agg({'mean': ['mean', 'std']}).round(2).reindex(order).reset_index())

        fig.add_trace(go.Bar(
            name=f'{pattern_type} Pattern(s): ' + ', '.join([str(x) for x in selected_patterns]),
            y=grouped_data['timeframe'],
            x=grouped_data['mean']['mean'],
            error_x=dict(
                type='data',
                array=grouped_data['mean']['std'],
                visible=True,
                color='#444'
            ),
            orientation='h',
            marker_color=colors[pattern_type],
            hovertemplate=(
                    '%{fullData.name}<br>' +
                    'Average: %{x:.1f} ± %{error_x.array:.1f} people<br>' +
                    'Timeframe: %{y}<extra></extra>'
            )
        ))

    # Update layout
    fig.update_layout(
        xaxis_title='Average number of people (total n=29)',
        xaxis=dict(
            range=[0, 30],
            zeroline=True,
            showgrid=True
        ),
        yaxis=dict(
            title='',
            zeroline=False,
            showgrid=False
        ),
        barmode='group',
        margin=dict(l=150, r=20, t=20, b=40),
        showlegend=False,
        legend=dict(
            x=0,
            y=1.2
        ),
        width=800,
        height=350
    )

    return fig


def display_main_findings():
    # Key Findings section
    st.subheader("Key Finding: Unexpected Patterns are as common as expected patterns")

    st.caption("Select from patterns 1-3 to see how many people have these patterns:")

    col1, col2, col3 = st.columns(3)

    pattern_selections = {}
    with col1:
        st.markdown('<p class="pattern-header"><strong>Patterns</strong></p>', unsafe_allow_html=True)
        pattern_selections[1] = st.checkbox('Pattern 1: More insulin...', value=True)
        pattern_selections[2] = st.checkbox('Pattern 2: Higher blood glucose...', value=True)
        pattern_selections[3] = st.checkbox('Pattern 3: Eating more carbs...', value=True)

    with col2:
        st.markdown("""
            <div class="expected-col">
                <p><strong>Expected Reason</strong></p>
                <p>... is needed for more carbs being eaten.</p>
                <p>... is due to eating more carbs.</p>
                <p>... needs more insulin.</p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="unexpected-col">
                <p><strong>Unexpected Reason</strong></p>
                <p>... is not due more carbs being eaten.</p>
                <p>... is not due more carbs being eaten.</p>
                <p>... does not need more insulin.</p>
            </div>
        """, unsafe_allow_html=True)

    selected_pattern_numbers = [k for k, v in pattern_selections.items() if v]

    # Create and display plot
    if selected_pattern_numbers:  # Only show plot if at least one pattern is selected
        fig = create_pattern_plot(pattern_frequency_df, selected_pattern_numbers)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please select at least one pattern to display.")


if __name__ == "__main__":
    main()

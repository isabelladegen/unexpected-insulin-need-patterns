import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit.components.v1 import html

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


def load_custom_js(file_name):
    with open(file_name, 'r') as file:
        js_content = file.read()
        html(f"<script>{js_content}</script>", height=0)


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
meal_rise_stats_df = pd.read_csv('data/figure-2a-stats-results.csv', header=[0, 1, 2], index_col=0)
night_high_1_stats_df = pd.read_csv('data/figure-3a-stats-results.csv', header=[0, 1, 2], index_col=0)
night_high_2_stats_df = pd.read_csv('data/figure-3b-stats-results.csv', header=[0, 1, 2], index_col=0)

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

    # Load css and js
    local_css("style/style.css")
    load_custom_js("scripts/style_metrics.js")

    # Sidebar
    st.logo(
        UNI_BRISTOL_LOGO_WIDE,
        size="large",
        link="https://www.bristol.ac.uk/cdt/interactive-ai/",
        icon_image=UNI_BRISTOL_ICON)

    st.sidebar.title(content_title)

    page_1 = "📊 Key Findings"
    page_2 = "🔍 Explore Patterns"
    # page_3 = ":clock1: Time of Day Analysis"
    page_4 = "👤 Individual Variations"
    page_5 = "🎯 Why This Matters"
    page = st.sidebar.radio(
        "Explore...",
        [page_1, page_2, page_4, page_5]
    )

    # old sidebar
    # st.sidebar.markdown('''
    # ### UKRI Center for Doctoral Training in Interactive AI

    # Main body content
    st.title(content_title)
    st.markdown("*Isabella Degen | Kate Robson Brown | Henry W. J. Reeve | Zahraa S. Abdallah*")
    st.markdown("[Full paper](https://dx.doi.org/10.2196/44384)")

    # Content based on selection
    if page == page_1:
        display_main_findings()

    if page == page_2:
        explore_patterns()

    # if page == page_3:
    #     display_page3()

    if page == page_4:
        display_page4()

    if page == page_5:
        display_why_this_matters()

    # # Footer
    # footer = """<div class='footer'>
    # <p><a href="https://dx.doi.org/10.2196/44384)">Full Paper</a> | Isabella Degen | Kate Robson Brown | Henry W. J. Reeve | Zahraa S. Abdallah</p>
    # </div>"""
    # st.markdown(footer, unsafe_allow_html=True)


def load_pattern_images():
    """Load and cache pattern images"""

    @st.cache_resource
    def _load_images():
        return {
            "Night High Glucose": Image.open("night_glucose.png"),
            "Post-meal Rise": Image.open("postmeal.png"),
            "Other": Image.open("other_pattern.png")
        }

    return _load_images()


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


def display_why_this_matters():
    st.header("Why this matters")
    st.subheader("Unexpected patterns are as frequent as expected patterns")
    st.markdown('''
    > This shows that factors beyond carbohydrates substantially influence blood glucose regulation.
    ''')
    with st.expander("Unexpected patterns explained"):
        st.markdown('''
            Unexpected patterns are times when an increase of insulin doesn't lower blood glucose and/or when eating
            more carbohydrates does not raise blood glucose.
            
            The hormone insulin is expected to enable the cells to take up glucose from the blood which should lead to
            glucose falling. When insulin doesn't lower blood glucose it shows that either more glucose is entering the
            blood stream than the insulin can cover or that other factors make insulin less effective than usually.
            
            Carbohydrates in Type 1 Diabetes lead to glucose raising due to the body not producing the required insulin.
            When carbohydrates don't raise blood glucose it shows that too much insulin has been injected or that
            other factors make insulin more effective than usually.    
        ''')

    st.markdown('''
    > Currently, automated insulin delivery systems are 'flying blind' to these additional factors.
    ''')
    with st.expander("Impact explained"):
        st.markdown('''
                    Due to these additional factor not being systematically quantified and considered in insulin dosing
                    automated insulin delivery systems need to take a cautious approach which can lead to
                    blood glucose levels going out of the healthy range and even require manual interventions from
                    the person with diabetes. Manual interventions in automated insulin delivery can cause the 
                    system to not appropriately asses the situation and can lead to dangerous situations.
                    Manual interventions can also be difficult for the person to deal with.
                ''')

    st.subheader(
        'Insulin requirements vary wildly between individuals and even for the same individual at different times')
    st.markdown('''
        > This highlights that dynamic and personalised approaches to dosing insulin are essential.
        ''')


def display_page4():
    st.header("Page 4")


def display_page3():
    st.header("Page 3")


def explore_patterns():
    patterns = {'night_high_1': "High Glucose during night - Version 1",
                'night_high_2': "High Glucose during night - Version 2",
                'post_meal_rise': "Post meal rise"
                }
    st.subheader("Explore Patterns")

    # Controls section
    pattern_select = st.selectbox(
        "Select pattern",
        list(patterns.values())
    )

    # Split view layout
    col1, col2 = st.columns([0.7, 0.3])
    with col1:  # plot
        if pattern_select == patterns['night_high_1']:
            fig = plot_cluster_confidence_intervals_for_df(night_high_1_stats_df)
            st.plotly_chart(fig, use_container_width=True)
        if pattern_select == patterns['night_high_2']:
            fig = plot_cluster_confidence_intervals_for_df(night_high_2_stats_df)
            st.plotly_chart(fig, use_container_width=True)
        if pattern_select == patterns['post_meal_rise']:
            fig = plot_cluster_confidence_intervals_for_df(meal_rise_stats_df)
            st.plotly_chart(fig, use_container_width=True)
        st.caption("The graph shows scaled, hourly mean readings and 95% confidence intervals for insulin, "
                   "carbohydrates and blood glucose seperated into two clusters")
    with col2:  # description
        st.write("")
        st.write("")
        st.subheader(pattern_select)
        if pattern_select == patterns['night_high_1']:
            st.metric("People with night highs", "11 of 28")
            st.markdown(
                '<div class="unexpected-pattern">Unexpected Pattern 2: Higher Blood Glucose is not due to more carbs being eaten.</div>',
                unsafe_allow_html=True)
            st.markdown("""Cluster 2 shows significantly higher blood glucose readings in the early part of the night 
                            (6 UTC).""")

        if pattern_select == patterns['night_high_2']:
            st.metric("People with night highs", "11 of 28")
            st.markdown(
                '<div class="unexpected-pattern">Unexpected Pattern 2: Higher Blood Glucose is not due to more carbs being eaten.</div>',
                unsafe_allow_html=True)
            st.markdown("""Cluster 2 shows significantly higher blood glucose readings in the the night (8 UTC).""")

        if pattern_select == patterns['post_meal_rise']:
            st.metric("People with night highs", "17 of 28")
            st.markdown(
                '<div class="unexpected-pattern">Unexpected Pattern 2: Higher Blood Glucose is not due to more carbs being eaten.</div>',
                unsafe_allow_html=True)
            st.markdown("""Both clusters show blood glucose rising post meals (carbohydrates spikes), see Cluster 1: 14
            UTC and Cluster 2: 2 UTC""")


def plot_cluster_confidence_intervals_for_df(df):
    # Get counts for each cluster from the data
    df = df.round(2)
    cluster_counts = {
        0: df[('0', 'count', 'xtrain iob mean')].iloc[0],
        1: df[('1', 'count', 'xtrain iob mean')].iloc[0]
    }

    # Create figure with subplots
    fig = make_subplots(
        rows=2, cols=1,
        vertical_spacing=0.05,
        shared_xaxes=True,
    )

    # Colors matching the matplotlib version
    colors = {
        'iob': '#1f77b4',
        'cob': '#ff7f0e',
        'bg': '#2ca02c'
    }

    # Names for legend
    metric_names = {
        'iob': 'Insulin',
        'cob': 'Carbohydrates',
        'bg': 'Blood Glucose'
    }

    # Plot for each cluster
    for cluster_idx in [0, 1]:
        row = cluster_idx + 1

        for metric_key, metric_name in metric_names.items():
            base_col = f'xtrain {metric_key} mean'
            color = colors[metric_key]

            # Add confidence interval as a filled area
            x_data = df.index.tolist()
            ci_hi = df[(str(cluster_idx), 'ci96_hi', base_col)]
            ci_lo = df[(str(cluster_idx), 'ci96_lo', base_col)]

            fig.add_trace(
                go.Scatter(
                    name=f'{metric_name} CI',
                    x=x_data + x_data[::-1],
                    y=ci_hi.tolist() + ci_lo.tolist()[::-1],
                    fill='toself',
                    fillcolor=f'rgba{tuple(list(int(color.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)) + [0.2])}',
                    line=dict(color='rgba(255,255,255,0)'),
                    showlegend=False,
                    hoverinfo='skip',
                ),
                row=row, col=1
            )

            # Add mean line
            fig.add_trace(
                go.Scatter(
                    name=metric_name,
                    x=x_data,
                    y=df[(str(cluster_idx), 'mean', base_col)],
                    mode='lines+markers',
                    line=dict(color=color, width=2),
                    marker=dict(size=6),
                    showlegend=False if cluster_idx == 1 else True,
                ),
                row=row, col=1
            )

    # Update layout
    fig.update_layout(
        height=500,
        showlegend=True,
        legend=dict(
            yanchor="top",  # Anchor to bottom of legend box
            y=1.1,  # Position between the two plots (adjust as needed)
            xanchor="center",
            x=0.5,
            orientation="h"
        ),
        hovermode='x unified'
    )

    # Update axes
    for i in [1, 2]:
        title = f"Cluster {i} ({cluster_counts[i - 1]} days)"
        fig.update_yaxes(title_text=title, row=i, col=1)
        fig.update_xaxes(
            title_text="Hour of day (UTC)" if i == 2 else None,
            tickmode='array',
            tickvals=list(range(0, 24, 2)),
            row=i, col=1
        )

    return fig


def create_pattern_plot(df, selected_patterns):
    # filter data by selected patterns, 1, 2, 3
    filtered_df = df[df['pattern_number'].isin(selected_patterns)]
    pattern_types = df['pattern_type'].unique().tolist()
    pattern_types = pattern_types[::-1]  # Reverse to put 'Expected' last which will plot it first

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
            showgrid=False,
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
    st.subheader("Unexpected Patterns are as common as expected patterns")

    st.caption("Select from patterns 1-3 to see how many of the 29 people have expected and unexpected patterns:")

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
                <p><strong>Expected Reasons</strong></p>
                <p>... is needed for more carbs being eaten.</p>
                <p>... is due to eating more carbs.</p>
                <p>... needs more insulin.</p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="unexpected-col">
                <p><strong>Unexpected Reasons</strong></p>
                <p>... is not due more carbs being eaten.</p>
                <p>... is not due more carbs being eaten.</p>
                <p>... does not need more insulin.</p>
            </div>
        """, unsafe_allow_html=True)

    # Create and display plot
    selected_pattern_numbers = [k for k, v in pattern_selections.items() if v]
    if selected_pattern_numbers:  # Only show plot if at least one pattern is selected
        filtered_df = pattern_frequency_df[pattern_frequency_df['pattern_number'].isin(selected_pattern_numbers)]
        avg_expected = filtered_df[filtered_df['pattern_type'] == 'Expected']['mean'].mean().round(1)
        avg_unexpected = filtered_df[filtered_df['pattern_type'] == 'Unexpected']['mean'].mean().round(1)
        # Display key metrics
        st.write("")  # add space
        col1, col2, col3 = st.columns(3)
        col1.metric("People with pattern", "Avg.")
        col2.metric("Expected Patterns", str(avg_expected))
        col3.metric("Unexpected Patterns", str(avg_unexpected))
        # plot
        fig = create_pattern_plot(pattern_frequency_df, selected_pattern_numbers)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please select at least one pattern to display.")


if __name__ == "__main__":
    main()

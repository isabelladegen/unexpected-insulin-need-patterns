import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit.components.v1 import html

from inividual_variations import display_individual_variations
from plot_cluster_interval import plot_cluster_confidence_intervals_for_df, daily_ts_graph_description_text
from why_this_matters import display_why_this_matters

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


pattern_frequency_df = pd.read_csv("data/pattern_frequency.csv", index_col=0)
meal_rise_stats_df = pd.read_csv('data/figure-2a-stats-results.csv', header=[0, 1, 2], index_col=0)
night_high_1_stats_df = pd.read_csv('data/figure-3a-stats-results.csv', header=[0, 1, 2], index_col=0)
night_high_2_stats_df = pd.read_csv('data/figure-3b-stats-results.csv', header=[0, 1, 2], index_col=0)


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
    st.markdown("We discovered interesting temporal patterns in the insulin needs of people with Type 1 Diabetes "
                "that cannot be explained by carbohydrate intake alone.")
    st.markdown("[Full paper](https://dx.doi.org/10.2196/44384)")

    # Content based on selection
    if page == page_1:
        display_main_findings()

    if page == page_2:
        explore_patterns()

    # if page == page_3:
    #     display_page3()

    if page == page_4:
        display_individual_variations()

    if page == page_5:
        display_why_this_matters()

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
        st.caption(daily_ts_graph_description_text)
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
    st.subheader("Unexpected patterns are as common as expected patterns")
    st.markdown("We currently do not systematically account for unexpected patterns. Their frequency is a surprise.")
    st.caption("Select from patterns 1-3 to see how many of the 29 people have these expected and unexpected patterns:")

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

    st.divider()
    # CORRELATION SECTION
    st.subheader("No pattern is strongly associated with demographic information")
    st.markdown("**Strong Correlations** (τ > 0.7)")
    st.markdown("None.")
    st.markdown("**Weak Correlations** (τ ≤ 0.31)")
    st.markdown("""
        - Age
        - Years with T1D
        - Amount of daily carbs eaten
        - Amount of daily basal insulin
        - Length of CGM and AID use
        """)

    # Define correlation data
    correlations = {
        1: {
            "expected": {
                "A1c": {"direction": "↓", "tau": "-0.41"},
                "Mean Glucose": {"direction": "↓0.", "tau": "-0.38"},
                "Mean Carbs": {"direction": "↑", "tau": "0.45 "}
            },
            "unexpected": {
                "A1c": {"direction": "↑", "tau": "0.42"},
                "Mean glucose": {"direction": "↑", "tau": "0.36"}
            }
        },
        2: {
            "expected": {
                "A1c": {"direction": "↑", "tau": "0.35"},
                "Mean glucose": {"direction": "↓", "tau": "0.35"}
            },
            "unexpected": {
                "A1c": {"direction": "↑", "tau": "0.39"},
                "Yars of pump experience": {"direction": "↓", "tau": "0.33-0.35"}
            }
        },
        3: {
            "expected": {},  # no significant correlations
            "unexpected": {}  # no significant correlations
        }
    }

    st.markdown("**Medium Correlations** (0.31 < τ ≤ 0.48)",
                help="Explanations: τ = Kendall's Tau, frequency of pattern ↑ increases/↓ decreases")
    corr_pattern_selections = {}
    corr_pattern_selections[1] = st.checkbox(
        'Pattern 1: More insulin  → more carbs (expected) | → not more carbs (unexpected)', value=True)
    corr_pattern_selections[2] = st.checkbox(
        'Pattern 2: Higher blood glucose → more carbs (expected) | → not more carbs (unexpected)', value=True)
    corr_pattern_selections[3] = st.checkbox(
        'Pattern 3: Eating more carbs → more insulin (expected) | → not more insulin (unexpected)', value=True)

    # select which medium correlations remain
    selected_corr_pattern_numbers = [k for k, v in corr_pattern_selections.items() if v]
    ps_of_expected_patterns = ""
    ps_of_unexpected_patterns = ""

    for pattern_num in selected_corr_pattern_numbers:
        if correlations[pattern_num]["expected"]:
            sub_e_patterns = []
            for measure, data in correlations[pattern_num]["expected"].items():
                sub_e_patterns.append(f"{measure} {data['direction']}")
            if sub_e_patterns:
                substring_e = ", ".join(sub_e_patterns)
                ps_of_expected_patterns = ps_of_expected_patterns + f"<p><strong>Pattern {pattern_num}:</strong> {substring_e}</p>"
            else:
                ps_of_expected_patterns = "<p>None</p>"
        if correlations[pattern_num]["unexpected"]:
            sub_un_patterns = []
            for measure, data in correlations[pattern_num]["unexpected"].items():
                sub_un_patterns.append(f"{measure} {data['direction']}")
            if sub_un_patterns:
                substring_un = ", ".join(sub_un_patterns)
                ps_of_unexpected_patterns = ps_of_unexpected_patterns + f"<p><strong>Pattern {pattern_num}:</strong> {substring_un}</p>"
            else:
                ps_of_unexpected_patterns = "<p>None</p>"

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
                   <div class="expected-col">
                       <p><strong>Expected Associations</strong></p>
                       {ps_of_expected_patterns}
                   </div>
               """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
                  <div class="unexpected-col">
                      <p><strong>Unexpected Associations</strong></p>
                      {ps_of_unexpected_patterns}
                  </div>
              """, unsafe_allow_html=True)

    st.caption("Note: Only correlations where τ ≥ 0.36 achieved statistical power ≥80%")


if __name__ == "__main__":
    main()

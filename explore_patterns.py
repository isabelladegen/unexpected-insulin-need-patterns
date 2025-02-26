import pandas as pd
import streamlit as st

from inividual_variations import different_days_stats_df
from key_findings import display_unexpected_reason, patterns_by_number
from plot_cluster_interval import plot_cluster_confidence_intervals_for_df, daily_ts_graph_description_text, \
    select_chart_type, colored_text

meal_rise_stats_df = pd.read_csv('data/figure-2a-stats-results.csv', header=[0, 1, 2], index_col=0)
# night_high_1_stats_df = pd.read_csv('data/figure-3a-stats-results.csv', header=[0, 1, 2], index_col=0)
night_high_2_stats_df = pd.read_csv('data/figure-3b-stats-results.csv', header=[0, 1, 2], index_col=0)
iob_higher_cob_not_df = pd.read_csv('data/iob_higher_cob_is_not.csv', header=[0, 1, 2], index_col=0)


def display_explore_patterns():
    patterns = {'iob_higher_cob_not': "Unexpected Pattern 1: Insulin significantly higher while carbs are similar",
        'night_high_2': "Unexpected Pattern 2: Significantly higher glucose during night",
        'post_meal_rise': "Unexpected Pattern 2: Post meal rise",
        'more_carbs': "Unexpected Pattern 3: Eating more carbs without needing more insulin",
    }
    highlighted_patterns = {
        patterns[
            'iob_higher_cob_not']: f"More {colored_text('insulin', 'iob')} was not due to more {colored_text('carbs', 'cob')}",
        patterns['night_high_2']: f"High {colored_text('Glucose', 'bg')} during night",
        patterns['more_carbs']: f"Eating more {colored_text('carbs', 'cob')} did not need more {colored_text('insulin', 'iob')}",
        patterns['post_meal_rise']: f"Post {colored_text('meal', 'cob')} rise"
    }
    # st.header(explore_patterns)

    # Controls section
    pattern_select = st.selectbox(
        "Select from the patterns below to see examples of unexpected patterns comparing the same hours between different days.",
        list(patterns.values())
    )

    # Split view layout
    col1, col2 = st.columns([0.3, 0.7])
    with col1:  # description
        st.write("")
        st.write("")
        # subheader
        st.markdown(f"""### {highlighted_patterns[pattern_select]}""", unsafe_allow_html=True)
        if pattern_select == patterns['iob_higher_cob_not']:
            # st.metric("People with night highs", "11 of 28")
            st.markdown("""##### Unexpected Pattern:""")
            st.markdown(f"""{display_unexpected_reason(patterns_by_number[1])}""", unsafe_allow_html=True)
            st.markdown(f"""Cluster 1 shows significantly higher {colored_text('insulin', 'iob')} especially from 13 onwards, while {colored_text('carbs', 'cob')} are the same as in Cluster 2. Despite the higher {colored_text('insulin', 'iob')}, {colored_text('blood glucose', 'bg')} too is significantly higher.""", unsafe_allow_html=True)

        # if pattern_select == patterns['night_high_1']:
        #     st.metric("People with night highs", "11 of 28")
        #     st.markdown("""##### Unexpected Pattern:""")
        #     st.markdown(f"""{display_unexpected_reason(patterns_by_number[2])}""", unsafe_allow_html=True)
        #     st.markdown(f"""Cluster 2 shows significantly higher {colored_text('blood glucose', 'bg')} readings in the early part of the night
        #                        (6 UTC).""", unsafe_allow_html=True)

        if pattern_select == patterns['night_high_2']:
            st.metric("People with night highs", "11 of 28")
            st.markdown("""##### Unexpected Pattern:""")
            st.markdown(f"""{display_unexpected_reason(patterns_by_number[2])}""", unsafe_allow_html=True)
            st.markdown(
                f"""Cluster 2 shows significantly higher {colored_text('blood glucose', 'bg')} readings in the the night (8 UTC).""",
                unsafe_allow_html=True)

        if pattern_select == patterns['more_carbs']:
            st.markdown("""##### Unexpected Pattern:""")
            st.markdown(f"""{display_unexpected_reason(patterns_by_number[3])}""", unsafe_allow_html=True)
            st.markdown(
                f"""Cluster 2 shows significantly more {colored_text('carbs', 'cob')} around 19 UTC alongside lower {colored_text('blood glucose', 'bg')} and similar  {colored_text('insulin', 'iob')}.""",
                unsafe_allow_html=True)

        if pattern_select == patterns['post_meal_rise']:
            st.metric("People with night highs", "17 of 28")
            st.markdown("""##### Unexpected Pattern:""")
            st.markdown(f"""{display_unexpected_reason(patterns_by_number[2])}""", unsafe_allow_html=True)
            st.markdown(
                f"""Both clusters show {colored_text('blood glucose', 'bg')} rising post meals ({colored_text('carbohydrates', 'cob')} spikes), see Cluster 1: 14
               UTC and Cluster 2: 2 UTC""", unsafe_allow_html=True)
    with col2:  # plot
        # Select chart type
        graph_layout = select_chart_type(key="explore_patterns_graph_layout")
        if pattern_select == patterns['iob_higher_cob_not']:
            fig = plot_cluster_confidence_intervals_for_df(iob_higher_cob_not_df, fix_y=7, plot_type=graph_layout)
            st.plotly_chart(fig, use_container_width=True)
        # if pattern_select == patterns['night_high_1']:
        #     fig = plot_cluster_confidence_intervals_for_df(night_high_1_stats_df, fix_y=7, plot_type=graph_layout)
        #     st.plotly_chart(fig, use_container_width=True)
        if pattern_select == patterns['night_high_2']:
            fig = plot_cluster_confidence_intervals_for_df(night_high_2_stats_df, fix_y=7, plot_type=graph_layout)
            st.plotly_chart(fig, use_container_width=True)
        if pattern_select == patterns['more_carbs']:
            fig = plot_cluster_confidence_intervals_for_df(different_days_stats_df, fix_y=7, plot_type=graph_layout)
            st.plotly_chart(fig, use_container_width=True)
        if pattern_select == patterns['post_meal_rise']:
            fig = plot_cluster_confidence_intervals_for_df(meal_rise_stats_df, fix_y=6, plot_type=graph_layout)
            st.plotly_chart(fig, use_container_width=True)
        st.caption(daily_ts_graph_description_text)

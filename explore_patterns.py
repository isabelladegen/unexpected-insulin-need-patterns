import pandas as pd
import streamlit as st

from constants import explore_patterns
from plot_cluster_interval import plot_cluster_confidence_intervals_for_df, daily_ts_graph_description_text

meal_rise_stats_df = pd.read_csv('data/figure-2a-stats-results.csv', header=[0, 1, 2], index_col=0)
night_high_1_stats_df = pd.read_csv('data/figure-3a-stats-results.csv', header=[0, 1, 2], index_col=0)
night_high_2_stats_df = pd.read_csv('data/figure-3b-stats-results.csv', header=[0, 1, 2], index_col=0)


def display_explore_patterns():
    patterns = {'night_high_1': "High Glucose during night - Version 1",
                'night_high_2': "High Glucose during night - Version 2",
                'post_meal_rise': "Post meal rise"
                }
    st.header(explore_patterns)

    # Controls section
    pattern_select = st.selectbox(
        "Select from the patterns below to see examples of unexpected daily patterns between the two clusters.",
        list(patterns.values())
    )

    # Split view layout
    col1, col2 = st.columns([0.3, 0.7])
    with col1:  # description
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
    with col2:  # plot
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


import pandas as pd
import streamlit as st

from constants import individual_variations
from plot_cluster_interval import plot_cluster_confidence_intervals_for_df, daily_ts_graph_description_text

flatline_stats_df = pd.read_csv('data/flatline-stats-results.csv', header=[0, 1, 2], index_col=0)
different_days_stats_df = pd.read_csv('data/different_days-stats-results.csv', header=[0, 1, 2], index_col=0)


def display_individual_variations():
    st.header(individual_variations)
    st.markdown("Each person is unique. Insulin requirements vary "
                "hugely between people and over time for the same person. No one size fits all.")

    st.subheader("Study demographics vs national averages")
    st.write("The study participants had better-than-average glucose control and higher technology adoption rates compared to the general UK Type 1 Diabetes population.")
    col4, col5, col6, col7 = st.columns(4)
    col4.metric("Avg. A1C in mmol/mol", 46, delta=-22, delta_color="inverse",
                help="This is a measure that reflects average blood glucose levels. Non "
                     "diabetic A1C < 42. The average A1C in the UK is 67-69. NICE"
                     " recommends A1C < 48, which 30% of adults in the UK achieve. "
                     "70% of adults in the UK have an A1C > 58, 40% have an A1C > 75.")
    col5.metric("Using an insulin pump since", 2006, delta=2015,
                help="Pumps became more widely available on the NHS around 2015/16.")
    col6.metric("Using a CGM since", 2014, delta=2022,
                help="CGM is a continuous glucose monitor and it became more widely available"
                     " on the NHS in 2022.")
    col7.metric("Using an AID since", 2017, delta=2022,
                help="AID is an automated insulin delivery system. Such systems became more"
                     "widely available on the NHS in 2022.")

    st.divider()

    st.subheader("Variation between people")
    st.write(
        "Even within a demographically similar group, we found substantial individual variations in glucose regulation patterns.")
    col1, col2 = st.columns(2)
    with col1:  # plot
        st.markdown("<p style='text-align: center; font-weight: bold; margin: 0;'>A person with almost flat lines</p>",
                    unsafe_allow_html=True)
        fig = plot_cluster_confidence_intervals_for_df(flatline_stats_df, fix_y=6)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown(
            "<p style='text-align: center; font-weight: bold; margin: 0;'>A person with more variation between the days</p>",
            unsafe_allow_html=True)
        fig = plot_cluster_confidence_intervals_for_df(different_days_stats_df, fix_y=6)
        st.plotly_chart(fig, use_container_width=True)

    st.caption(daily_ts_graph_description_text)

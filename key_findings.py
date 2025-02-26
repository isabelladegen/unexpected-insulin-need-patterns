import random

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from constants import expected_colour, unexpected_colour

format_with_arrow = lambda number: f"{'↑' if number > 0 else '↓' if number < 0 else ''} {abs(number):.2f} τ"

granger_causality_df = pd.read_csv("data/granger_causality.csv", index_col=0)
predict_glucose_columns = {
    'Insulin': 'IOB->IG',
    'Carbs': 'COB->IG',
}
pattern_associations_df = pd.read_csv("data/demographic_associations.csv")
# key = display name, value = dataframe column names
demographic_factors = {
    "Age": "Age",
    "Duration of T1D": "Duration of T1D",
    "A1C": "A1C",
    "Avg. Carbs": "Avg. Carbs",
    "Avg. Insulin": "Avg. Insulin",
    "Avg. Basal Insulin": "Avg. Basal Insulin",
    "Pumping since": "Pumping since",
    "CGM since": "CGM since",
    "AID since": "AID since"
}
pattern_frequency_df = pd.read_csv("data/pattern_frequency.csv", index_col=0)
# key = display name, value = dataframe timeframe
temporal_units = {
    "Hours of the day": "Hours of the day",
    "Same hour across days": "Clusters",
    "Days of the week": "Days of the week",
    "Months of the year": "Months of the year",
}
patterns_by_number = {
    1: ':one:   More **insulin** :syringe:...',
    2: ':two:   Higher **blood glucose** :drop_of_blood: ...',
    3: ':three:   Eating more **carbs** :green_apple:...',
}
# key = display name, value = dataframe pattern number
selectable_patterns = {
    patterns_by_number[1]: 1,
    patterns_by_number[2]: 2,
    patterns_by_number[3]: 3
}

expected_reasons = {
    ':one:   More **insulin** :syringe:...': " was needed for more **carbs**.",
    ':two:   Higher **blood glucose** :drop_of_blood: ...': " was due to more **carbs**.",
    ':three:   Eating more **carbs** :green_apple:...': " needed more **insulin**."
}

unexpected_reasons = {
    ':one:   More **insulin** :syringe:...': " was not due to more **carbs**.",
    ':two:   Higher **blood glucose** :drop_of_blood: ...': " was not due to more **carbs**.",
    ':three:   Eating more **carbs** :green_apple:...': " did not need more **insulin**."
}


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
            name=f'{pattern_type} Pattern: ' + ', '.join([str(x) for x in selected_patterns]),
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
            hovertemplate=('%{x:.1f} people')
        ))

    # Update layout
    fig.update_layout(
        xaxis_title='Number of people (total n=29)',
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


def display_explore_predictability():
    lags = {
        '1 hour': 1,
        '2 hours': 2,
        '3 hours': 3,
    }
    derivatives = {
        'Original values': 0,
        'Speed': 1,
        'Acceleration': 2,
        'Change of Acceleration': 3
    }
    variates = list(predict_glucose_columns.keys())
    help_for_col_name = {
        variates[0]: f'Shows for how many people of the 28 we can predict blood glucose from {variates[0]}',
        variates[1]: f'Shows for how many people of the 28 we can predict blood glucose from {variates[1]}',
    }
    with st.expander("Explore for how many people we can predict blood glucose from insulin or carbs"):
        total_people = 28  # we removed the id from the data for privacy
        selected_lag = st.segmented_control(
            "Select how many hours back in time to check for effects:", list(lags.keys()),
            default=list(lags.keys())[0]
        )
        selected_derivative = st.segmented_control(
            "Select aspects of the data to use to predict blood glucose:", list(derivatives.keys()),
            default=list(derivatives.keys())[0]
        )
        if not selected_lag or not selected_derivative:
            st.error("Please select at least one option each")
        else:
            # filter lag
            lags_value = lags[selected_lag]
            g_filtered = granger_causality_df[granger_causality_df["lag"] == lags_value]

            # filter derivative
            derivative_value = derivatives[selected_derivative]
            g_filtered = g_filtered[g_filtered["no_derivatives"] == derivative_value]

            # st.write(g_filtered)


            all_predictable_ids = set()
            one_cluster_only_ids = {}
            both_clusters_ids = {}
            # calculate ids
            for i, col_name in enumerate(variates):
                rel_name = predict_glucose_columns[col_name]
                # DataFrame showing whether each ID-cluster combination has any True values
                has_true_by_id_cluster = g_filtered.groupby(['id', 'Cluster'])[rel_name].any().reset_index()
                # Count how many clusters have True for each ID
                trues_per_id = has_true_by_id_cluster[has_true_by_id_cluster[rel_name] == True].groupby(
                    'id').size()

                # keep trac of ids with trues
                ids_with_any_true = trues_per_id.index.tolist()
                all_predictable_ids.update(ids_with_any_true)

                # Filter for IDs that have exactly 1 cluster with True (not both)
                unique_ids_one_cluster_only = trues_per_id[trues_per_id == 1]
                unique_ids_both_clusters = trues_per_id[trues_per_id == 2]
                one_cluster_only_ids[col_name] = unique_ids_one_cluster_only
                both_clusters_ids[col_name] = unique_ids_both_clusters

            with st.container(border=True):
                final_cols = st.columns(2)
                with final_cols[0]:
                    st.metric("Unique people who show predictability from Insulin or Carbs",
                              value=f"{people_string(len(all_predictable_ids))} of 28")
                with final_cols[1]:
                    create_icon_array(indices_group1=all_predictable_ids, indices_group2=[], color_group1="#212121")

            # display clusters
            cols = st.columns(len(variates))
            for i, col_name in enumerate(variates):
                with cols[i]:
                    with st.container(border=True):
                        st.markdown("People for which we can predict glucose from **" + col_name + "**",
                                    help=help_for_col_name[col_name])
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Some days", value=f"{one_cluster_only_ids[col_name].count()}")
                        with col2:
                            st.metric("Most days", value=f"{both_clusters_ids[col_name].count()}")
                        create_icon_array(indices_group1=one_cluster_only_ids[col_name],
                                          indices_group2=both_clusters_ids[col_name])

            st.caption("Note: Granger causality was used to determine forecastability")

def people_string(n: int):
    if n == 0:
        return "No one"
    elif n== 1:
        return str(1) + " person"
    else:
        return str(n) + " people"
def create_icon_array(indices_group1, indices_group2,
                      color_group1="#7CBDDA",
                      color_group2="#0A6C95",
                      inactive_color="#F0F0F0"):
    # SVG person silhouette
    unique_id = random.randint(10, 1000)
    person_svg = """
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 4a4 4 0 1 0 0 8 4 4 0 0 0 0-8zm0 10c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
        </svg>
        """

    # Use unique class names with the unique_id
    html = f"""
        <style>
        .icon-grid-{unique_id} {{
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 8px;
            margin-bottom: 8px;
        }}
        .icon-{unique_id} {{
            text-align: center;
        }}
        .group1-{unique_id} {{
            color: {color_group1};
        }}
        .group2-{unique_id} {{
            color: {color_group2};
        }}
        .inactive-{unique_id} {{
            color: {inactive_color};
        }}
        </style>
        """

    # 4 rows of 7 icons each
    for row in range(4):
        html += f'<div class="icon-grid-{unique_id}">'
        for col in range(7):
            # Calculate position (0-27)
            position = row * 7 + col

            # Convert to 1-based indexing
            index = position + 1

            # Determine which group this index belongs to
            if index in indices_group1:
                icon_class = f"group1-{unique_id}"
            elif index in indices_group2:
                icon_class = f"group2-{unique_id}"
            else:
                icon_class = f"inactive-{unique_id}"

            html += f'<div class="icon-{unique_id} {icon_class}">{person_svg}</div>'
        html += '</div>'

    st.markdown(html, unsafe_allow_html=True)


def display_main_findings():
    # st.header(key_findings)
    st.subheader("1. Discovered unexpected temporal patterns in insulin needs", divider=True)
    st.markdown(
        "Current models cannot fully explain the observed unexpected patterns, highlighting the need for further research into underlying physiological mechanisms.")

    st.subheader("2. Unexpected patterns are common", divider=True)
    st.markdown(
        "Unexpected patterns occur just as frequently as expected ones, suggesting they are a fundamental part of glucose regulation, not anomalies. This challenges conventional glucose regulation models.")
    display_exploration_pattern_frequency()

    st.subheader("3. Unexpected patterns are not associated with demographics", divider=True)
    st.markdown(
        "Unexpected patterns appear across all demographic groups with no strong associations to demographics, emphasising the need for personalised rather than group-based approaches.")
    display_explore_correlations()

    st.subheader("4. Glucose cannot easily be predicted from insulin or carbs",
                 divider=True)
    st.markdown(
        "The causal relationship between insulin, carbohydrates and glucose levels varies widely between individuals and situations. This variability makes reliable glucose prediction difficult without information about what drives these unexpected patterns, highlighting the need to include more causal factors.")
    display_explore_predictability()


def display_explore_correlations():
    with st.expander("Explore associations between patterns and demographics"):
        st.caption(
            "Select from patterns 1-3 to see associations for the selected pattern:")
        selected_pattern = pattern_selector(key="pattern-correlation-select-patterns")
        temporal_unit = st.radio(
            "Select temporal unit:",
            list(temporal_units.keys()),
            index=0,
            horizontal=True,
            key="select_correlation_temporal_unit",
            label_visibility="visible"
        )
        selectable_pattern_keys = list(demographic_factors.keys())
        demographics = st.multiselect(
            "Select demographics:",
            selectable_pattern_keys,
            [selectable_pattern_keys[0], selectable_pattern_keys[1], selectable_pattern_keys[2],
             selectable_pattern_keys[6], selectable_pattern_keys[7], selectable_pattern_keys[8]]
        )
        taus = st.slider("Change association strength τ:", 0.0, 1.0, (0.31, 0.7))
        lower_tau = taus[0]
        upper_tau = taus[1]

        filtered_assoc_df = pattern_associations_df[
            pattern_associations_df['pattern_number'] == selectable_patterns[selected_pattern]]
        filtered_assoc_df = filtered_assoc_df[filtered_assoc_df['timeframe'] == temporal_units[temporal_unit]]
        # this is only 1 row left and per expected and unexpected
        expected_df = filtered_assoc_df[filtered_assoc_df['pattern_type'] == 'Expected'][demographics]
        expected_demographics = [col for col in demographics
                                 if (abs(expected_df[col].values[0]) >= lower_tau) and
                                 (abs(expected_df[col].values[0]) <= upper_tau)]
        expected_df = expected_df[expected_demographics]

        unexpected_df = filtered_assoc_df[filtered_assoc_df['pattern_type'] == 'Unexpected'][demographics]
        unexpected_demographics = [col for col in demographics
                                   if (abs(unexpected_df[col].values[0]) >= lower_tau) and
                                   (abs(unexpected_df[col].values[0]) <= upper_tau)]
        unexpected_df = unexpected_df[unexpected_demographics]

        # Expected
        with st.container(key="expected_patterns_associations"):
            st.markdown("Associations for **expected pattern**: " + display_expected_reason(selected_pattern),
                        help="↑ higher demographic values lead to **more frequent** patterns; ↓ higher demographic value lead to **less frequent** patterns")
            if not expected_demographics:
                st.caption("No associated demographics")
            else:
                cols = create_cols_for_associations(expected_demographics)
                for i, dem in enumerate(expected_demographics):
                    with cols[i]:
                        st.metric(label=demographic_factors[dem], value=format_with_arrow(expected_df[dem].iloc[0]))

        # Unexpected
        with st.container(key="unexpected_patterns_associations"):
            st.markdown("Associations for **unexpected pattern**: " + display_unexpected_reason(selected_pattern),
                        help="↑ higher demographic values lead to **more frequent** patterns; ↓ higher demographic value lead to **less frequent** patterns")
            if not unexpected_demographics:
                st.caption("No associated demographics")
            else:
                cols = create_cols_for_associations(unexpected_demographics)
                for i, dem in enumerate(unexpected_demographics):
                    with cols[i]:
                        st.metric(label=demographic_factors[dem], value=format_with_arrow(unexpected_df[dem].iloc[0]))

        st.caption("Note: Only associations where τ ≥ 0.36 achieved statistical power ≥80%")


def display_expected_reason(selected_pattern):
    reason = expected_reasons[selected_pattern]
    result = selected_pattern.replace("...", "")
    return result + reason


def display_unexpected_reason(selected_pattern):
    reason = unexpected_reasons[selected_pattern]
    result = selected_pattern.replace("...", "")
    return result + reason


def create_cols_for_associations(selected_factors):
    n_factors = len(selected_factors)
    col_width = max(1, min(25, int(100 / n_factors + 1)))
    cols = st.columns([col_width] * n_factors)
    return cols


def display_exploration_pattern_frequency():
    with st.expander("Explore Pattern Frequency"):
        st.caption(
            "Select from patterns 1-3 to see how many of the 29 people had which expected pattern (patterns with known reasons) and unexpected patterns (patterns with unknown reasons):")
        selected_pattern = pattern_selector(key="pattern-frequency-select-patterns")
        show_graph = st.toggle("Show as graph")

        if show_graph:
            # plot
            fig = create_pattern_plot(pattern_frequency_df, [selectable_patterns[selected_pattern]])
            st.plotly_chart(fig, use_container_width=True)
            # else:
            #     st.warning("Please select at least one pattern to display.")
        else:
            # Show numbers
            # Calculate number of people with pattern
            temporal_unit = st.radio(
                "Compare across:",
                list(temporal_units.keys()),
                index=0,
                horizontal=True,
                label_visibility="visible"  # Hides the empty label completely
            )

            filtered_df = pattern_frequency_df[
                pattern_frequency_df['pattern_number'] == selectable_patterns[selected_pattern]]
            filtered_df = filtered_df[filtered_df['timeframe'] == temporal_units[temporal_unit]]
            avg_expected = filtered_df[filtered_df['pattern_type'] == 'Expected']['mean'].iloc[0]
            avg_unexpected = filtered_df[filtered_df['pattern_type'] == 'Unexpected']['mean'].iloc[0]

            # Display key metrics
            st.write("")  # add space
            col1, col2, col3 = st.columns(3)
            col1.metric("Total People", "29")
            col2.metric("People with Expected Patterns", str(avg_expected))
            col3.metric("People with Unexpected Patterns", str(avg_unexpected))


def pattern_selector(key=""):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<p class="pattern-header"><strong>Select Pattern</strong></p>', unsafe_allow_html=True)
        selected_pattern = st.radio(
            "Select Pattern:",
            list(selectable_patterns.keys()),
            index=0,
            key=key,
            horizontal=False,
            label_visibility="collapsed"  # Hides label but keeps it for accessibility
        )
    with col2:
        st.markdown("""
                <div class="expected-col">
                    <p><strong>Expected → known reasons</strong></p>
                    <p>... was needed for more <strong>carbs</strong>.</p>
                    <p>... was due to more <strong>carbs</strong>.</p>
                    <p>... needed more <strong>insulin</strong>.</p>
                </div>
            """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
                <div class="unexpected-col">
                    <p><strong>Unexpected → unknown reasons</strong></p>
                    <p>... was not due to more carbs.</p>
                    <p>... was not due to more carbs.</p>
                    <p>... did not need more insulin.</p>
                </div>
            """, unsafe_allow_html=True)
    return selected_pattern

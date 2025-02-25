import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from constants import expected_colour, unexpected_colour, key_findings

format_with_arrow = lambda number: f"{'↑' if number > 0 else '↓' if number < 0 else ''} {abs(number):.2f} τ"

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
# key = display name, value = dataframe pattern number
selectable_patterns = {
    ':one:   More **insulin** :syringe:...': 1,
    ':two:   Higher **blood glucose** :drop_of_blood: ...': 2,
    ':three:   Eating more **carbs** :green_apple:...': 3
}

expected_reasons = {
    ':one:   More **insulin** :syringe:...': " was needed for more **carbs**.",
    ':two:   Higher **blood glucose** :drop_of_blood: ...': " was due to more **carbs**.",
    ':three:   Eating more **carbs** :green_apple:...': " needed more **insulin**."
}

unexpected_reasons = {
    ':one:   More **insulin** :syringe:...': " was not due to more carbs.",
    ':two:   Higher **blood glucose** :drop_of_blood: ...': " was not due to more carbs.",
    ':three:   Eating more **carbs** :green_apple:...': " did not need more insulin."
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


def display_main_findings():
    st.header(key_findings)
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
            st.markdown("Associations for **expected pattern**: " + display_expected_reason(selected_pattern), help="↑ higher demographic values lead to **more frequent** patterns; ↓ higher demographic value lead to **less frequent** patterns")
            if not expected_demographics:
                st.caption("No associated demographics")
            else:
                cols = create_cols_for_associations(expected_demographics)
                for i, dem in enumerate(expected_demographics):
                    with cols[i]:
                        st.metric(label=demographic_factors[dem], value=format_with_arrow(expected_df[dem].iloc[0]))

        # Unexpected
        with st.container(key="unexpected_patterns_associations"):
            st.markdown("Associations for **unexpected pattern**: " + display_unexpected_reason(selected_pattern), help="↑ higher demographic values lead to **more frequent** patterns; ↓ higher demographic value lead to **less frequent** patterns")
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

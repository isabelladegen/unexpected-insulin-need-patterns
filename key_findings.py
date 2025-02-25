import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from constants import expected_colour, unexpected_colour, key_findings

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
    st.markdown("Unexpected patterns appear across all demographic groups with no strong associations to demographics, emphasising the need for personalised rather than group-based approaches.")
    display_explore_correlations()

    st.subheader("4. Glucose cannot easily be predicted from insulin or carbs",
                 divider=True)
    st.markdown("The causal relationship between insulin, carbohydrates and glucose levels varies widely between individuals and situations. This variability makes reliable glucose prediction difficult without information about what drives these unexpected patterns, highlighting the need to include more causal factors.")


def display_explore_correlations():
    with st.expander("Explore associations between patterns and demographic information"):
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


def display_exploration_pattern_frequency():
    with st.expander("Explore Pattern Frequency"):
        st.caption(
            "Select from patterns 1-3 to see how many of the 29 people had which expected pattern (patterns with known reasons) and unexpected patterns (patterns with unknown reasons):")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('<p class="pattern-header"><strong>Select Pattern</strong></p>', unsafe_allow_html=True)
            selected_pattern = st.radio(
                "Select Pattern:",
                list(selectable_patterns.keys()),
                index=0,
                key="pattern-frequency-select-patterns",
                horizontal=False,
                label_visibility="collapsed"  # Hides label but keeps it for accessibility
            )

        with col2:
            st.markdown("""
                <div class="expected-col">
                    <p><strong>Expected → known reasons</strong></p>
                    <p>... is needed for more <strong>carbs</strong>.</p>
                    <p>... is due to more <strong>carbs</strong>.</p>
                    <p>... needs more <strong>insulin</strong>.</p>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
                <div class="unexpected-col">
                    <p><strong>Unexpected → unknown reasons</strong></p>
                    <p>... is not due more carbs.</p>
                    <p>... is not due more carbs.</p>
                    <p>... does not need more insulin.</p>
                </div>
            """, unsafe_allow_html=True)


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

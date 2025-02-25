from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st

daily_ts_graph_description_text = "The graphs shows daily time series of scaled, hourly mean readings and 95% confidence intervals for " \
                                  "insulin, carbohydrates and blood glucose seperated into two clusters based on euclidian distance."


def select_chart_type():
    col_head, col_radio = st.columns([2, 3])  # Adjust the ratio as needed
    with col_head:
        st.caption('<div style="text-align: center; padding-top: 10px;">Select visualisation type:</div>',
                   unsafe_allow_html=True)
    with col_radio:
        graph_layout = st.radio(
            "Select visualisation type",
            ["Cluster-based", "Variate-based"],
            index=0,
            horizontal=True,
            label_visibility="collapsed"  # Hides the empty label completely
        )
    return graph_layout


def plot_cluster_confidence_intervals_for_df(df, fix_y=0, plot_type="Cluster-based"):
    # Get counts for each cluster from the data
    df = df.round(2)
    if plot_type == "Cluster-based":
        return display_clusters_separately(df, fix_y=fix_y)
    else:
        return display_variates_separately(df, fix_y)


def display_clusters_separately(df, fix_y):
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
        fig.update_yaxes(
            title_text=title,
            range=[0, fix_y] if fix_y > 0 else None,
            row=i,
            col=1)
        fig.update_xaxes(
            title_text="Hour of day (UTC)" if i == 2 else None,
            tickmode='array',
            tickvals=list(range(0, 24, 2)),
            row=i, col=1
        )
    return fig


def display_variates_separately(df, fix_y):
    # Create figure with subplots
    fig = make_subplots(
        rows=3, cols=1,
        vertical_spacing=0.05,
        shared_xaxes=True,
    )
    # Colors matching the matplotlib version
    colors = {
        0: '#75CBD8',
        1: '#B8B943',
    }
    # Names for legend
    cluster_names = {
        0: 'Cluster 1',
        1: 'Cluster 2',
    }
    # Names variates
    metric_names = {
        'iob': 'Insulin',
        'cob': 'Carbohydrates',
        'bg': 'Blood Glucose'
    }
    # Plot for each cluster
    for i, metric_key in enumerate(metric_names.keys(), 1):
        row = i

        for cluster_key, cluster_name in cluster_names.items():
            base_col = f'xtrain {metric_key} mean'
            color = colors[cluster_key]

            # Add confidence interval as a filled area
            x_data = df.index.tolist()
            ci_hi = df[(str(cluster_key), 'ci96_hi', base_col)]
            ci_lo = df[(str(cluster_key), 'ci96_lo', base_col)]

            fig.add_trace(
                go.Scatter(
                    name=f'{cluster_name} CI',
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
                    name=cluster_name,
                    x=x_data,
                    y=df[(str(cluster_key), 'mean', base_col)],
                    mode='lines+markers',
                    line=dict(color=color, width=2),
                    marker=dict(size=6),
                    showlegend=True if i == 1 else False,
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
    for i, metric_name in enumerate(metric_names.values(), 1):
        title = f"{metric_name}"
        fig.update_yaxes(
            title_text=title,
            range=[0, fix_y] if fix_y > 0 else None,
            row=i,
            col=1)
        fig.update_xaxes(
            title_text="Hour of day (UTC)" if i == 3 else None,
            tickmode='array',
            tickvals=list(range(0, 24, 2)),
            row=i, col=1
        )
    return fig

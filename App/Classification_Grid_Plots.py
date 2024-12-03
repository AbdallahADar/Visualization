import numpy as np
import pandas as pd
import plotly.graph_objects as go

def classification_grid_prep(series, color_mapping, position_mapping, order_scenario, label_scenario):

    # Convert to dataframe form
    df = series.rename("Classification").to_frame().reset_index(names = "Scenario")

    # Order based on scenario
    df['Scenario'] = pd.Categorical(df['Scenario'],
                                    categories = ["ews" + (f"_{i}" if i else "") for i in order_scenario], 
                                    ordered=True)

    # Create segment position and color in graph
    df['Color'] = df['Classification'].map(color_mapping)
    df['Position'] = df['Classification'].map(position_mapping)

    # Scenario labels. They follow order of order_scenario
    df["Label"] = label_scenario

    return df


def classification_grid_plot(df, color_mapping, position_mapping, background_color):
    fig = go.Figure()
    
    # Adjust X-values to bring them closer
    x_positions = [0.125, 0.25, 0.375, 0.5]
    
    # Add color bands for each scenario with slight overlap to remove white lines
    overlap = 0.00005
    bar_width = 0.125
    for i, scenario in enumerate(df['Scenario']):
        for color, y in color_mapping.items():
            fig.add_shape(type="rect",
                          x0=x_positions[i] - bar_width/2 - overlap, y0=position_mapping[color] - bar_width,
                          x1=x_positions[i] + bar_width/2 + overlap, y1=position_mapping[color] + bar_width,
                          fillcolor=color_mapping[color],
                          opacity=0.5,
                          layer="below",
                          line_width=0)
    
    # Add a trace for the company's classification
    fig.add_trace(go.Scatter(
        x=x_positions,
        y=df['Position'],
        mode='lines+markers',
        line=dict(color='black', width=2),
        marker=dict(size=14, color=df['Color'], symbol='circle'),
        # text=df['Label'],
        hoverinfo='text'
    ))
    
    # Customize layout for aesthetics
    fig.update_layout(
        autosize = True,
        title="",
        xaxis_title="",
        yaxis_title="",
        yaxis=dict(tickvals=[0.25, 0.5, 0.75, 1.0],
                   ticktext=['', '', '', '']),
        plot_bgcolor=background_color,
        paper_bgcolor=background_color,
        font=dict(size=18),
        showlegend=False,
        xaxis=dict(
            tickmode='array',
            tickvals=x_positions,
            ticktext=df['Label']
        ),
        # height=450,  # Adjust the height to make the plot square-shaped
        # width=450,   # Set width to match height for square shape
        # aspectratio=dict(x=1, y=1),
        margin=dict(l=10, r=10, t=10, b=10)  # Adjust margins
    )

    print(df["Label"])
    return fig
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from itertools import product, combinations
from plotly.subplots import make_subplots

def parallel_category_plot(df, top_n, key = True, backgroundcolor = "white"):

    # Define category orders
    order = ["H", "MH", "ML", "L"]
    
    check = df.nlargest(top_n, 'Names')
    
    fig = go.Figure(go.Parcats(
        dimensions=[
            dict(values=check['SalesB'], label='Sales', categoryorder='array', categoryarray=order),
            dict(values=check['AssetB'], label='Asset', categoryorder='array', categoryarray=order),
            dict(values=check['ShrinkB'], label='Shrink', categoryorder='array', categoryarray=order),
            dict(values=check['BorrowB'], label='Borrow', categoryorder='array', categoryarray=order)
        ],
        labelfont=dict(size=16),  # Adjust the label size here
        line=dict(color=check['Names'], 
                  colorscale="Plasma",
                  colorbar=dict(title='Count', tickvals=[])),
        hoverinfo = "none"
    ))

    if key:
        fig.add_annotation(
            x = 0.5, y = 1.2,
            xref="paper", yref="paper",
            text="H = High | MH = Medium-High | ML = Medium-Low | L = Low",
            showarrow=False,
            align="left",
            font=dict(size=14),
            bordercolor="black",
            borderwidth=1,
            borderpad=4,
            bgcolor="white",
            opacity=0.8
        )
    
    fig.update_layout(
        coloraxis_colorbar=dict(
            x=1.05,                  # Increase the distance between color bar and plot
            title=dict(
                text="Count",       # Title of the color bar
                font=dict(size=16)  # Increase title font size
            ),
            tickfont=dict(size=14)  # Increase tick label font size
        ),
        width=1000,
        height=500,
        margin=dict(l=20, r=10, t=90, b=30),
        plot_bgcolor=backgroundcolor,  
        paper_bgcolor=backgroundcolor,
    )

    return fig


def pairwise_combo_grid(pairwise_dict, combos, key = False, backgroundcolor = "white"):

    # Create subplots with default spacing and without subplot titles
    fig = make_subplots(
        rows=2, cols=3,
        shared_xaxes=False, shared_yaxes=False,
        horizontal_spacing=0.05,  # Adjust as needed for more compact layout
        vertical_spacing=0.1
    )
    
    for combo, (r, c) in zip(combos, [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3)]):
        fig.add_trace(
            go.Heatmap(
                x=pairwise_dict[combo][combo[0]], 
                y=pairwise_dict[combo][combo[1]], 
                z=pairwise_dict[combo]["Names"],
                coloraxis="coloraxis",
                colorscale="Plasma",
                showscale=False,
                hovertemplate=f"{combo[0]}: %{{x}}<br>{combo[1]}: %{{y}}<br>Count: %{{z}}<extra></extra>"
            ),
            row=r, col=c
        )
    
        fig.add_annotation(
            yref="paper",
            x=1.5, y=-0.8,
            text=combo[0],
            showarrow=False,
            row=r,
            col=c
        )
    
        fig.add_annotation(
            yref="paper",
            x=-0.8, y=1.5,
            textangle = -90,
            text=combo[1],
            showarrow=False,
            row=r,
            col=c
        )
    
        # Set x and y labels with consistent ordering and reduced standoff
        fig.update_xaxes(
            categoryorder="array", 
            categoryarray=["H", "MH", "ML", "L"],
            side = "top",
            showgrid=False,
            row=r, col=c
        )
        fig.update_yaxes(
            categoryorder="array", 
            categoryarray=["H", "MH", "ML", "L"], 
            side = "right",
            showgrid=False,
            row=r, col=c
        )

    if key:
        fig.add_annotation(
            x = 0.55, y = 1.15,
            xref="paper", yref="paper",
            text="H = High | MH = Medium-High | ML = Medium-Low | L = Low",
            showarrow=False,
            align="left",
            font=dict(size=12),
            bordercolor="black",
            borderwidth=1,
            borderpad=4,
            bgcolor="white",
            opacity=0.8
        )
    
    # Add a shared color axis and colorbar
    fig.update_layout(coloraxis=dict(colorbar=dict(tickvals=[],title="Count",xpad=30)),
                      width=1000,  # Set the width
                      height=500,  # Set the height
                      margin=dict(l=30, r=0, t=70, b=20),
                      plot_bgcolor=backgroundcolor,
                      paper_bgcolor=backgroundcolor
                     )

    return fig
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt

def bucket_distribution(df, country, size, sector, color_dict, background_color):

    # Define static variables used for plotting
    prob_types = np.array(["Sales", "Asset", "Borrow", "Shrink"], dtype = "object")
    category_types = np.array(["_L", "_ML", "_MH", "_H"], dtype = "object")
    segment_types = ["_cntry_size","_cntry_size_sector","_glb_size", "_glb_size_sector"]
    locations = [0.1, 0.5, 0.9, 1.3]
    subplot_titles = (country + " - " + size, 
                      country + " - " + sector + " - " + size, 
                      "Global - " + size, 
                      "Global - " + sector + " - " + size)

    # Create subplots: a 2x2 matrix
    fig = make_subplots(rows=2, cols=2, vertical_spacing=0.2, horizontal_spacing=0.1,subplot_titles=subplot_titles)

    # Iterate over each subplot position and data category to populate the subplots
    subplot_pos = [(1, 1), (1, 2), (2, 1), (2, 2)]  # (row, col) positions
    for pos, category in zip(subplot_pos, segment_types):

        sums = [df[i+category_types+category].sum() for i in prob_types] # Order matches prob_types. Used to normalize height of full bar
        L = np.divide(df[prob_types + "_L" + category].values, sums)
        ML = np.divide(df[prob_types + "_ML" + category].values, sums)
        MH = np.divide(df[prob_types + "_MH" + category].values, sums)
        H = np.divide(df[prob_types + "_H" + category].values, sums)
        
        # Create a stacked bar plot for the current category and add it to the subplot
        fig.add_trace(go.Bar(x=locations, y=L, marker_color=color_dict["L"], width=0.3), row=pos[0], col=pos[1])
        fig.add_trace(go.Bar(x=locations, y=ML, marker_color=color_dict["ML"], width=0.3), row=pos[0], col=pos[1])
        fig.add_trace(go.Bar(x=locations, y=MH, marker_color=color_dict["MH"], width=0.3), row=pos[0], col=pos[1])
        fig.add_trace(go.Bar(x=locations, y=H, marker_color=color_dict["H"], width=0.3), row=pos[0], col=pos[1])


    fig.update_layout(
        barmode='stack',
        showlegend=False, # Remove legend
        paper_bgcolor=background_color,  # Change as needed
        plot_bgcolor=background_color,  # Change as needed
    )

    # Update axes labels and remove gridlines
    fig.update_xaxes(title = '',
                     tickvals = locations,
                     ticktext = prob_types,
                     showline = False, showgrid = False, zeroline = False,
                    titlefont=dict(size=12))
    fig.update_yaxes(showticklabels=False, showline=False, showgrid=False, zeroline=False)

    # Add matrix outlines via boxes
    fig.update_layout(shapes=[
        go.layout.Shape(
            type="rect",
            xref="paper",
            yref="paper",
            x0=-0.05,
            y0=-0.05,
            x1=0.5,
            y1=1.1,
            line={"width": 1, "color": "black"}),
        go.layout.Shape(
            type="rect",
            xref="paper",
            yref="paper",
            x0=0.5,
            y0=-0.05,
            x1=1.05,
            y1=1.1,
            line={"width": 1, "color": "black"}),
        go.layout.Shape(
            type="rect",
            xref="paper",
            yref="paper",
            x0=-0.05,
            y0=-0.05,
            x1=1.05,
            y1=0.5,
            line={"width": 1, "color": "black"}),
    ])

    # Update final size
    fig.update_layout(
        # width=1000,
        # height=1000,
        margin=dict(l=50, r=50, b=50, t=50),  # Adjust margins as needed
        autosize=True
    )

    # Dynamically adjust subplot titles based on length
    for annotation in fig.layout.annotations:
        title_length = len(annotation.text)
        if title_length > 25:  # If the title exceeds 15 characters
            annotation.font.size = 14  # Decrease font size for long titles
        else:
            annotation.font.size = 16  # Default font size for short titles

    # Adjust the position of subplot titles for proper alignment
    # fig.layout.annotations[0].update(x=0.21, y=1.05, xanchor='center')  # Top-left subplot
    # fig.layout.annotations[1].update(x=0.78, y=1.05, xanchor='center')  # Top-right subplot
    # fig.layout.annotations[2].update(x=0.21, y=0.45, xanchor='center')  # Bottom-left subplot
    # fig.layout.annotations[3].update(x=0.78, y=0.45, xanchor='center')  # Bottom-right subplot

    return fig
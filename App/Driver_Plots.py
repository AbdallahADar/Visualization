import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.colors as mcolors
import itertools
from io import BytesIO
import base64
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

def create_radial_graph(percentiles, color_hex_df, pred, model_type, background_color):

    # First column is perc
    col_names = [i for i in percentiles.columns.tolist() if i!= "perc"]
    
    for i in col_names:
        percentiles = percentiles.merge(color_hex_df.rename(columns = {0 : str(i), 
                                                                       1 : str(i)+"_c"}),
                                        how = "left",
                                        on = i)

    # Prepare data
    num_segments = len(col_names)
    segment_size = 2 * np.pi / num_segments

    # Create circular heatmap
    fig, ax = plt.subplots(figsize = (10, 10), 
                           subplot_kw = dict(polar = True))


    # Create heatmap within each segment
    for i, col in enumerate(col_names):
        theta = np.linspace(i * segment_size, (i + 1) * segment_size, 100)
        r = np.linspace(0, 100, 100)
        T, R = np.meshgrid(theta, r)
        Z = R

        ax.pcolormesh(T, R, Z, 
                      shading = 'auto', 
                      cmap = mcolors.ListedColormap(percentiles[str(col) + "_c"].values))

    # Add lines for each segment
    for i in range(num_segments):
        ax.plot([i * segment_size, i * segment_size], [0, 100], color = 'black', linewidth = 4)

    # Remove grid lines
    ax.grid(False)

    # Remove axis and labels
    ax.set_yticklabels([])
    ax.set_xticklabels([])

    # Remove the default polar spine
    ax.spines['polar'].set_visible(False)

    # Radar plot overlay
    pred = pred[[i + "_" + model_type for i in col_names]] # Reorder based on our data order
    # values = pred.iloc[0].tolist() + [pred.iloc[0].tolist()[0]]
    # angles = np.linspace(0, 2 * np.pi, num_segments, endpoint = False).tolist() + [0]
    angles = np.linspace(0, 2 * np.pi, num_segments, endpoint=False).tolist()
    angles = [angle + segment_size / 2 for angle in angles]  # Center points in the middle of the segments
    angles += angles[:1]
    values = pred.tolist()
    values += values[:1]
    ax.plot(angles, values, color = 'darkblue', linewidth = 2, linestyle = "none")
    ax.scatter(angles, values, color = 'darkblue', s=100)

    # Add column names outside the segments with more space
    label_distance = 110  # Adjust this value to increase/decrease the space between the diagram and the labels
    for i, label in enumerate(col_names):
        angle_rad = i * segment_size + segment_size / 2
        ax.text(angle_rad, label_distance, label, size=18, horizontalalignment="center", verticalalignment='center')

    fig.patch.set_facecolor(background_color)

    # Save the plot to a BytesIO object and encode as base64
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode()

    plt.close(fig)
    return image_base64



def bar_heatmap(df, percentiles, custom_cmap, model_type, background_color):

    # First column is perc
    col_names = [i for i in percentiles.columns.tolist() if i!= "perc"]

    # Prepare data
    num_vars = len(col_names)

    # Create empty subplots
    fig = make_subplots(rows = num_vars, cols = 1, 
                        vertical_spacing = 0.02)

    # Fill subplots
    for n, j in enumerate(col_names):
        
        # Add the heatmap
        fig.add_trace(
            go.Heatmap(z = [percentiles[j]],
                       colorscale = custom_cmap,
                       showscale = False),
            row = n + 1, col = 1)

        # Add the marker for current selection
        fig.add_trace(
            go.Scatter(x = [df[j + "_" + model_type]], y = [0],
                       mode = 'markers',
                       marker = dict(symbol = 'triangle-down', size = 15, color = 'black'),
                       name = f'{j} markers',
                       showlegend = False,
                       cliponaxis = False),
            row = n + 1, col = 1)

        fig.update_xaxes(
            range = [0,100],  # Add dynamic padding
            row = n+1, col = 1,
            automargin = True,  # Automatically adjust margins
            showline = True,  # Display x-axis line
            zeroline = False  # Remove zero line to keep layout clean
        )

        # Update Layout
        fig.update_yaxes(tickmode = 'array',
                         tickvals = [0],  # Position for the pseudo title
                         ticktext = [str(j) + "  "],  # The pseudo title text
                         tickangle = 0,  # Keep the tick (now title) horizontal
                         automargin = True,
                         row = n+1, col = 1,
                         showticklabels = True)

    # Update full layout
    fig.update_xaxes(showticklabels = False)
    fig.update_layout(height = 600,
                      plot_bgcolor = background_color,  # Match the background to the card color
                      paper_bgcolor = background_color,  # Match the paper background as well
                      margin = dict(l=0, r=20, t=0, b=10),
                     )

    return fig
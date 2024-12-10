import numpy as np
import pandas as pd
import plotly.express as px
from utils.constants import METADATA_COLUMNS, TREE_CMAP

## Get Tree Map
def tree_plot(selection_id, selection_category, normalize = True, bg_color = "white"):

    ## Read file
    df = pd.read_csv(f"data/industry_rates/{selection_category}/{selection_id}.csv")
    df[METADATA_COLUMNS["TREE_PARENT"]] = df[METADATA_COLUMNS["TREE_PARENT"]].fillna("")

    if normalize:
        mean_val = df[METADATA_COLUMNS["TREE_COUNT"]].mean()
        std_val = df[METADATA_COLUMNS["TREE_COUNT"]].std()
        df[METADATA_COLUMNS["TREE_COUNT"]] = (df[METADATA_COLUMNS["TREE_COUNT"]] - mean_val)/std_val
        df[METADATA_COLUMNS["TREE_COUNT"]] = df[METADATA_COLUMNS["TREE_COUNT"]] - df[METADATA_COLUMNS["TREE_COUNT"]].min() + 1

    average = df[df[METADATA_COLUMNS["TREE_TYPE"]] == "Overall"][METADATA_COLUMNS["GROWTH_RATE_COLUMN"]].values[0] * 100
    
    fig = px.treemap(
        parents = df[METADATA_COLUMNS["TREE_PARENT"]],
        names = df[METADATA_COLUMNS["TREE_CHILD"]],
        values = df[METADATA_COLUMNS["TREE_COUNT"]],
        color = df[METADATA_COLUMNS["GROWTH_RATE_COLUMN"]]*100,
        color_continuous_scale = TREE_CMAP,
        color_continuous_midpoint = average,
        branchvalues="total"
    )

    fig.update_layout(
        margin=dict(t=30, l=10, r=10, b=10),  # Reduce margins to 10px on all sides
        width=1200,      # Set the width of the figure
        height=600,      # Set the height of the figure
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        coloraxis_colorbar=dict(
        title="Median<br>Growth Rate",  # Set a custom title
        tickvals=[],           # Remove tick labels
        ticks=''               # Remove tick marks
    )
    )

    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Growth Rate: %{color:.2f}%",  # Custom hover text
        textinfo="label",  # Keep text in the boxes
        insidetextfont=dict(size=18),
        marker=dict(pad=dict(t=30, l=5, r=5, b=5))  # Padding for better readability
    )

    return fig
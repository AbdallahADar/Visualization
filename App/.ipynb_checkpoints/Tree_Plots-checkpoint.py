import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

## Get tree map with full country as the parent and sect
def tree_sector_plot(df, average, country_col, count_col, sector_col, rate_col, normalize = True, background_color = "white", show_colorbar = True):

    if normalize:
        mean_value = df[count_col].mean()
        std_value = df[count_col].std()
        df['Standardized Count'] = (df[count_col] - mean_value) / std_value  # Standardize
        # Shift the values to make them all positive (since treemap values can't be negative)
        df['Standardized Count'] = df['Standardized Count'] - df['Standardized Count'].min() + 1

        fig = px.treemap(
        df,
        path = [country_col, sector_col],
        values = "Standardized Count",
        color = rate_col,
        color_continuous_scale = "curl_r",
        color_continuous_midpoint = average
        )

    else:
        fig = px.treemap(
        df,
        path = [country_col, sector_col],
        values = count_col,
        color = rate_col,
        color_continuous_scale = "curl_r",
        color_continuous_midpoint = average
        )
    
    # Manually set color to overall rate
    fig.data[0]["marker"]["colors"][-1] = average
    
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Growth Rate: %{color:.2f}",  # Custom hover text
        textinfo="label",  # Keep text in the boxes
        insidetextfont=dict(size=18),
        marker=dict(pad=dict(t=30, l=5, r=5, b=5))  # Padding for better readability
    )
        
    fig.update_layout(
        margin=dict(t=10, l=10, r=10, b=10),  # Reduce margins to 10px on all sides
        plot_bgcolor=background_color,
        paper_bgcolor=background_color
    )

    # Conditionally show or hide the color bar
    if not show_colorbar:
        fig.update_coloraxes(showscale=False)
    
    return fig

def combined_tree_sector_plot(df_cntry, df_glb, average_cntry, average_glb, country_col, count_col, sector_col, rate_col, normalize = True, background_color = "white"):

    # Plot 1 for country
    fig1 = tree_sector_plot(df_cntry, average_cntry, 
                            country_col, count_col, sector_col, rate_col,
                            normalize = normalize, background_color = background_color)

    # Plot 2 for global
    fig2 = tree_sector_plot(df_glb, average_glb, 
                            country_col, count_col, sector_col, rate_col,
                            normalize = normalize, background_color = background_color, show_colorbar = False)

    # Combine both figures into a single figure with subplots
    fig_combined = make_subplots(rows = 2, cols = 1, 
                                 shared_xaxes = True,
                                 specs=[[{'type': 'domain'}],
                                        [{'type': 'domain'}]],
                                vertical_spacing = 0.05)

    # Add the first treemap to the combined figure
    fig_combined.add_traces(fig1.data, rows=1, cols=1)

    # Add the second treemap to the combined figure
    fig_combined.add_traces(fig2.data, rows=2, cols=1)

    # Set the color axis 
    fig_combined.update_coloraxes(
        colorscale="curl_r",  # Shared colorscale
        colorbar=dict(
            thickness=40,  # Increase color bar width
            len=0.9,  # Increase the length of the color bar
            y=0.5,  # Center the color bar vertically
            yanchor="middle",
            title=dict(
                text="Growth<br>Rate",  # Break the title into two lines
            ),
            tickvals=[],  # Remove ticks
            ticktext=[]   # Remove tick labels
        )
    )

    # Update layout for better spacing
    fig_combined.update_layout(
        margin=dict(t=5, l=5, r=5, b=5),  # Reduce margins
        plot_bgcolor=background_color,
        paper_bgcolor=background_color
    )

    return fig_combined

def color_bar():

    # Define the color scale using curl_r from Plotly's diverging color scales
    colors = px.colors.diverging.curl_r
    
    # Zip the colors with evenly spaced numbers between 0 and 1 to create the color scale
    custom_color_scale = list(zip(np.linspace(0, 1, len(colors)), colors))
    
    # Create a figure with a single-column heatmap to represent the color scale
    fig = go.Figure()
    
    # Use a 2D array for `z`, where each value corresponds to a different color
    fig.add_trace(go.Heatmap(
        z=np.linspace(0, 1, 100).reshape(100, 1),  # A single column with values from 0 to 1
        colorscale=custom_color_scale,  # Use the custom color scale
        showscale=False,  # Hide the default color bar
        hoverinfo='none'  # Disable hover interaction
    ))
    
    # Adjust layout to make the plot look like a vertical color bar and remove margins/whitespace
    fig.update_layout(
        title=dict(
            text="Growth<br>Rate",  # Title text
            y=0.95,  # Position above the plot
            x=0.5,  # Center the title horizontally
            xanchor="center",
            yanchor="top",
            font=dict(size=24, color = "black"),  # Set title font size
        ),
        xaxis=dict(visible=False, showgrid=False, zeroline=False),  # Hide x-axis completely
        yaxis=dict(visible=False, showgrid=False, zeroline=False),  # Hide y-axis completely
        margin=dict(t=80, b=0, l=0, r=0),  # Increased top margin for title
        height=600,  # Set the height for the vertical color bar
        width=100,   # Set the width for the vertical color bar
        autosize=True,  # Disable autosize
        paper_bgcolor='rgba(0,0,0,0)',  # Make background completely transparent
        plot_bgcolor='rgba(0,0,0,0)'   # Make plot area background completely transparent,
    )

    return fig
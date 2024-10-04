import numpy as np
import pandas as pd
import plotly.graph_objects as go


def create_radar_meter(value, background_color):
    
    # Determine the color and the corresponding text category based on the value
    if value >= 75:
        color = "Green"
        category_text = "High"
    elif value >= 50:
        color = "Yellow"
        category_text = "Medium<br>High"
    elif value >= 25:
        color = "Orange"
        category_text = "Medium<br>Low"
    else:
        color = "Red"
        category_text = "Low"
    
    # Adjust font size based on the length of the category text
    if len(category_text) > 6:  # Longer text
        font_size = 20
    else:  # Shorter text
        font_size = 35

    # Create the gauge plot
    fig = go.Figure(go.Indicator(
        mode="gauge",  # Display only the gauge (remove the number from inside)
        value=value,  # This is the raw numeric value used for the gauge
        gauge={
            'axis': {'range': [0, 100], 'tickvals': [], 'visible': False},  # Set the range from 0 to 100
            'bar': {'color': color},  # The color based on the category
            'bgcolor': 'lightgray',
            'steps': [
                {'range': [0, value], 'color': color},  # Fill the gauge based on the value
            ],
        }
    ))

    # Adding the textual category (High, Medium-High, etc.) to the plot
    fig.add_annotation(
        x=0.5,  # Center the text horizontally
        y=0.15,  # Position the text slightly lower within the gauge
        text=category_text,  # The category text
        showarrow=False,  # No arrow needed
        font=dict(size=font_size, color='darkblue'),  # Adjust font size dynamically
        xanchor='center',  # Center the text
        yanchor='bottom',
        align="center"  # Ensure the text is aligned in the center
    )

    # Update layout to manage the plot size and positioning
    fig.update_layout(
        autosize=True,  # Make the plot responsive
        height=200,  # Adjust height to fit within the card
        margin={'l': 10, 'r': 10, 't': 5, 'b': 10},  # Adjust margin to give enough space
        plot_bgcolor=background_color,
        paper_bgcolor=background_color,
    )

    return fig
import numpy as np
import pandas as pd
import plotly.graph_objects as go

def line_plot_data_prep(df, model_type):
    columns_addons = np.array([""] + ["_"+str(i) for i in range(1,6)], dtype = "object")
    return df[model_type + columns_addons[::-1]].values

# Function to create background line plot with filled area
def create_background_line_plot(values):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[i for i in range(len(values))], y=values, mode='lines', fill='tozeroy', line=dict(color='rgba(0, 0, 255, 0.1)')))
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=150,
        #autosize=True
    )
    return fig

# Function to create country silhouette plot
def create_country_silhouette(country = "USA"):
    
    fig = go.Figure(go.Scattergeo(
        locations=[country],
        locationmode='country names',
        mode='markers',
        marker=dict(size=1, color='rgba(0,0,0,0)')
    ))

    fig.update_geos(
        showcountries=True, countrycolor="black",
        showsubunits=False,
        showcoastlines=False,
        showland=False, landcolor="white",
        showocean=False, oceancolor="white",
        showframe=False,
        projection_type='natural earth',
        lataxis_range=[-60, 90],
        lonaxis_range=[-180, 180]
    )

    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        geo=dict(bgcolor= 'rgba(0,0,0,0)')
    )

    return fig
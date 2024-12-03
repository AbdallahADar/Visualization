import pandas as pd
import numpy as np
import textwrap
import plotly.graph_objects as go

def funnel_plot(df, models, top_n = 3, backgroundcolor = "white"):

    df_list = []
    for i in models:
        df_list.append(df.groupby(i+"_Reason")["Names"].count().reset_index().sort_values("Names", ascending=False).head(top_n).rename(columns = {i+"_Reason":"Reason"}).assign(model = i))
    
    df_want = pd.concat(df_list)
    
    # Define increased x-values for each level to make each row wider
    position_widths = [
        2.0,  # Top level width
        1.8,
        1.6,
        1.4,  # Bottom level width
        1.2
    ]
    
    colors_acceptable = [
        '#006466',  # Deep Teal
        '#4D194D',  # Indigo
        '#333333',  # Charcoal
        '#1B3A4B',  # Navy Blue
        '#2C3E50',  # Slate Blue
        '#1A535C'   # Dark Cyan
        ]
    
    font_sizes = [18, 16, 14, 12, 10]

    # Initialize the figure
    fig = go.Figure()
    
    # Add a funnel trace for each category using increased width values by position
    for n,cat in enumerate(models):
        fig.add_trace(
            go.Funnel(
                y = list(range(1, top_n + 1)),
                x = position_widths[:top_n],  # Width increases for more readability
                text = ["<br>".join(textwrap.wrap(i, 16)) for i in df_want.iloc[0+top_n*n:top_n+top_n*n]["Reason"].values],
                textinfo = "text",
                textposition = 'inside',
                marker=dict(color=colors_acceptable[n]),
                textfont=dict(size=font_sizes[:top_n], color='white'),  # Different font size per level
                hovertemplate=[f"{cat} Propensity<br>Count: {str(i)}<extra></extra>" for i in df_want.iloc[0+top_n*n:top_n+top_n*n]['Names'].values]
            )
        )
        
    # Add category labels as annotations above each column
    if len(models) % 2 == 1: # Odd
        add = np.array(range(1, len(models)//2+1))*2
        x_pos = np.sort(np.concatenate([-add, [0], add]))
    else: # Even
        add = np.array(range(1, len(models)//2))*2 + 1
        x_pos = np.sort(np.concatenate([-add, [-1,1], add]))
    
    annotations = [
        dict(x = i, y = 0.45, text = j+"<br>Propensity", showarrow=False, font=dict(size=20, color = colors_acceptable[n]))
             for n,(i,j) in enumerate(zip(x_pos, models))
    ]
    
    fig.update_layout(
        showlegend=False,
        annotations=annotations,
        yaxis_title="",
        xaxis_title="",
        width=1000,
        height=800,
        funnelmode="stack",
        plot_bgcolor=backgroundcolor,  
        paper_bgcolor=backgroundcolor,
        margin=dict(l=0, r=10, t=15, b=10)
    )
    
    # Remove grid, ticks, and labels from x and y axes
    fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False)
    fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False)

    return fig
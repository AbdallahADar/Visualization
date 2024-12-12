import plotly.graph_objects as go

PLACEHOLDER = go.Figure(
    data = go.Scatter(
        x=[1, 2, 3],
        y=[1, 4, 9], 
        mode='markers')
    ).update_layout(title="Placeholder",
                    xaxis_visible=False, 
                    yaxis_visible=False, 
                    template="plotly_white", 
                    margin=dict(l=40, r=40, t=40, b=40)
                   )
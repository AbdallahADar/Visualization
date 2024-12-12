import pandas as pd
import numpy as np
import networkx as nx
import plotly.graph_objects as go
import textwrap

################# NETWORK GRAPHS #################

def create_network_graph1(df, main_company, radius=2, wrap_width=10, background_color = "white"):
    """
    Create a network graph with the main company as the central node and competitors connected to it.
    The input is a dataframe with company names and colors.

    Args:
        df (pd.DataFrame): DataFrame with 'Names' and 'Color' columns.
        main_company (str): Name of the main company.
        radius (float): Radius at which competitors are spaced around the main company.
        wrap_width (int): Number of characters per line for text wrapping inside the bubbles.

    Returns:
        fig (go.Figure): The resulting plotly figure.
    """
    # Create a NetworkX graph
    G = nx.Graph()

    # Add the main company as a node
    G.add_node(main_company)

    # Add competitors as nodes and connect them to the main company
    competitors = df[df['Names'] != main_company]['Names'].tolist()
    for competitor in competitors:
        G.add_node(competitor)
        G.add_edge(main_company, competitor)  # Create an edge from main company to each competitor

    # Use a spring layout to position nodes
    pos = nx.spring_layout(G, seed=42)

    # Extract node positions and edges
    node_x = []
    node_y = []
    for node in G.nodes:
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    edge_x = []
    edge_y = []
    for edge in G.edges:
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)  # None separates the edges
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    # Assign colors from the DataFrame
    color_dict = dict(zip(df['Names'], df['Color']))

    # Wrap the text for the company names
    def wrap_text(text, width):
        return '<br>'.join(textwrap.wrap(text, width=width))

    # Create traces for edges (lines come first to avoid being drawn over the nodes)
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='gray'),
        hoverinfo='none',
        mode='lines')

    # Create traces for nodes
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=[wrap_text(node, wrap_width) for node in G.nodes],  # Wrap text for each node
        textposition='middle center',
        marker=dict(
            showscale=False,
            color=[color_dict[node] for node in G.nodes],  # Use colors from the DataFrame
            size=[150 if node == main_company else 120 for node in G.nodes],  # Larger size for main company
            line_width=2,
            opacity=1,  # Make circles fully opaque to hide lines underneath
        ),
        hoverinfo='text',
        textfont=dict(
            size=[18 if node == main_company else 15 for node in G.nodes],  # Dynamic font size
            color="black"
        )
    )

    # Create the plot
    fig = go.Figure(data=[edge_trace, node_trace])

    # Set axis limits and layout
    fig.update_layout(
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        plot_bgcolor = background_color,  # Match the background to the card color
        paper_bgcolor = background_color,  # Match the paper background as well
        height=800,  # Increased height
        width=800,   # Increased width
        margin=dict(l=10, r=10, t=10, b=10),  # Remove padding to minimize background
    )

    return fig


def get_combo_circle_points(center_x, center_y, radius):

    # Central circle
    central = (center_x, center_y)
    # Top circle
    top = (center_x, center_y + radius)
    # Bottom circle
    bottom = (center_x, center_y - radius)
    # Right circle
    right = (center_x + radius, center_y)
    # Left circle
    left = (center_x - radius, center_y)
    
    ret = {label : (point[0] - radius, point[1] + radius, point[0] + radius, point[1] - radius) 
           for label, point in {"central" : central, "top" : top, "bottom" : bottom, "right" : right, "left" : left}.items()}
    
    return ret

def add_circles(fig, points, colors, name):

    # Top, Bottom, Right, Left circles
    for i in ["top","bottom","right","left"]:
        fig.add_shape(type="circle",
                      xref="x", yref="y",
                      fillcolor = colors[i],
                      x0 = points[i][0], y0 = points[i][1], x1 = points[i][2], y1 = points[i][3],
                      line_color=colors[i],
                      # layer="below"
                     )

    # Center circle
    fig.add_shape(type="circle",
                  xref="x", yref="y",
                  fillcolor = "cornflowerblue",
                  x0 = points["central"][0], y0 = points["central"][1], x1 = points["central"][2], y1 = points["central"][3],
                  line_color = "cornflowerblue",
                  label = dict(text = name)
                  # layer = "below"
                 )

    return fig
    

def create_network_graph2(df, main_company, radius=0.1, wrap_width=10, background_color = "white"):
    """
    Create a network graph with the main company as the central node and competitors connected to it.
    The input is a dataframe with company names and colors.

    Args:
        df (pd.DataFrame): DataFrame with 'Names' and 'Color' columns.
        main_company (str): Name of the main company.
        radius (float): Radius at which competitors are spaced around the main company.
        wrap_width (int): Number of characters per line for text wrapping inside the bubbles.

    Returns:
        fig (go.Figure): The resulting plotly figure.
    """

    # Create a NetworkX graph
    G = nx.Graph()

    # Add the main company as a node
    G.add_node(main_company, color='red')

    # Add competitors as nodes and connect them to the main company
    competitors = df[df['Names'] != main_company]['Names'].tolist()
    for competitor in competitors:
        G.add_node(competitor)
        G.add_edge(main_company, competitor)  # Create an edge from main company to each competitor

    # Use a spring layout to position nodes
    pos = nx.spring_layout(G, seed=42)

    # Extract node positions and edges
    node_x = []
    node_y = []
    for node in G.nodes:
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    edge_x = []
    edge_y = []
    for edge in G.edges:
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)  # None separates the edges
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    # Wrap the text for the company names
    def wrap_text(text, width):
        return '<br>'.join(textwrap.wrap(text, width=width))

    # Create traces for edges (lines come first to avoid being drawn over the nodes)
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='gray'),
        hoverinfo='none',
        mode='lines')

    # Create the plot
    fig = go.Figure(data=[edge_trace])

    # Add Circle patches to create the circle shape
    for cx, cy, c in zip(node_x, node_y, G.nodes):
        fig = add_circles(fig,
                          get_combo_circle_points(cx, cy, radius),
                          {"top" : df[df["Names"] == c]["SalesP_C"].iloc[0], 
                           "bottom" : df[df["Names"] == c]["ShrinkP_C"].iloc[0], 
                           "right" : df[df["Names"] == c]["AssetP_C"].iloc[0], 
                           "left" : df[df["Names"] == c]["BorrowP_C"].iloc[0]},
                         wrap_text(c, wrap_width))

        # Create traces for nodes
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='text',
        text=[wrap_text(node, wrap_width) for node in G.nodes],  # Wrap text for each node
        textposition='middle center',
        hoverinfo='text',
        textfont=dict(
            size=[18 if node == main_company else 15 for node in G.nodes],  # Dynamic font size
            color="black"
        )
    )

    fig.add_trace(node_trace)

    # Set axis limits and layout
    fig.update_layout(
        autosize=True,
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        plot_bgcolor = background_color,  # Match the background to the card color
        paper_bgcolor = background_color,  # Match the paper background as well
        # height=800,  # Increased height
        # width=800,   # Increased width
        margin=dict(l=10, r=10, t=10, b=10),  # Remove padding to minimize background
    )

    return fig

def network_data_prep(df, model_types):

    for i in model_types:
        df[i + "P_C"] = df[i + "P"].apply(lambda x: "#0046BF" if x >= 75 else "#669EFF" if x >= 50 else "#99BFFF" if x >= 25 else "#CCDFFF")

    return df

## Sample data for testing
network_graph1_sample_df = pd.DataFrame({
    'Names': ['Main Company', 'Competitor A', 'Competitor B', 'Competitor C', 'Competitor D', 'Competitor E'],
    'Color': ['blue', 'lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 'lightpink'],
    'SalesP' : [25, 50, 75, 13, 85, 47],
    'AssetP' : [15, 5, 95, 53, 25, 27],
    'ShrinkP' : [75, 40, 5, 63, 35, 27],
    'BorrowP' : [21, 33, 57, 3, 33, 22]
})


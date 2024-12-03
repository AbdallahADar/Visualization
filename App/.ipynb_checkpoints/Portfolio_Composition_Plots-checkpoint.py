import pandas as pd
import numpy as np
from plotly.express.colors import sample_colorscale
from sklearn.preprocessing import minmax_scale
import plotly.graph_objects as go
import plotly.express as px
from itertools import product, combinations

## Create empty pairwise combo tables
possible_labels = ["High", "Medium-High", "Medium-Low", "Low"]
combos = [("SalesB", "AssetB"), ("SalesB", "BorrowB"), ("SalesB", "ShrinkB"),
         ("BorrowB", "AssetB"), ("BorrowB", "ShrinkB"), ("AssetB", "ShrinkB")]
permutations_all = list(product(possible_labels, repeat=2))
pairwise_dict_in = {}
for i,j in combos:
    pairwise_dict_in[(i,j)] = pd.DataFrame(permutations_all, columns = [i, j])

large_to_small_labels = {
    "High":"H",
    "Medium-High":"MH",
    "Medium-Low":"ML",
    "Low":"L"
}

## Create all 4 sized combo tables
all_combinations_label = pd.DataFrame(list(product(possible_labels, possible_labels, possible_labels, possible_labels)),
                                      columns = ["SalesB", "AssetB", "BorrowB", "ShrinkB"])

def combo_data_prep(df, names, model_type_list, scenario_order_risk, segment_names):

    df_temp = df[df["Names"].isin(names)].copy()
    
    for i in model_type_list:
        conditions = [
            (df_temp[i+'P'] >= 75),
            (df_temp[i+'P'] >= 50),
            (df_temp[i+'P'] >= 25)]
        
        choices = ['High', 'Medium-High', 'Medium-Low']
        df_temp[i+"B"] = np.select(conditions, choices, default='Low')
        df_temp[i+"B"] = pd.Categorical(df_temp[i+"B"], ordered = True, categories = ['High', 'Medium-High', 'Medium-Low', 'Low'])

    ## Labels
    out = df_temp.groupby(["SalesB", "AssetB"]+["ews" + (f"_{i}" if i else "") for i in scenario_order_risk])["Names"].count().reset_index().sort_values("Names", ascending = False)
    out["Label"] = out[["ews" + (f"_{i}" if i else "") for i in scenario_order_risk]].apply(lambda row: segment_names[";".join(row)], axis = 1)
    

    df_temp_full = all_combinations_label.merge(df_temp.groupby([i+"B" for i in model_type_list])["Names"].count().reset_index(),
                                                how = "left",
                                                on = [i+"B" for i in model_type_list]).query("Names!=0").dropna(how="any").replace(large_to_small_labels)

    pairwise_dict = pairwise_dict_in.copy()
    for i,j in pairwise_dict:
        replacement_map = {i : large_to_small_labels, j:large_to_small_labels}
        pairwise_dict[(i,j)] = pairwise_dict[(i,j)].merge(df_temp.groupby([i, j])["Names"].count().reset_index(),
                                                          how = "left",
                                                          on = [i,j]).replace(replacement_map).dropna(how="any")
    
    
    return out, df_temp_full, pairwise_dict

def Donut_Plot(df, background_color = "white", top_n = 50):

    cntry_counts = df.groupby("Country")["Names"].count().reset_index().sort_values("Names")
    cntry_counts = cntry_counts[:top_n]

    discrete_colors = sample_colorscale('teal', minmax_scale(cntry_counts["Names"].values))

    fig = go.Figure()

    fig.add_trace(go.Pie(labels=cntry_counts["Country"], 
                         values=cntry_counts["Names"],
                         textinfo='label',
                         marker = dict(colors = discrete_colors),
                         pull = [0.1]*len(cntry_counts),
                         textposition='outside',
                         hoverinfo="label+percent+value"))

    # Use `hole` to create a donut-like pie chart
    fig.update_traces(hole=.4, hoverinfo="label+percent")
    
    fig.update_layout(
        title="",
        showlegend=False,  # Hide legend
        plot_bgcolor=background_color,
        paper_bgcolor=background_color,
        height = 400,
        width = 400,
        margin=dict(l=10, r=10, b=10, t=10),  # Adjust margins as needed
    )

    return fig

def PieChart_Plot(df, background_color = "white"):

    size_counts = df.groupby("Size")["Names"].count().reset_index()

    discrete_colors = sample_colorscale('teal', minmax_scale(size_counts["Names"].values))

    fig = go.Figure()

    fig.add_trace(go.Pie(labels=size_counts["Size"], 
                         values=size_counts["Names"],
                         textinfo='label',
                         marker = dict(colors = discrete_colors),
                         pull = [0.05]*len(size_counts),
                         textposition='inside',
                         hoverinfo="label+percent+value"))

    fig.update_traces(hoverinfo="label+percent")

    fig.update_layout(
        title="",
        showlegend=False,  # Hide legend
        plot_bgcolor=background_color,
        paper_bgcolor=background_color,
        height = 400,
        width = 400,
        margin=dict(l=20, r=20, b=20, t=20),  # Adjust margins as needed
    )

    return fig

def SunBurst_Plot(df, background_color = "white"):

    sector_ndy_counts = df.groupby(["Sector", "Industry"])["Names"].count().reset_index()

    fig = px.sunburst(sector_ndy_counts, path=['Sector', 'Industry'], values='Names',
                      color = "Names",
                      color_continuous_scale = "teal",)

    # Hide legend
    fig.update_coloraxes(showscale=False)

    fig.update_traces(marker=dict(line=dict(color="white", width=1)),  # Adjust width for more separation
                      insidetextorientation='radial')
    
    fig.update_layout(
        title="",
        showlegend=False,  # Hide legend
        plot_bgcolor=background_color,
        paper_bgcolor=background_color,
        height = 400,
        width = 400,
        margin=dict(l=20, r=20, b=20, t=20),  # Adjust margins as needed
    )

    return fig

def BucketDist_Portfolio(df, color_dict, prob_types, background_color = "white"):

    fig = go.Figure()
    locations = [0.1, 1.5, 2.9, 4.3]

    out = []
    for m in prob_types:
        out.append(df.groupby(m)["Names"].sum().reset_index().rename(columns = {m:"category"}).assign(model = m))
    out = pd.concat(out)
    out["model"] = pd.Categorical(out["model"], ordered=True, categories=prob_types)

    ## Add the bars
    fig.add_trace(go.Bar(x=out[out["category"] == "L"].sort_values("model")["Names"],
                         y=locations,
                         marker_color=color_dict["L"], 
                         text = ["Low"]*len(locations),
                         textposition='inside',
                         insidetextanchor='middle',
                         hovertemplate=(
                             "</b> %{y}<br>" + "<b>Model:</b> %{text}<br>" + "<b>Value:</b> %{x}<extra></extra>"),
                         width=1, orientation="h"))
    fig.add_trace(go.Bar(x=out[out["category"] == "ML"].sort_values("model")["Names"],
                         y=locations,
                         marker_color=color_dict["ML"], 
                         text = ["Medium-Low"]*len(locations),
                         textposition='inside',
                         insidetextanchor='middle',
                         hovertemplate=(
                             "</b> %{y}<br>" + "<b>Model:</b> %{text}<br>" + "<b>Value:</b> %{x}<extra></extra>"),
                         width=1, orientation="h"))
    fig.add_trace(go.Bar(x=out[out["category"] == "MH"].sort_values("model")["Names"],
                         y=locations,
                         marker_color=color_dict["MH"], 
                         text = ["Medium-High"]*len(locations),
                         textposition='inside',
                         insidetextanchor='middle',
                         hovertemplate=(
                             "</b> %{y}<br>" + "<b>Model:</b> %{text}<br>" + "<b>Value:</b> %{x}<extra></extra>"),
                         width=1, orientation="h"))
    fig.add_trace(go.Bar(x=out[out["category"] == "H"].sort_values("model")["Names"],
                         y=locations,
                         marker_color=color_dict["H"], 
                         text = ["High"]*len(locations),
                         textposition='inside',
                         insidetextanchor='middle',
                         hovertemplate=(
                             "</b> %{y}<br>" + "<b>Model:</b> %{text}<br>" + "<b>Value:</b> %{x}<extra></extra>"),
                         width=1, orientation="h"))

    # Update axes labels and remove gridlines
    fig.update_xaxes(title = '',
                     tickvals = [],
                     ticktext = [],
                     showline = False, showgrid = False, zeroline = False,
                    titlefont=dict(size=12))
    fig.update_yaxes(tickvals = locations, ticktext=[i+"<br>Propensity" for i in prob_types], 
                     tickfont=dict(size=14),
                     showline=False, 
                     showgrid=False, zeroline=False)

    fig.update_layout(
        barmode='stack',
        showlegend=False, # Remove legend
        paper_bgcolor=background_color,  # Change as needed
        plot_bgcolor=background_color,  # Change as needed
        width=800,
        height=500,
        margin=dict(l=60, r=10, b=10, t=10),  # Adjust margins as needed
    )

    return fig
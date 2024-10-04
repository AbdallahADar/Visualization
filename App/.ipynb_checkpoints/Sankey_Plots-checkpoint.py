import pandas as pd
import numpy as np
import plotly.graph_objects as go
from functools import reduce
from itertools import combinations

def SankeyData_Plotly(df: pd.DataFrame, levels: list, value: str, omission: list = [], label_levels: list = [],cmap: dict = {}, sort: bool = True):
    
    """
    Prepare data for a Sankey diagram in Plotly from a DataFrame.

    Parameters:
    - df (pd.DataFrame): The input data.
    - levels (list): The columns in the DataFrame that define the levels of the Sankey diagram.
    - value (str): The column in the DataFrame that contains the values to be aggregated.
    - omission (list, optional): Values in the levels to be omitted. Defaults to an empty list.
    - label_levels (list, optional): Levels for which labels should be generated. Defaults to an empty list.
    - cmap (dict, optional): A dictionary mapping levels to colors. If empty, default colors will be used. Defaults to an empty dict.
    - sort (bool, optional): Whether to sort the DataFrame based on levels before processing. Defaults to True.

    Returns:
    dict: A dictionary containing the processed data for plotting a Sankey diagram and other lists needed in plotting.
    """
    
    ## Default colors for levels cmap is empty. 12 colors repeated.
    def_colors = ["#3d85c6", "#a64d79", "#6aa84f", "#cc0000", 
                  "#e69138", "#674ea7", "#16537e", "#c90076",
                  "#ffd966", "#bcbcbc", "#8fce00", "#000000"] * (len(levels) // 12 + 1)
    ## Color descriptions in matching order:
    # Steel Blue, Raspberry, Apple Green, Boston University Red,
    # Tiger Orange, Royal Purple, Lapis Blue, Magenta,
    # Banana Yellow, Silver Sand, Electric Lime, Black
    
    if sort:
        df.sort_values(levels, inplace = True)
        
    ## We want to omit based on the omission list
    # Use reduce to combine conditions for all specified columns
    # Condition is a list of bools
    condition = reduce(lambda x, y: x & y, [~df[col].isin(omission) for col in levels])
    
    ## Reshape df to only have unique values for each level
    ## Introduce index that matches the order of the level
    out = (pd.melt(df[condition],
                   value_vars = levels).
           drop_duplicates(['value']).
           reset_index(drop=True).
           reset_index().
           rename(columns = {"index":"source_idx",
                             "value":"source"})
          )

    ## Create value to index mapping
    index_dict = dict(zip(out["source"], out["source_idx"]))
    
    ## Get labels
    labels = out.apply(lambda row: row["source"] if row["variable"] in label_levels else "", axis = 1).to_list()
    
    ## Get x positions for plot
    x = np.linspace(0, 1, len(levels))
    # The starting and end point should not be exactly 0 or 1 but a value very close to it
    # Using boolean indexing instead of integer indexing helps avoid cases when we only have 1 element array
    x[x == 0] = 0.0001
    x[x == 1] = 0.999
    x_map = dict(zip(levels, x))
    x_positions = out["variable"].apply(lambda x: x_map[x]).to_list()
    
    ## Get y positions for plot
    # Function to apply linspace generation for each group
    def apply_linspace(group):
        count = len(group)
        y = np.linspace(0, 1, count)
        y[y == 0] = 0.0001
        y[y == 1] = 0.999
        group['y'] = y  # Direct assignment
        return group
    
    y_positions = out.groupby('variable', group_keys=False).apply(apply_linspace)["y"].to_list()
        
    ## Create color map from the larger color map supplied by user or using default colors
    if len(cmap) > 0:
        # Default to black if not found
        color_map = [cmap.get(i, def_colors[-1]) for i in index_dict.keys()]
    else:
        def_colors_map = dict(zip(levels, def_colors[:len(levels)]))
        color_map = out["variable"].apply(lambda x: def_colors_map[x]).to_list()

    ## Get starting dataframe which does not include the last level
    out = out[out["variable"] != levels[-1]].drop(columns = "variable")

    ## Create columns for target and values
    out["target"] = np.nan
    out["values"] = np.nan

    # For each successive pair in the levels list, we iterate over it and add information
    for source, target in zip(levels, levels[1:]):
        out = out.merge(df[[source, target, value]].groupby([source, target]).sum().reset_index().rename(columns = {source : "source"}),
                       how = "left",
                       on = "source")
        out["target"] = out["target"].combine_first(out[target])
        out["values"] = out["values"].combine_first(out[value])
        out.drop(columns=[target, value], inplace=True)
        
    # Add target idx
    out["target_idx"] = out["target"].apply(lambda x: index_dict.get(x, np.nan))
    
    # When omission list is populated, it means that we want to remove some values for different levels from being displayed
    # However we want their effect/value to be shown in source nodes
    # Other omissions whose effect does not wish to be shown in the plot should be omitted prior to inputting the df into the function
    out = out[(out["source_idx"].notna()) & (out["target_idx"].notna())]
    
    return {"dataframe" : out,
            "source" : out["source_idx"],
            "target" : out["target_idx"],
            "value" : out["values"],
            "label" : labels,
           "cmap" : color_map,
           "x_position" : x_positions,
           "y_position" : y_positions}


def Sankey_plots(df_dict, background_color):

    ## Create plot
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label = df_dict["label"], #Make ews labels empty
            color= df_dict["cmap"],
            x = df_dict["x_position"],
            y = df_dict["y_position"]
        ),
        arrangement="snap",
        link=dict(
            source=df_dict["source"],
            target=df_dict["target"],
            value=df_dict["value"],
            color = "rgba(200,200,200,0.5)"
        ))])

    fig.update_layout(
        autosize = True,
        margin=dict(l=20, r=20, t=10, b=50),
        plot_bgcolor=background_color,
        paper_bgcolor=background_color
        )
    
    return fig
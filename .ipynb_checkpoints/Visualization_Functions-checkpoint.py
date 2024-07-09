# ==========================================================================
# 
#  Author: Abdallah Dar
#  Developed: July 2024
# 
# ==========================================================================



import pandas as pd
import numpy as np
from functools import reduce
from itertools import combinations
from matplotlib_venn import venn2 ,venn3, venn3_unweighted

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
    
    y_positions = out.groupby('variable', group_keys=False).apply(apply_linspace, include_groups=False)["y"].to_list()
        
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


def SankeyPlotly_Example():
    
    ret = '''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.io as pio
pio.renderers.default = 'notebook'
import plotly.graph_objects as go

## Create example data
level1 = "Technology"
times_of_day = ["Morning", "Afternoon", "Evening", "Night"]
cities = ["New York", "Los Angeles", "Chicago", "Houston"]

# Generate the list of dictionaries
rows = []
for time in times_of_day:
    for city in cities:
        row = {
            "Level1": level1,
            "Level2": time,
            "Level3": city,
            "val": np.random.randint(1, 100)  # Generating a random value between 1 and 99
        }
        rows.append(row)

# Convert the list into a dataframe
df = pd.DataFrame(rows)

## Prepare the data
out = SankeyData_Plotly(df = df,
                     levels = ["Level1", "Level2", "Level3"],
                     value = "val",
                     omission = [],
                     label_levels = ["Level1", "Level3"],
                     cmap = {},
                     sort = True)

## Create plot

fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label = out["label"], #Make ews labels empty
        color= out["cmap"],
        x = out["x_position"],
        y = out["y_position"]
    ),
    arrangement="snap",
    link=dict(
        source=out["source"],
        target=out["target"],
        value=out["value"],
        color = "rgba(200,200,200,0.5)"
    ))])
fig.update_layout(title_text="Sankey Diagram from DataFrame", font_size=10)
fig.show(renderer='iframe')
    '''
    
    return ret


def VennData(df: pd.DataFrame, segments: dict[str, str]) -> dict:
    """
    Get the count belonging to different segments of the Venn diagram.

    Parameters:
    - df (DataFrame): Get the counts after performing the filters
    - segments (dict): Dictionary where key-value pairs represent column names and their respective values of interest.
    
    Returns:
    dict with tuples of column names as keys and counts of matching rows as values.
    """
    
    # segments is a dict where the key is the column name and the value is the value of the column we are interested in
    
    out = {
    tuple(sub_tuple[0] for sub_tuple in comb) : # Extract the column names only
    np.sum(reduce(
        lambda x, y: x & y, 
        [df[col].isin([val] if not isinstance(val, (list, set, tuple)) else val) for col, val in comb] + # Inclusion principle
        [~df[col].isin([val] if not isinstance(val, (list, set, tuple)) else val) for col, val in segments.items() if col not in dict(comb).keys()] #Exclusion principle
    )) # Filter to get count for segments
    for size in range(1, len(segments) + 1) # Different combination sizes
    for comb in combinations(segments.items(), size) # Get the combination of size l
    }
    
    return out


def Venn2D_Example(seed = 123):
    
    ret = f"np.random.seed({seed})"
    
    ret += '''   

## Define example dataframe
sectors = ['Technology', 'Healthcare', 'Finance', 'Consumer Goods', 'Energy']
years = np.arange(2000, 2024)  # From year 2000 to 2023
num_rows = np.random.randint(100, 2000)  # Random number of rows

# Generate random data
deciles = np.random.randint(1, 11, size=num_rows)  # Random deciles from 1 to 10
categories = np.random.choice(sectors, size=num_rows)  # Random sector for each row
random_years = np.random.choice(years, size=num_rows)  # Random year for each row

# Create the DataFrame
df = pd.DataFrame({
    'Decile': deciles,
    'Category': categories,
    'Year': random_years
})

## Get the values
segments = {"Decile":[9,10], "Category":["Energy","Technology"]}
out = VennData(df, segments)

plt.figure(figsize = (10, 10))
venn = venn2(subsets = [*out.values()],
            set_labels = (*segments.keys(),), # Labels for the circles
            alpha = 0.7)

# Set colors of segments
venn.get_patch_by_id("10").set_color("green")
venn.get_patch_by_id("01").set_color("blue")
venn.get_patch_by_id("11").set_color("red")

# Label Text inside the segments
venn.get_label_by_id("10").set_text("_".join([*out.keys()][0]) + "\\n" +str([*out.values()][0]))
venn.get_label_by_id("01").set_text("_".join([*out.keys()][1]) + "\\n" +str([*out.values()][1]))
venn.get_label_by_id("11").set_text("_".join([*out.keys()][2]) + "\\n" +str([*out.values()][2]))

## Label customization
for text in venn.subset_labels:
    text.set_fontsize(14) # Text size
    text.set_color("white") # Text color

plt.show()
    '''
    
    return ret


def Venn3D_Example(seed = 123):
    
    ret = f"np.random.seed({seed})"
    
    ret += '''

## Define example dataframe
sectors = ['Technology', 'Healthcare', 'Finance', 'Consumer Goods', 'Energy']
years = np.arange(2000, 2024)  # From year 2000 to 2023
num_rows = np.random.randint(100, 2000)  # Random number of rows

# Generate random data
deciles = np.random.randint(1, 11, size=num_rows)  # Random deciles from 1 to 10
categories = np.random.choice(sectors, size=num_rows)  # Random sector for each row
random_years = np.random.choice(years, size=num_rows)  # Random year for each row

# Create the DataFrame
df = pd.DataFrame({
    'Decile': deciles,
    'Category': categories,
    'Year': random_years
})

## Get the values
segments = {"Decile":[9,10], "Category":["Energy","Technology"], "Year":[2012,2013,2020]}
out = VennData(df, segments)
A, B, C, AB, AC, BC, ABC = [*out.values()]
A_l, B_l, C_l, AB_l, AC_l, BC_l, ABC_l = [*out.keys()]

## Venn diagram input order: A,B,AB,C,AC,BC,ABC
plt.figure(figsize = (10,10))

venn = venn3(subsets = [A,B,AB,C,AC,BC,ABC],
            set_labels = (*segments.keys(),), # Labels for the circles
            alpha = 0.7)

## Set colors of segments
venn.get_patch_by_id("100").set_color("blue") #A
venn.get_patch_by_id("010").set_color("green") #B
venn.get_patch_by_id("110").set_color("red") #AB
venn.get_patch_by_id("001").set_color("gray") #C
venn.get_patch_by_id("101").set_color("pink") #AC
venn.get_patch_by_id("011").set_color("purple") #BC
venn.get_patch_by_id("111").set_color("orange") #ABC

# Label Text inside the segments
venn.get_label_by_id("100").set_text("_".join(A_l)+ "\\n" +str(A))
venn.get_label_by_id("010").set_text("_".join(B_l)+ "\\n" +str(B))
venn.get_label_by_id("110").set_text("_".join(AB_l)+ "\\n" +str(AB))
venn.get_label_by_id("001").set_text("_".join(C_l)+ "\\n" +str(C))
venn.get_label_by_id("101").set_text("_".join(AC_l)+ "\\n" +str(AC))
venn.get_label_by_id("011").set_text("_".join(BC_l)+ "\\n" +str(BC))
venn.get_label_by_id("111").set_text("_".join(ABC_l)+ "\\n" +str(ABC))

for text in venn.subset_labels:
    text.set_fontsize(15)
    text.set_color("white")

plt.show()
    '''
    
    return ret


def ChoroPleth_USA_PlotlyPX(seed = 123):
    
    ret = f"np.random.seed({seed})"
    
    ret += '''
# List of U.S. states
states = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

# Assuming an arbitrary value for demonstration; this could be replaced with actual data
values = np.random.randint(1, 100, size=len(states))  # Generates random integers between 1 and 100

# Creating the pandas DataFrame
df = pd.DataFrame({
    'States': states,
    'Value': values
})

## Create custom continuous color scale
custom_color_scale = [
    [0,"#5bd75b"],
    [0.33,"#ffd634"],
    [0.66,"#ff8000"],
    [1,"#ff6666"]
]

fig = px.choropleth(locations = df["States"],
                    locationmode = "USA-states",
                    color = df["Value"],
                    scope="usa",
                    color_continuous_scale = custom_color_scale,
                    # color_continuous_scale = 'Reds' # Use built in color scale
                    # color_discrete_map={1:'#5bd75b', 2:'#FFD030', 3:'#ff8000', 4:'#ff6666'}, # If discrete map is to be used
                    # range_color=(0, 100) # Explicitly set color bar limits to have same scale for multiple graphs
                   )

## Add state names
fig.add_scattergeo(
    locations = df['States'],
    locationmode = "USA-states", 
    text = df['States'],
    mode = 'text',
)

## Additional details for plot
fig.update_layout(
    title_text = 'Title',
    # Text updates
    font=dict(
        family = "Courier New, monospace",
        size = 10,  # Set the font size here
        color = "Black"
    ),
    geo = dict(showlakes = False), # Do not show lakes on the plot
    coloraxis_colorbar_title_text = 'Bar', # Name of color bar
    coloraxis_showscale = True, # Toggle to display color bar
    # coloraxis_colorbar_tickvals = [] # Hide ticks in the color bar
)

fig.update_coloraxes(colorbar_showticklabels = False) #Alternate way to hide ticks in color bar

fig.show(renderer='iframe')
'''
    return ret


def ChoroPleth_USA_PlotlyGO(seed = 123):
    
    ret = f"np.random.seed({seed})"
    
    ret += '''
# List of U.S. states
states = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

# Assuming an arbitrary value for demonstration; this could be replaced with actual data
values = np.random.randint(1, 100, size=len(states))  # Generates random integers between 1 and 100

# Creating the pandas DataFrame
df = pd.DataFrame({
    'States': states,
    'Value': values
})

## Create custom continuous color scale
custom_color_scale = [
    [0,"#5bd75b"],
    [0.33,"#ffd634"],
    [0.66,"#ff8000"],
    [1,"#ff6666"]
]

fig = go.Figure(data = 
                go.Choropleth(
                    locations = df['States'],
                    z = df['Value'],
                    locationmode = 'USA-states',
                    colorscale = custom_color_scale,
                    # continuous_scale = 'Reds' # Use built in color scale
                    colorbar_title = "Bar", # Set color bar title
                    colorbar_showticklabels = False, # Hide ticks in the color bar
                    # Set color bar limits to have same scale for multiple graphs
                    zmin = 0,
                    zmax = 100
))

## Add state names
fig.add_scattergeo(
    locations = df['States'],
    locationmode = "USA-states", 
    text = df['States'],
    mode = 'text',
)

## Additional details for plot
fig.update_layout(
    title_text = 'Title',
    geo_scope = "usa", # Limit map to USA
    # Text updates
    font=dict(
        family = "Courier New, monospace",
        size = 10,  # Set the font size here
        color = "Black"
    ),
    geo = dict(showlakes = False), # Do not show lakes on the plot
    coloraxis_showscale = False, # Toggle to display color bar
)

fig.show(renderer='iframe')
'''
    return ret
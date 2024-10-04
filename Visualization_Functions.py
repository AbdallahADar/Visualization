# ==========================================================================
# 
#  Author: Abdallah Dar
#  Created: July 2024
#  Updated: October 2024
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

np.random.seed(123)

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


def ChoroPleth_USA_PlotlyPX_Example(seed = 123):
    
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


def ChoroPleth_USA_PlotlyGO_Example(seed = 123):
    
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

def JointDensityPlotKDE_Seaborn_Example():
    
    ret = '''
import pandas as pd
import random
import seaborn as sns
import matplotlib.pyplot as plt

# Sample dataframe
data = {
    "Assets": [random.randint(10000, 1000000) for _ in range(100)],
    "Sales": [random.randint(5000, 500000) for _ in range(100)]
}
df = pd.DataFrame(data)

# Plotting the joint distribution
plt.figure(figsize=(12, 10))  # Set the figure size
sns.set(style="whitegrid", palette="muted")  # Set the style and color palette for the plot

# Creating the joint plot
joint_plot = sns.jointplot(
    data=df, 
    x="Assets",  # Data for the x-axis
    y="Sales",  # Data for the y-axis
    kind="kde",  # Kind of plot, 'kde' for kernel density estimate
    fill=True,  # Fill the area under the KDE curves
    color="blue",  # Set the color of the plot
    height=10,  # Set the height of the plot
    space=0,  # Space between the joint plot and the marginal plots
    ratio=8  # Ratio of the size of the joint plots to the marginal plot
)

# Adding a title and labels
joint_plot.set_axis_labels('Assets', 'Sales', fontsize=14)  # Set axis labels with font size
plt.suptitle('Joint Density Plot of Assets and Sales', fontsize=18, y=1.03)  # Set the title with font size and adjust the y position
plt.subplots_adjust(top=0.95)  # Adjust the top margin to make room for the title

# Enhancing the aesthetics
sns.despine(trim=True)  # Remove the top and right spines (axes lines) for a cleaner look

# Display the plot
plt.show()  # Show the plot
    '''

    return ret

def RadialHeatMap_Radar_Matplotlib_Example():

    ret = '''
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as mcolors

# Generate sample data
np.random.seed(42)

percentiles = pd.DataFrame(
    {"perc": range(0, 101),
     "q1": np.random.rand(101),
     "q2": np.random.rand(101),
     "q3": np.random.rand(101),
     "q4": np.random.rand(101),
     "q5": np.random.rand(101),
     "q6": np.random.rand(101),
     "q7": np.random.rand(101)})

color_hex_101 = ["#A50026", "#AA0426", "#AF0926", "#B40E26", "#B91326", "#BE1826", "#C31C26", "#C82126", "#CD2626", "#D22B26", "#D73027", "#D93629",
                 "#DC3C2C", "#DF422F", "#E24832", "#E54E34", "#E85437", "#EB5A3A", "#EE603D", "#F16640", "#F46D43", "#F47345", "#F57949", "#F6804C",
                 "#F7864E", "#F88D51", "#F99355", "#FA9A58", "#FBA15A", "#FCA75D", "#FDAD60", "#FDB365", "#FDB869", "#FDBC6D", "#FDC271", "#FDC775",
                 "#FDCB7A", "#FDD17E", "#FDD582", "#FDDB86", "#FEE08B", "#FEE390", "#FEE695", "#FEE99A", "#FEEC9F", "#FEEFA4", "#FEF2AA", "#FEF5AF",
                 "#FEF8B4", "#FEFBB9", "#FFFFBF", "#FBFDB9", "#F7FBB4", "#F3FAAF", "#EFF8AA", "#ECF7A4", "#E8F59F", "#E4F39A", "#E0F295", "#DCF090",
                 "#D9EF8B", "#D3EC87", "#CEEA84", "#C9E881", "#C4E67D", "#BFE47A", "#BAE177", "#B5DF73", "#B0DD70", "#ABDB6D", "#A6D96A", "#9FD669",
                 "#99D368", "#92D067", "#8CCD67", "#86CB66", "#7FC865", "#79C565", "#72C264", "#6CBF63", "#66BD63", "#5EB961", "#56B55F", "#4FB15D",
                 "#47AE5B", "#40AA59", "#38A657", "#30A355", "#299F53", "#219B51", "#1A9850", "#17934D", "#148E4A", "#128948", "#0F8445", "#0C7F43",
                 "#0A7B41", "#07763E", "#05713C", "#026C39", "#006837"]

for i in percentiles.columns[1:]:
    percentiles = percentiles.merge(percentiles[[i]].sort_values(by=i).assign(**{str(i) + "_c": color_hex_101}),
                                    how="left",
                                    on=i)

# Prepare data
num_vars = len(percentiles)
num_segments = 7
segment_size = 2 * np.pi / num_segments

# Create circular heatmap
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

for i, col in enumerate(percentiles.columns[1:8]):
    theta = np.linspace(i * segment_size, (i + 1) * segment_size, 100)
    r = np.linspace(0, 100, 100)
    T, R = np.meshgrid(theta, r)
    Z = R

    ax.pcolormesh(T, R, Z,
                  shading='auto',
                  cmap=mcolors.ListedColormap(percentiles[str(col) + "_c"].values))

# Add lines for each segment
for i in range(num_segments):
    ax.plot([i * segment_size, i * segment_size], [0, 100], color='black', linewidth=4)

# Remove grid lines
ax.grid(False)

# Remove axis and labels
ax.set_yticklabels([])
ax.set_xticklabels([])

# Remove the default polar spine
ax.spines['polar'].set_visible(False)

# If you want to display outside borders
# ax.spines['polar'].set_visible(True)
# ax.spines['polar'].set_linewidth(4)

# Generate sample pred data
pred = pd.DataFrame(
    {"q1": [51],
     "q2": [62],
     "q3": [70],
     "q4": [89],
     "q5": [19],
     "q6": [8],
     "q7": [34]})

# Radar plot
labels = pred.columns
num_vars = len(labels)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles = [angle + segment_size / 2 for angle in angles]  # Center points in the middle of the segments
angles += angles[:1]

values = pred.iloc[0].tolist()
values += values[:1]

ax.plot(angles, values, color='darkblue', linewidth=2, linestyle="none")
ax.scatter(angles, values, color='darkblue', s=100)  # Adjust 's' for larger markers

# Add column names outside the segments with more space
label_distance = 110  # Adjust this value to increase/decrease the space between the diagram and the labels
for i, label in enumerate(labels):
    angle_rad = i * segment_size + segment_size / 2
    ax.text(angle_rad, label_distance, label, size=18, horizontalalignment="center", verticalalignment='center')

# plt.title('Circular Heatmap with Radar Overlay', fontsize=16, fontweight='bold', pad=20)
plt.show()
    '''

    return ret

def BarHeatMap_Radar_Plotly_Example():

    ret = '''
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.io as pio
pio.renderers.default = 'iframe'
import plotly.offline as pyo
pyo.init_notebook_mode(connected=True)
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Generate sample data
np.random.seed(42)

percentiles = pd.DataFrame(
    {"perc": range(0, 101),
     "q1": np.random.rand(101),
     "q2": np.random.rand(101),
     "q3": np.random.rand(101),
     "q4": np.random.rand(101),
     "q5": np.random.rand(101),
     "q6": np.random.rand(101),
     "q7": np.random.rand(101)})

pred = pd.DataFrame(
    {"q1": [51],
     "q2": [62],
     "q3": [70],
     "q4": [89],
     "q5": [19],
     "q6": [8],
     "q7": [34]})

color_hex_101 = ["#A50026", "#AA0426", "#AF0926", "#B40E26", "#B91326", "#BE1826", "#C31C26", "#C82126", "#CD2626", "#D22B26", "#D73027", "#D93629",
                 "#DC3C2C", "#DF422F", "#E24832", "#E54E34", "#E85437", "#EB5A3A", "#EE603D", "#F16640", "#F46D43", "#F47345", "#F57949", "#F6804C",
                 "#F7864E", "#F88D51", "#F99355", "#FA9A58", "#FBA15A", "#FCA75D", "#FDAD60", "#FDB365", "#FDB869", "#FDBC6D", "#FDC271", "#FDC775",
                 "#FDCB7A", "#FDD17E", "#FDD582", "#FDDB86", "#FEE08B", "#FEE390", "#FEE695", "#FEE99A", "#FEEC9F", "#FEEFA4", "#FEF2AA", "#FEF5AF",
                 "#FEF8B4", "#FEFBB9", "#FFFFBF", "#FBFDB9", "#F7FBB4", "#F3FAAF", "#EFF8AA", "#ECF7A4", "#E8F59F", "#E4F39A", "#E0F295", "#DCF090",
                 "#D9EF8B", "#D3EC87", "#CEEA84", "#C9E881", "#C4E67D", "#BFE47A", "#BAE177", "#B5DF73", "#B0DD70", "#ABDB6D", "#A6D96A", "#9FD669",
                 "#99D368", "#92D067", "#8CCD67", "#86CB66", "#7FC865", "#79C565", "#72C264", "#6CBF63", "#66BD63", "#5EB961", "#56B55F", "#4FB15D",
                 "#47AE5B", "#40AA59", "#38A657", "#30A355", "#299F53", "#219B51", "#1A9850", "#17934D", "#148E4A", "#128948", "#0F8445", "#0C7F43",
                 "#0A7B41", "#07763E", "#05713C", "#026C39", "#006837"]
custom_color_map_101 = [[i,j] for i,j in zip(np.linspace(0,1,len(color_hex_101)),color_hex_101)]

num_vars = 7
fig = make_subplots(rows=num_vars, cols=1, vertical_spacing = 0.02)

for n,j in enumerate(percentiles.columns[1:]):
    
    fig.add_trace(
            go.Heatmap(z=[percentiles[j]],
                       colorscale=custom_color_map_101,
                       showscale=False),
            row=n+1, col=1)

    fig.add_trace(
            go.Scatter(x=pred[j], y=[0],
                       mode='markers',
                       marker=dict(symbol='triangle-down', size=15, color='black'),
                       name=f'{j} markers',
                      showlegend=False),
            row=n+1, col=1)
    
    fig.update_yaxes(tickmode='array',
                             tickvals=[0],  # Position for the pseudo title
                             ticktext=[str(j) + "  "],  # The pseudo title text
                             tickangle=0,  # Keep the tick (now title) horizontal
                             automargin=True,
                             row=n+1, col=1,
                             showticklabels=True)


fig.update_xaxes(showticklabels=False)

fig.update_layout(height=600)
# Save image
# fig.write_image("driver_bars_"+i+".png")

## Just display the last one to check it ran as expected
fig.show(renderer='iframe')
    '''

    return ret


def PlotZoomIn_Matplotlib_Example():

    ret = '''
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

# Create example data
x = np.arange(-100,100)
y = np.arange(-100,100)

# Change y values to add groove in the graph for easy distinction
y[95] += 40
y[100] += 20
y[105] -= 40

# Create base plot
ax.plot(x,y)

# Define inset axes
# [x0, y0, width, height]: Lower-left corner of inset Axes, and its width and height. In terms of percentage of the overall graph so values from 0 to 1.
axin = ax.inset_axes([0.7,0.1, 0.2,0.4])

# Recreate plot with axin
axin.plot(x,y)

# Focus on region of interest
axin.set_xlim(-10,10)
axin.set_ylim(-50,50)

# Remove labels and ticks for inset axes
axin.set_xticks([])
axin.set_yticks([])
axin.set_xticklabels([])
axin.set_yticklabels([])

# Embed axis
ax.indicate_inset_zoom(axin)

plt.show()
    '''

    return ret

def Flexible_SubPlots_Mosaic_Matplotlib_Example():

    ret = '''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Create example dataframe
df = pd.DataFrame({
    "x": np.arange(100)/100,
    "y": np.arange(100),
    "z": np.arange(100)**0.5,
    "a": np.arange(100)**2,
    "b": [0]*15 + [1]*10 + [2]*30 + [3]*40 + [4]*5,
    "c": np.random.randn(100)
})

# Create mosaic plot scheme
mosaic_scheme = \'''
ABC
ADD
EEE
\'''

# Create subplot using mosaic scheme
fig, ax = plt.subplot_mosaic(mosaic_scheme)

# Customize the individual plots
background_color = "#f0f8ff"  # Light blue background color similar to Seaborn

# Set a light blue background color and add gridlines
for key in ax.keys():
    ax[key].set_facecolor(background_color)
    ax[key].grid(True, linestyle='-', color='gray', alpha=0.5) # Major gridlines
    # Add minor gridlines
    ax[key].minorticks_on()
    ax[key].grid(which='minor', linestyle='-', linewidth='0.5', color='gray', alpha=0.5) # Minor gridlines


# Plot A: Line plot
ax["A"].plot(df["x"], df["y"], color='blue', linewidth=2)
ax["A"].set_title("Linear Growth", fontsize=12)
ax["A"].set_xlabel("X-axis", fontsize=10)
ax["A"].set_ylabel("Y-axis", fontsize=10)

# Plot B: Scatter plot
ax["B"].scatter(df["x"], df["z"], color='green', marker='o', alpha=0.7)
ax["B"].set_title("Square Root Growth", fontsize=12)
ax["B"].set_xlabel("X-axis", fontsize=10)
ax["B"].set_ylabel("Z-axis", fontsize=10)

# Plot C: Scatter plot
ax["C"].scatter(df["x"], df["a"], color='purple', marker='+', alpha=0.7)
ax["C"].set_title("Quadratic Growth", fontsize=12)
ax["C"].set_xlabel("X-axis", fontsize=10)
ax["C"].set_ylabel("A-axis", fontsize=10)

# Plot D: Bar plot
ax["D"].bar(df["b"].unique(), df["b"].value_counts().values, color='orange', edgecolor='black')
ax["D"].set_title("Category Distribution", fontsize=12)
ax["D"].set_xlabel("Categories", fontsize=10)
ax["D"].set_ylabel("Counts", fontsize=10)

# Plot E: Histogram
ax["E"].hist(df["c"], bins=20, color='red', edgecolor='black', alpha=0.7)
ax["E"].set_title("Random Data Distribution", fontsize=12)
ax["E"].set_xlabel("Values", fontsize=10)
ax["E"].set_ylabel("Frequency", fontsize=10)

# Adjust layout
plt.tight_layout()

# Display full figure
plt.show()
    '''

    return ret


def SimplePlots_Altair_Example():

    ret = '''
## Create charts using Altair
# Allows for layered charts with subplots involved

import altair as alt
from vega_datasets import data
import numpy as np
import pandas as pd

# Get example data
source = data.cars()

# Scatter plot
# alt.Chart() is for the data used in the plot
# .mark_point() is the plot type which is a scatter plot in this case
# .encode() is for specifying the variables
# :Q means the variables is quantitative and :N means it is nominal
points = alt.Chart(source).mark_point().encode(
    x='Horsepower:Q',
    y='Miles_per_Gallon:Q',
    color='Origin:N'
)

# Line plot
# .transform_loess() applies Loess to the point data where x and y were specified
# .mark_line() indicates that the plot is a line plot
# the x and y variables do not need to be encoded since they carry over from points
lines = points.transform_loess(
    'Horsepower', 'Miles_per_Gallon'
).mark_line()

# Want to add data from another table?
# Create a separate plot and we layer them together in the end
# New data for the additional line
new_data = pd.DataFrame({
    'x': np.arange(25)*10,
    'y': np.linspace(5, 45, 25)
})

# Create a line chart for the new data
new_line = alt.Chart(new_data).mark_line(color='red').encode(
    x='x:Q',
    y='y:Q'
)

# Layer the scatter plot, LOESS line, and the new line together
# Instead of doing points + lines + new_line we can also use alt.layer(points, lines, new_line)
layered_chart = (points + lines + new_line).properties(
    title="Scatter Plot with LOESS Line and Additional Line"
)

# Simply call the named chart variable to display it

## We want to add a separate plot that is in the same row.
# .transform_density() is to get the density plot
# .mark_area(orient) is used to define the orientation
distribution_plot = alt.Chart(source).transform_density(
    'Miles_per_Gallon',
    as_=['Miles_per_Gallon', 'density']
).mark_area(orient='vertical').encode(
    y='Miles_per_Gallon:Q',
    x='density:Q'
).properties(
    width=200,
    height=300
)

# Concatenate the distribution plot to the layered plot
# Alternatively we couldve used this to get the same row subplots: alt.hconcat(layered_chart,distribution_plot)
top_row = (layered_chart | distribution_plot).resolve_scale(
    color='independent'
)

## We want to add a separate plot that is in the next row
# Create a histogram
# .mark_bar() is for histogram
aggregated_data = source.groupby('Origin')["Horsepower"].mean().reset_index()
histogram = alt.Chart(aggregated_data).mark_bar(color = "purple").encode(
    x=alt.X('Origin:N', title='Country Code'),
    y=alt.Y('Horsepower:Q', title='Mean Population')
).properties(
    width=700,
    height=200
)

# Concatenate the top row with the histogram in the second row
# Alternatively we couldve used this to get the different row subplots: alt.vconcat(top_row,histogram)
final_chart = top_row & histogram

# If you wish to save the chart
# final_chart.save('plot.png')

final_chart.show()
    '''

    return ret


def ClassificationGrid_Plotly():

    ret = '''
import plotly.graph_objects as go
import pandas as pd

# Example data for a single company
data = {
    'Scenario': ['S1', 'S2', 'S3', 'S4'],
    'Classification': ['Green', 'Yellow', 'Orange', 'Red']
}

# Create a DataFrame
df = pd.DataFrame(data)

# Define the color mapping and position mapping
color_mapping = {'Red': '#FF4136', 'Orange': '#FF851B', 'Yellow': '#FFDC00', 'Green': '#2ECC40'}
position_mapping = {'Red': 0.25, 'Orange': 0.5, 'Yellow': 0.75, 'Green': 1.0}

df['Color'] = df['Classification'].map(color_mapping)
df['Position'] = df['Classification'].map(position_mapping)

# Create the parallel coordinate chart
fig = go.Figure()

# Adjust X-values to bring them closer
x_positions = [0.125, 0.25, 0.375, 0.5]

# Add color bands for each scenario with slight overlap to remove white lines
overlap = 0.00005
bar_width = 0.125
for i, scenario in enumerate(df['Scenario']):
    for color, y in color_mapping.items():
        fig.add_shape(type="rect",
                      x0=x_positions[i] - bar_width/2 - overlap, y0=position_mapping[color] - bar_width,
                      x1=x_positions[i] + bar_width/2 + overlap, y1=position_mapping[color] + bar_width,
                      fillcolor=color_mapping[color],
                      opacity=0.5,
                      layer="below",
                      line_width=0)

# Add a trace for the company's classification
fig.add_trace(go.Scatter(
    x=x_positions,
    y=df['Position'],
    mode='lines+markers',
    line=dict(color='black', width=2),
    marker=dict(size=14, color=df['Color'], symbol='circle'),
    text=df['Classification'],
    hoverinfo='text'
))

# Customize layout for aesthetics
fig.update_layout(
    title="Company Classification",
    xaxis_title="",
    yaxis_title="",
    yaxis=dict(tickvals=[0.25, 0.5, 0.75, 1.0],
               ticktext=['', '', '', '']),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(size=14),
    showlegend=False,
    xaxis=dict(
        tickmode='array',
        tickvals=x_positions,
        ticktext=df['Scenario']
    ),
    height=500,  # Adjust the height to make the plot square-shaped
    width=500,   # Set width to match height for square shape
    margin=dict(l=40, r=40, t=40, b=40)  # Adjust margins
)

# Show plot
fig.show()
    '''

    return ret


def ClassificationBar_Plotly():

    ret = '''
import plotly.graph_objects as go
import pandas as pd

# Example data for a single company
data = {
    'Scenario': ['S1', 'S2', 'S3', 'S4'],
    'Classification': ['Green', 'Yellow', 'Orange', 'Red']
}

# Create a DataFrame
df = pd.DataFrame(data)

# Define the color mapping
color_mapping = {'Red': '#FF4136', 'Orange': '#FF851B', 'Yellow': '#FFDC00', 'Green': '#2ECC40'}
df['Color'] = df['Classification'].map(color_mapping)

# Adjust X-values to bring the boxes closer together
x_positions = [0.125, 0.25, 0.375, 0.5]
bar_width = 0.125

# Create the simplified horizontal bar plot
fig = go.Figure()

# Add a larger arrowhead next to the S4 box leading to the final label
fig.add_annotation(
    ax=x_positions[-1] + bar_width * 0.5,  # Start point near the S4 box
    ay=0.5,
    axref="x",
    ayref="y",
    x=x_positions[-1] + bar_width * 1.5,  # End point further right, towards the label
    y=0.5,
    xref="x",
    yref="y",
    showarrow=True,
    arrowhead=2,
    arrowsize=5,  # Increase the size of the arrow
    arrowwidth=4,  # Increase the width of the arrow
    arrowcolor="black"
)

# Add color bars for each scenario, placing them next to each other
for i, scenario in enumerate(df['Scenario']):
    fig.add_shape(type="rect",
                  x0=x_positions[i] - bar_width/2, y0=0.44,  # Adjusted y0 for slightly taller rectangles
                  x1=x_positions[i] + bar_width/2, y1=0.56,  # Adjusted y1 for slightly taller rectangles
                  fillcolor=df['Color'][i],
                  line=dict(color=df['Color'][i]),
                  layer="above")

    # Add the tick label as text inside the rectangle with shadow effect
    fig.add_annotation(
        text=scenario,
        x=x_positions[i],
        y=0.5,  # Center vertically inside the rectangle
        showarrow=False,
        font=dict(size=14, color="black", family="Arial Black"),  # Bold and slightly larger text
        align="center",
        yshift=0,  # Adjust yshift to fine-tune vertical alignment
        xshift=0,  # Centered horizontally
        opacity=0.9,
        # Adding a subtle text shadow effect
        font_family='Arial black',
        font_color='black'
    )

# Center the final label inside the arrowhead
final_classification = "Volatile"  # Example final label based on the scenarios
fig.add_annotation(
    text=final_classification,
    x=x_positions[-1] + bar_width * 0.85,  # Center it inside the arrowhead
    y=0.5,  # Center it vertically
    showarrow=False,
    font=dict(size=16, color="white", family="Arial Black"),
    align="center"
)

# Customize layout for aesthetics
fig.update_layout(
    title="Company Classification Across Economic Scenarios",
    xaxis_title="",
    yaxis_title="",
    yaxis=dict(showticklabels=False, range=[0.4, 0.6]),  # Squash Y-axis into a single line
    xaxis=dict(
        tickmode='array',
        tickvals=x_positions,
        ticktext=[''] * len(x_positions),  # Remove default tick labels
        range=[0, max(x_positions) + 0.8]  # Extend the range to make room for the final label
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(size=14),
    showlegend=False,
    height=200,  # Adjust the height for a more compact look
    margin=dict(l=50, r=50, t=50, b=50)  # Adjust margins
)

# Show plot
fig.show()
    '''

    return ret
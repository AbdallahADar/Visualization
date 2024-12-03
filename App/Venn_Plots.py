import matplotlib.pyplot as plt
from matplotlib_venn import venn3
from matplotlib.gridspec import GridSpec
from io import BytesIO
import base64
import pandas as pd
import numpy as np

def venn3_plot(labels, colors, background_color):
    
    # Define subset sizes
    subset_sizes = [1, 1, 0.3, 1, 0.3, 0.3, 0.15]  # Specify the subset sizes

    # Create the Venn diagram
    venn = venn3(subsets=subset_sizes, set_labels = labels,alpha = 0.5)

    # Set custom colors for each circle
    venn.get_patch_by_id('100').set_color(colors[0])  # Set color for Set A (left circle)
    venn.get_patch_by_id('010').set_color(colors[1])  # Set color for Set B (right circle)
    venn.get_patch_by_id('001').set_color(colors[2])  # Set color for Set C (top circle)


    # Hide all the labels (numbers inside the Venn diagram)
    for label in venn.set_labels:  # Set labels for the sets (A, B, C)
        label.set_fontsize(16)  # Adjust font size if desired

    for label in venn.subset_labels:  # Hide the subset values
        if label:  # Make sure the label exists
            label.set_text('')  # Remove the text by setting it to an empty string

    # Set the background color of the figure
    fig = plt.gcf()  # Get the current figure
    fig.patch.set_facecolor(background_color)  # Set the background color

    # Extract the middle patch (where A, B, and C overlap)
    middle_patch = venn.get_patch_by_id('111')

    # Get the face color of the middle patch
    middle_color_rgba = middle_patch.get_facecolor()
    middle_color = f"rgba({int(middle_color_rgba[0] * 255)}, {int(middle_color_rgba[1] * 255)}, {int(middle_color_rgba[2] * 255)}, {middle_color_rgba[3]})"

    # Save plot to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    # Encode the BytesIO object to base64
    image_data = base64.b64encode(buf.read()).decode('utf-8')
    
    # Return the base64-encoded image and middle color
    return f"data:image/png;base64,{image_data}", middle_color


def Venn_CommonSegments(df, model_type_list, ordered_scenarios, segment_names):

    for i in model_type_list:
        conditions = [
            (df[i+'P'] >= 75),
            (df[i+'P'] >= 50),
            (df[i+'P'] >= 25)]
        
        choices = ['High', 'Medium-High', 'Medium-Low']
        df[i] = np.select(conditions, choices, default='Low')
        df[i] = pd.Categorical(df[i], ordered = True, categories = ['High', 'Medium-High', 'Medium-Low', 'Low'])
        df.drop(columns = [i+"P"], inplace = True)

    out = df.groupby(model_type_list+["ews" + (f"_{i}" if i else "") for i in ordered_scenarios])["Names"].count().reset_index().sort_values("Names", ascending = False)
    out["Risk\nSegment"] = out[["ews" + (f"_{i}" if i else "") for i in ordered_scenarios]].apply(lambda row: segment_names[";".join(row)], axis = 1)
    
    return out


def Venn_Portfolio_Plot(df, propensity_buckets, scenario_order_risk, segment_names, color_dict, background_color = "white"):

    venn_data = Venn_CommonSegments(df, propensity_buckets, scenario_order_risk, segment_names)

    return create_dice_layout(venn_data[propensity_buckets + ["Risk\nSegment"]], 
                              color_dict, background_color, 
                              len(venn_data.iloc[:3]))

# Function to create each Venn diagram with customized appearance and spacing
def create_spaced_venn(ax, labels_l, colors_l):

    # Define subset sizes
    subset_sizes = [1, 1, 0.3, 1, 0.3, 0.3, 0.15]  # Specify the subset sizes
    
    venn = venn3(subsets=subset_sizes, set_labels=labels_l, ax=ax)
    
    # Set colors and transparency for a clean look
    venn.get_patch_by_id('100').set_color(colors_l[0])
    venn.get_patch_by_id('010').set_color(colors_l[1])
    venn.get_patch_by_id('001').set_color(colors_l[2])
    venn.get_patch_by_id('100').set_alpha(0.5)
    venn.get_patch_by_id('010').set_alpha(0.5)
    venn.get_patch_by_id('001').set_alpha(0.5)

    # Add separation with a white edge
    for subset in ['100', '010', '001']:
        venn.get_patch_by_id(subset).set_edgecolor('white')
        venn.get_patch_by_id(subset).set_linewidth(2)

    # Hide outer labels for a cleaner look
    # for text in venn.set_labels:
    #     text.set_visible(False)
    for text in venn.subset_labels:
        text.set_visible(False)

# Function to create the main layout with optional subplots
def create_dice_layout(df, color_dict, background_color, num_venns=3):
    
    if num_venns == 1:
        
        labels = df.columns.tolist()[:-1] + [df.iloc[0].values[-1]]
        colors = [color_dict.get(i, "#4682B4") for i in df.iloc[0].values]
        fig = plt.figure(figsize=(3, 3))
        gs = GridSpec(1, 1, fig)
        ax = fig.add_subplot(gs[0, 0])  # Center position for a single Venn diagram
        create_spaced_venn(ax, labels, colors)
        
    elif num_venns == 2:

        labels = df.columns.tolist()[:-1] + [df.iloc[0].values[-1]]
        colors = [color_dict.get(i, "#4682B4") for i in df.iloc[0].values]
        fig = plt.figure(figsize=(8, 6))
        gs = GridSpec(2, 2, fig)
        ax1 = fig.add_subplot(gs[0, 0])  # Top-left position
        create_spaced_venn(ax1, labels, colors)

        labels = df.columns.tolist()[:-1] + [df.iloc[1].values[-1]]
        colors = [color_dict.get(i, "#4682B4") for i in df.iloc[1].values]
        ax2 = fig.add_subplot(gs[0, 1])  # Top-right position
        create_spaced_venn(ax2, labels, colors)
        
    elif num_venns == 3:
        
        labels = df.columns.tolist()[:-1] + [df.iloc[0].values[-1]]
        colors = [color_dict.get(i, "#4682B4") for i in df.iloc[0].values]
        fig = plt.figure(figsize=(8, 8))
        gs = GridSpec(3, 3, fig)
        ax1 = fig.add_subplot(gs[0, 0])  # Top-left position
        create_spaced_venn(ax1, labels, colors)

        labels = df.columns.tolist()[:-1] + [df.iloc[1].values[-1]]
        colors = [color_dict.get(i, "#4682B4") for i in df.iloc[1].values]
        ax2 = fig.add_subplot(gs[0, 2])  # Top-right position
        create_spaced_venn(ax2, labels, colors)

        labels = df.columns.tolist()[:-1] + [df.iloc[2].values[-1]]
        colors = [color_dict.get(i, "#4682B4") for i in df.iloc[2].values]
        ax3 = fig.add_subplot(gs[1, 1])  # Center position
        create_spaced_venn(ax3, labels, colors)

    # Set an overall title and remove extra grid space for aesthetics
    plt.suptitle("", fontsize=16)
    plt.subplots_adjust(wspace=0, hspace=0, left=0.05, right=0.95, top=0.9, bottom=0.05)

    # Set the background color of the figure
    fig = plt.gcf()  # Get the current figure
    fig.patch.set_facecolor(background_color)  # Set the background color

    # Save plot to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    # Encode the BytesIO object to base64
    image_data = base64.b64encode(buf.read()).decode('utf-8')
    
    # Return the base64-encoded image and middle color
    return f"data:image/png;base64,{image_data}"

    # return fig
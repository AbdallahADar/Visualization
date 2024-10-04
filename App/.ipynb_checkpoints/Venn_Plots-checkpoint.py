import matplotlib.pyplot as plt
from matplotlib_venn import venn3
from io import BytesIO
import base64

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
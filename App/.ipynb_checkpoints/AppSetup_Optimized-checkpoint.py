import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State, ALL
import dash_daq as daq
import pandas as pd
import json
import numpy as np
import itertools
from itertools import count
from functools import reduce

import Network_Plots as NPlots
import Driver_Plots as DPlots
import DistMatrix_Plots as DMPlots
import Silhouette_Plots as SPlots
import RadarMeter_Plots as RPlots
import Tree_Plots as TPlots
import Sankey_Plots as SKPlots
import Classification_Grid_Plots as CGPlots
import Venn_Plots as VPlots
import Setup
from Setup import BACKGROUND_COLOR, NAME_BUBBLE_STYLE, MODEL_BUTTON_STYLE, COLOR_BUTTON_STYLE, OKAY_BUTTON_STYLE, CARD_STYLE, SECTOR_CONTAINER_STYLE, TILE_STYLE, BOX_STYLE, BOX_STYLE_FULL, HOVER_STYLE, SEGMENT_LABEL, category_colors, custom_color_map_101, color_hex_df, category_colors_labels, model_type_list, sectors_ndy, out_text_style, growth_metadata, color_mapping_risk, position_mapping_risk, scenario_order_risk, scenario_label_risk, segment_names, narrative, cntry_size_dist_metadata, cntry_size_sector_dist_metadata, glb_size_dist_metadata, glb_size_sector_dist_metadata

######### APP COMPONENTS #########

## Toggle switch card
def toggle_switch_card():

    return html.Div(
        id = "toggle-switch-card",
        children = [
        html.Div([
            html.Label('Hot Zones', style={
                'font-weight': 'bold', 
                'font-size': '16px', 
                'text-align': 'center',
                'margin-bottom': '10px'  # Add space between label and switch
            }),  
            daq.ToggleSwitch(
                id='toggle-switch',
                value=False  # Default state is off (hot zones hidden)
            )
        ], style={
            'display': 'flex', 
            'flex-direction': 'column', 
            'align-items': 'center',
            'justify-content': 'center',
            'padding': '20px',
            'border-radius': '10px',
            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)',  # Light shadow for card effect
            'background': 'linear-gradient(135deg, #f5a3a9, #f8c2c6)',  # Light red gradient
            'width': '200px',  # Set card width
        })
    ], style={'display': 'flex', 'justify-content': 'center', 'padding': '5px', 'margin-bottom': '5px', 'margin-top': '5px'})  # Center the card

## Size boxes upper row
def initial_size_boxes_upper():
    return html.Div(
        id='upper-size-box',
        children = [
        html.Div("Large", id="large-box-size", style={'display':'none'}),
        html.Div("Medium", id="medium-box-size", style={'display':'none'}),
        ], style={'display': 'flex', 'justifyContent': 'center','marginTop': '30px',})

## Size boxes upper row
def initial_size_boxes_lower():
    return html.Div([
        html.Div("Small", id="small-box-size", style={'display':'none'}),
        html.Div("Micro", id="micro-box-size", style={'display':'none'}),
        ], style={'display': 'flex', 'justifyContent': 'center'})

## Define print display function
def print_page(selected_sectors, selected_industries, selected_geography, selected_size):
    
    # Initialize empty list to save selections
    selected_items = {}
    selected_items["geography"] = f"Selected Location: {', '.join(list(selected_geography.values())[::-1])}"
    selected_items["sector"] = f"Selected Sectors: {', '.join(selected_sectors)}"
    selected_items["industry"] = f"Selected Industries: {', '.join(selected_industries)}"
    selected_items["size"] = f"Selected Size: {selected_size.capitalize()}"
    
    return html.Div([html.P(item, style = out_text_style[name]) for name, item in selected_items.items()])

## Counter display style
def counter_out_style(count, full):

    percent = (count / full) * 100

    return {
        'width': '120px',
        'height': '120px',
        'borderRadius': '50%',
        'background': f'conic-gradient(#28a745 0% {percent}%, #e0e0e0 {percent}% 100%)',
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'fontSize': '30px',
        'fontWeight': 'bold',
        'color': '#000000',  # Text color changed to black
        'textAlign': 'center',
        'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.2)',
        'margin': '5px auto',
        'transition': 'background 0.4s ease'
    }

## Initial counter display
def initial_counter_display(count):

    return html.Div(id='counter-display',
                    children = f"{count:,}",
                    style = counter_out_style(1, 1)
                    )

## Sector/Industry container
def sector_ndy_containers(selected_sectors = None):

    if selected_sectors is None:
        sector_tiles = [
            html.Div(
                sector["name"],
                id={'type': 'sector-box', 'index': i}, 
                n_clicks=0,
                style={
                    **TILE_STYLE,
                    'backgroundColor': sector["color"]
                    },
                className='sector-box'
                ) for i, sector in enumerate(sectors_ndy)
        ]
    else:
        sector_tiles = [
            html.Div(
                sector["name"],
                id = {'type': 'sector-box', 'index': i},
                n_clicks = 0,
                style = {
                    **TILE_STYLE,
                    'backgroundColor': sector["color"] if sector["name"] not in selected_sectors else '#000000',
                    'color': '#fff' if sector["name"] not in selected_sectors else '#00ff00'
                    },
                className = 'sector-box'
            ) for i, sector in enumerate(sectors_ndy)
        ]
        
    return sector_tiles

## Initial sector industry container
def initial_sector_ndy_grid():

    return html.Div(
        id = 'sector-container',
        children = sector_ndy_containers(),  # Set the initial children to the sector tiles
        style = SECTOR_CONTAINER_STYLE # Set the style. This block is initially hidden
    )

# Get industry and color from selected sectors
def associated_ndy_grid(selected_sectors, selected_industries = None):

    if selected_industries is None:
        industry_counter = count() # From itertools that does a global count as we call on next
        return [
            html.Div(
                industry,
                id = {'type': 'industry-box', 'index': next(industry_counter)},
                n_clicks = 0,
                style = {
                    **TILE_STYLE,
                    'backgroundColor': sector["color"],  # Match industry card to sector color
                    },
                className = 'industry-box',
                **{"data-sector-color": sector["color"]}
                )
            for sector in sectors_ndy if sector["name"] in selected_sectors
            for industry in sector["industries"]
            ]
    else:
        # Update the industry grid with the new selection and color change
        industry_counter = count()  # From itertools that does a global count as we call on next
        return [
            html.Div(
                industry,
                id = {'type': 'industry-box', 'index': next(industry_counter)},
                n_clicks = 0,
                style = {
                    **TILE_STYLE,
                    'backgroundColor': "#000000" if industry in selected_industries else sector["color"],  # Change color if selected
                    'color': "#00ff00" if industry in selected_industries else "#fff",
                },
                className = 'industry-box',
                **{"data-sector-color": sector["color"]}
            )
            for sector in sectors_ndy if sector["name"] in selected_sectors
            for industry in sector["industries"]
        ]
    
## Model button style retriever
def model_mode_button_style(update = True):

    return {**MODEL_BUTTON_STYLE,'backgroundColor': '#007bff', 'color': 'white'} if update else MODEL_BUTTON_STYLE


## Initial Model mode button set up
def initial_model_mode_button(model_mode):
    
    return html.Div([
        html.Button('Sales', id='button-sales', n_clicks=0, style = {'display' : 'none'}),
        html.Button('Asset', id='button-asset', n_clicks=0, style = {'display' : 'none'}),
        html.Button('Borrow', id='button-borrow', n_clicks=0, style = {'display' : 'none'}),
        html.Button('Shrink', id='button-shrink', n_clicks=0, style = {'display' : 'none'})
    ], style={'textAlign': 'center'})

def initial_category_button():

    return html.Div([
        html.Button('', id='btn-green', style={'display' : 'none'}),
        html.Button('', id='btn-yellow', style={'display' : 'none'}),
        html.Button('', id='btn-orange', style={'display' : 'none'}),
        html.Button('', id='btn-red', style={'display' : 'none'}),
    ], style={'textAlign': 'center', 'margin': '10px'})


## Bubble element child retriever
def bubble_element_child(df, selected_status = None):

    # Initial version
    if selected_status == None:
        return [html.Div(children = row["Names"],
                         id = {'type': 'name-bubble', 'index': row["Names"]},
                         style={**NAME_BUBBLE_STYLE,
                                'backgroundColor': category_colors[row['Category']],
                                'textColor': '#000'},
                         className='bubble') for _, row in df.iterrows()]
    else:
        return [html.Div(children=row["Names"],
                         id={'type': 'name-bubble', 'index': row["Names"]},
                         style={**NAME_BUBBLE_STYLE,
                                'backgroundColor': category_colors['Selected'] if selected_status[row['Names']] else category_colors[row['Category']],
                                'color': category_colors[row['Category']] if selected_status[row['Names']] else '#000'},
                         className='bubble'
                         ) for _, row in df.iterrows()]

## Initial setup of bubble name choices with nothing selected. Is called again when we change mode
def initial_bubble_elements():

    return html.Div(id = 'names-container',
                    children = [],
                    style={'display':'none'}, # Hidden initially
                   )


## Get sales and assets with trend lines
def sales_assets_trend_card(company_data, page, model):

    return html.Div([
        html.H3("Company " + model + ("s" if model != "Sales" else ""), 
                style = {'text-align' : 'center', 'font-size': '28px'}),
        dcc.Graph(figure = SPlots.create_background_line_plot(SPlots.line_plot_data_prep(company_data, model)),
                  config={'displayModeBar': False},
                  style={'position': 'absolute', 'top': '20px', 'left': '20px', 'width': 'calc(100% - 40px)', 'height': 'calc(100% - 40px)', 'z-index': '0'},
                  id=f'graph1-{page}'),
        html.P(round(company_data[model]), style={'text-align': 'center', 'font-size': '24px', 'position': 'relative', 'z-index': '1'}),
        ], style = CARD_STYLE)

def location_card(company_data):

    return html.Div([
        html.H3("Country", style={'text-align': 'center', 'position': 'relative', 'z-index': '1', 'font-size': '28px'}),
        html.P(company_data["Country"], style={'text-align': 'center', 'font-size': '24px', 'position': 'relative', 'z-index': '1'}),
        dcc.Graph(figure = SPlots.create_country_silhouette(), #We just want the global silhouette with nothing 
                  config={'displayModeBar': False}, 
                  style={'position': 'absolute', 'top': '0', 'left': '0', 'width': '100%', 'height': '100%', 'z-index': '0', 'opacity': '0.1'}),
        ], style = CARD_STYLE)

def propensity_radar_cards(company_data, model):

    out_map = {"Sales" : "Sales", "Asset" : "Asset", "Shrink" : "Shrinkage", "Borrow" : "Borrowing"}

    return html.Div([
        html.H3([out_map[model], html.Br(), 'Propensity'], 
                style={'text-align': 'center', 
                       'font-size': '28px',}),  # Ensure the text breaks if it's too long}),
        dcc.Graph(figure = RPlots.create_radar_meter(company_data[model + "P"], BACKGROUND_COLOR)),
        ], style={**CARD_STYLE, 'padding': '5px', 'width':'25%'})

def barplot_driver_cards(company_data, model, page):

    out_map = {"Sales" : "Sales Drivers", "Asset" : "Asset Drivers", "Shrink" : "Shrinkage Drivers", "Borrow" : "Borrowing Drivers"}

    return html.Div([
        html.Div([
            html.H3(out_map[model], style={'text-align': 'center', 'font-size': '24px', 'margin-bottom': '10px'}),
            dcc.Graph(figure = DPlots.bar_heatmap(company_data, 
                                                  Setup.percentiles_full[model], 
                                                  custom_color_map_101, 
                                                  model,
                                                  BACKGROUND_COLOR), 
                      id=f'graph-bar-{page}',
                      style={'height': '300px', 'width': '100%', 'padding': '10px'})
            ], style={'width': '100%', 'height': '100%', 'padding': '0px', 'box-sizing': 'border-box'})
        ], style={**CARD_STYLE,
        'width': '65%', 
                  'flex-basis': '65%',
        # 'background-color': BACKGROUND_COLOR, 
        # 'margin': '10px', 
        # 'box-shadow': '2px 2px 5px rgba(0,0,0,0.1)', 
        # 'border-radius': '10px', 
        'box-sizing': 'border-box',
        'max-height': '400px',  # Limit the card height
        'overflow': 'hidden'  # Prevent content overflow
        })

def radialplot_driver_cards(company_data, model):

    out_map = {"Sales" : "Sales Drivers", "Asset" : "Asset Drivers", "Shrink" : "Shrinkage Drivers", "Borrow" : "Borrowing Drivers"}

    return html.Div([
        html.Div([
            html.H3(out_map[model], style={'text-align': 'center', 'font-size': '24px', 'margin-bottom': '10px'}),
            html.Img(src=f"data:image/png;base64,{DPlots.create_radial_graph(Setup.percentiles_full[model],color_hex_df,company_data,model,BACKGROUND_COLOR)}",
                     style={'height': '300px', 'width': '100%', 'object-fit': 'contain'})  # Set a fixed height and ensure image fits properly
            ], style={'width': '100%', 'height': '100%', 'padding': '0px', 'box-sizing': 'border-box', 'background-color': BACKGROUND_COLOR})
        ], style={**CARD_STYLE,
        'width': '35%', 
        'flex-basis': '35%',
        #'background-color': BACKGROUND_COLOR, 
        #'margin': '10px', 
        #'box-shadow': '2px 2px 5px rgba(0,0,0,0.1)', 
        #'border-radius': '10px', 
        'box-sizing': 'border-box',
        'max-height': '400px',  # Limit the card height
        'overflow': 'hidden'  # Prevent content overflow
    })


def competitor_network_cards(df_sub, company_name, page, model_type_list):

    # Get color columns
    df_sub = NPlots.network_data_prep(df_sub, model_type_list)

    return html.Div([
        html.Div([
            html.H3("Competitors", style={'text-align': 'center', 'font-size': '24px', 'margin-bottom': '10px'}),
            dcc.Graph(figure = NPlots.create_network_graph2(df_sub, company_name, background_color = BACKGROUND_COLOR), 
                      id=f'graph-network-{page}',
                      style={'padding': '10px'}),
            ], style={'width': '100%', 'height': '100%', 'padding': '10px', 'box-sizing': 'border-box', 'background-color': BACKGROUND_COLOR})
        ], style={**CARD_STYLE,
        'width': '50%', 
        #'background-color': BACKGROUND_COLOR, 
        #'margin': '10px', 
        #'box-shadow': '2px 2px 5px rgba(0,0,0,0.1)', 
        #'border-radius': '10px', 
        'height' : '550px',
        'max-height': '550px',  # Limit the card height
        'overflow': 'hidden',  # Prevent content overflow
        'display': 'flex'
    })

# Get bucket distribution
def bucket_dist_cards(company_data, page, cntry_size_dist_metadata, cntry_size_sector_dist_metadata, glb_size_dist_metadata, glb_size_sector_dist_metadata):

    full_data = (
        company_data
        .to_frame().T
        .merge(cntry_size_dist_metadata, how = "left", on = ["Country","Size"])
        .merge(cntry_size_sector_dist_metadata, how = "left", on = ["Country","Size","Sector"])
        .merge(glb_size_dist_metadata, how = "left", on = ["Size"])
        .merge(glb_size_sector_dist_metadata, how = "left", on = ["Size","Sector"])
    ).iloc[0]

    return html.Div([
        html.Div([
            dcc.Graph(figure = DMPlots.bucket_distribution(full_data,
                                                           country = full_data["Country"], 
                                                           size = full_data["Size"],
                                                           sector = full_data["Sector"],
                                                           color_dict = category_colors_labels,
                                                           background_color = BACKGROUND_COLOR), 
                      id=f'graph-dist-{page}',
                      style={'width': '100%',  # Ensure the graph takes 100% of its container
                             'height': 'auto',  # Allow the height to adjust automatically
                             'max-width': '100%'  # Prevent the graph from exceeding the container width
                            }),
            ], style={'width': '100%', 'height': '100%', 'padding': '10px', 'box-sizing': 'border-box', 'background-color': BACKGROUND_COLOR,
                     'align-items': 'center', 'display':'flex'})
        ], style={**CARD_STYLE,
        'width': '50%', 
        #'background-color': BACKGROUND_COLOR, 
        #'margin': '10px',
        'align-items': 'center',
        'display': 'flex',
        #'box-shadow': '2px 2px 5px rgba(0,0,0,0.1)', 
        #'border-radius': '10px', 
        'height' : '550px',
        'max-height': '550px',  # Limit the card height
        'overflow': 'hidden'  # Prevent content overflow
    })

# Get the growth rate tree plots
def tree_plot_cards(cntry, country_col, count_col, 
                    sector_col, rate_col, normalize = True, background_color = "white", show_colorbar = True):

    # Prepare data
    cntry_data = growth_metadata[(growth_metadata["Country"] == cntry) & (growth_metadata["Sector"] != "All")].copy()
    cntry_all = growth_metadata[(growth_metadata["Country"] == cntry) & (growth_metadata["Sector"] == "All")].iloc[0]["Growth Rate"]
    
    glb_data = growth_metadata[(growth_metadata["Country"] == "Global") & (growth_metadata["Sector"] != "All")].copy()
    glb_all = growth_metadata[(growth_metadata["Country"] == "Global") & (growth_metadata["Sector"] == "All")].iloc[0]["Growth Rate"]

    return html.Div([
    # Main parent div to align stacked graphs and color bar side by side
    html.Div([
        # Container for the two stacked graphs (on the left side)
        html.Div([
            dcc.Graph(figure=TPlots.tree_sector_plot(cntry_data, cntry_all, 
                                                     country_col, count_col, sector_col, rate_col, 
                                                     normalize=normalize, background_color=background_color, 
                                                     show_colorbar=show_colorbar), 
                      style={'width': '100%', 'height': '300px', 'flex-shrink': '1'}),  # First graph
            
            dcc.Graph(figure=TPlots.tree_sector_plot(glb_data, glb_all, 
                                                     country_col, count_col, sector_col, rate_col, 
                                                     normalize=normalize, background_color=background_color, 
                                                     show_colorbar=show_colorbar), 
                      style={'width': '100%', 'height': '300px', 'flex-shrink': '0'})  # Second graph
        ], style={'display': 'flex', 'flex-direction': 'column', 'width': '92%', 'height': '600px'}),  # Stack graphs vertically
        
        # Container for the color bar (on the right side)
        html.Div([
            dcc.Graph(figure=TPlots.color_bar(), style={'height': '600px', 'width': '100%'})  # Color bar with fixed height and width
        ], style={'width': '8%', 'height': '600px', 
                  'display': 'flex', 'align-items': 'center',
                 })  # Ensure color bar container matches graph height
    ], 
    style={'display': 'flex', 'flex-direction': 'row', 'height': '600px', 'width': '100%',
           'box-sizing': 'border-box',  # Ensure margins are considered within width
          })  # Main container for row layout
], style={**CARD_STYLE, 'height': '600px', 'width': '100%'})  # Ensure that CARD_STYLE does not override height or layout
    

## Sankey plot cards
def sankey_plot_cards(company_data, background_color, model_type_list):

    # Sales
    m = model_type_list[0]
    value = company_data[m + "P"]
    # Determine the color and the corresponding text category based on the value
    if value >= 75:
        color = "Green"
        category_text = "High"
    elif value >= 50:
        color = "Yellow"
        category_text = "Medium<br>High"
    elif value >= 25:
        color = "Orange"
        category_text = "Medium<br>Low"
    else:
        color = "Red"
        category_text = "Low"

    rc = company_data[company_data.index.str.contains('_' + m + "_RC")].rename("RC").to_frame().copy().assign(out = category_text)
    rc = rc.assign(var = rc.index.str.replace("_" + m +"_RC", ""))
    rc = rc.assign(category = rc["var"].map(Setup.ratio_categories)).sort_values("category")

    # Color map
    cmap = reduce(lambda x, y: {**x, **y}, 
              [dict(zip(rc[i], [j] * len(rc))) 
               for i,j in dict(zip(["var", "category", "out"], 
                                   ["#3d85c6", "#a64d79", color])).items()
              ])

    out_sk = SKPlots.SankeyData_Plotly(rc, levels = ["var","category","out"], 
                                       value = "RC", label_levels = ["var","category","out"],
                                       sort = False,
                                       cmap = cmap)

    fig1 = SKPlots.Sankey_plots(out_sk, background_color)

    # Borrow
    m = model_type_list[2]
    value = company_data[m + "P"]
    # Determine the color and the corresponding text category based on the value
    if value >= 75:
        color = "Green"
        category_text = "High"
    elif value >= 50:
        color = "Yellow"
        category_text = "Medium<br>High"
    elif value >= 25:
        color = "Orange"
        category_text = "Medium<br>Low"
    else:
        color = "Red"
        category_text = "Low"

    rc = company_data[company_data.index.str.contains('_' + m + "_RC")].rename("RC").to_frame().copy().assign(out = category_text)
    rc = rc.assign(var = rc.index.str.replace("_" + m +"_RC", ""))
    rc = rc.assign(category = rc["var"].map(Setup.ratio_categories)).sort_values("category")

    # Color map
    cmap = reduce(lambda x, y: {**x, **y}, 
              [dict(zip(rc[i], [j] * len(rc))) 
               for i,j in dict(zip(["var", "category", "out"], 
                                   ["#3d85c6", "#a64d79", color])).items()
              ])

    out_sk = SKPlots.SankeyData_Plotly(rc, levels = ["var","category","out"], 
                                       value = "RC", label_levels = ["var","category","out"],
                                       sort = False,
                                       cmap = cmap)

    fig2 = SKPlots.Sankey_plots(out_sk, background_color)

    
    return html.Div([
        html.Div([
            html.H3("Sales Propensity Contributors", style={'text-align': 'center', 'font-size': '24px', 'margin-bottom': '10px'}),
            dcc.Graph(figure = fig1,
                      style={'width': '100%', 'height': '300px'})
        ], style={**CARD_STYLE, 'padding': '5px', 'height':'370px', 'width':'50%', 'box-sizing': 'border-box','flex-shrink': '1'}),
        html.Div([
            html.H3("Borrowing Propensity Contributors", style={'text-align': 'center', 'font-size': '24px', 'margin-bottom': '10px'}),
            dcc.Graph(figure = fig2,
                      style={'width': '100%', 'height': '300px'})
        ], style={**CARD_STYLE, 'padding': '5px', 'height':'370px', 'width':'50%', 'box-sizing': 'border-box','flex-shrink': '1'}),
    ], style={'display': 'flex', 'width' : '100%', 'height':'390px','box-sizing': 'border-box', 
              'flex-shrink': '1',
              'max-width':'100%'
              # 'padding': '5px'
             })


## Get risk segmentation
def risk_segmentation_cards(company_data, color_mapping, position_mapping, order_scenario, label_scenario, segment_names, background_color):

    # Prep data for plotting
    out = CGPlots.classification_grid_prep(company_data[company_data.index.str.startswith('ews')], 
                                           color_mapping, position_mapping, order_scenario, label_scenario)

    # Get labels
    label = segment_names[";".join(out["Classification"].values)]

    return html.Div([
    # Label
    html.Div([
        html.H3("Early Warning Risk Segment", 
                style={'text-align': 'center', 'font-size': '24px', 'margin-bottom': '10px'}),
        html.Div(
            children=label, 
            style={**SEGMENT_LABEL, 
                   'height': '30%', 
                   'display': 'flex', 
                   'alignItems': 'center', 
                   'justifyContent': 'center'})
    ], style={
        'flex-basis': '35%',  # Label takes up 35% of the container width
        'display': 'flex',    # Flex container for header and label
        'flexDirection': 'column',  # Arrange header and label in a column
        'alignItems': 'center',     # Center align the column content
        'justifyContent': 'center', # Center align vertically
        'height': '100%',           # Make sure it takes the full height
    }),
    
    # Plot
    html.Div([
        dcc.Graph(
            figure=CGPlots.classification_grid_plot(out, color_mapping, position_mapping, background_color).update_layout(
                autosize=True,                       # Make the graph responsive
                margin=dict(l=0, r=0, t=0, b=0),     # Remove any internal margins in the graph
                height=450,                          # Set the graph height explicitly to match the container
                width=450,                           # Set the graph width explicitly to match the container
            ),
            config={'responsive': True}
        )
    ], style={
        'flex-basis': '65%',         # Graph takes up 65% of the container width
        'margin': '0px',             # Remove margins
        'display': 'flex',           # Ensure the graph container uses flexbox
        'alignItems': 'center',      # Center the graph vertically
        'justifyContent': 'center',  # Center the graph horizontally
        'max-height': '90%',         # Ensure it fits within the container's height
        'max-width': '100%',       # Prevent overflow from graph
        'flex-shrink': '1',          # Allow flexibility in shrinking the graph
        'box-sizing': 'border-box'
    })
], style={**CARD_STYLE,
    'display': 'flex',               # Flexbox for side-by-side layout
    'flexDirection': 'row',          # Ensure label and graph are in a row
    'flex-basis': '50%',             # This container takes up 50% of the larger container
    'box-sizing': 'border-box',      # Include padding and border in width/height
    'height': '500px',               # Set a fixed height for the container
          'min-width': '50%',         # Minimum width is 50% of the parent
        'max-width': '50%',         # Maximum width is also 50%
          'flex-shrink': '1',
    'alignItems': 'center',          # Vertically center contents
    'justifyContent': 'space-between' # Ensure even spacing between the elements
})


def venn_narrative_cards(company_data, narrative, background_color, order_scenario, color_mapping, segment_names):

    label = segment_names[";".join(company_data[["ews" + (f"_{i}" if i else "") 
                                   for i in order_scenario]].values)]

    # Determine the color and the corresponding text category based on the value
    value1 = company_data["SalesP"]
    if value1 >= 75:
        color_sales = "Green"
    elif value1 >= 50:
        color_sales = "Yellow"
    elif value1 >= 25:
        color_sales = "Orange"
    else:
        color_sales = "Red"

    value2 = company_data["BorrowP"]
    if value2 >= 75:
        color_borrow = "Green"
    elif value2 >= 50:
        color_borrow = "Yellow"
    elif value2 >= 25:
        color_borrow = "Orange"
    else:
        color_borrow = "Red"

    venn_image, middle_color = VPlots.venn3_plot(["Sales\nPropensity", "Borrowing\nPropensity", label], 
                                                 [color_mapping[color_sales], color_mapping[color_borrow], "#4682B4"],
                                                 background_color)

    return html.Div([
    # Venn diagram image
    html.Div([
        html.Img(src=venn_image, 
                 style={
                     'height': '500px', 
                     'width': '100%',   # Make the image take the full width of its container
                     'padding': '5px', # Padding around the image
                     'objectFit': 'contain'  # Ensure the image scales properly within its container
                 })
    ], style={
        'flex-basis': '60%',           # Venn diagram takes up 50% of the container width
        'display': 'flex',             # Use flexbox to align the image within the container
        'alignItems': 'center',        # Center the image vertically
        'justifyContent': 'center',    # Center the image horizontally
        'height': '100%'               # Ensure the image takes up the full container height
    }),
        
        html.Div([
        html.P(narrative, 
               style={
                   'padding': '10px', 
                   'fontSize': '16px', 
                   'color': '#000'
               }),
    ], style={
        'backgroundColor': middle_color,  # Set the background color to match the middle patch
        'borderRadius': '8px',            # Rounded corners for the box
        'padding': '10px',                # Padding inside the box
        'width': '100%',                  # Ensure the text takes up the full width of its container
        'boxShadow': '2px 2px 12px rgba(0, 0, 0, 0.2)',  # Optional shadow for better effect
        'display': 'flex',                # Use flexbox for better alignment
        'alignItems': 'center',           # Center the text vertically
        'justifyContent': 'center',       # Center the text horizontally
            'min-width': '50%',         # Minimum width is 50% of the parent
        'max-width': '50%',         # Maximum width is also 50%
            'flex-basis': '40%',              # Narrative text takes up 50% of the container width
        'height': '400px'                  # Ensure the text takes up the full container height
    })
], style={**CARD_STYLE,
    'display': 'flex',                    # Flexbox layout to display image and text side by side
    'flexDirection': 'row',               # Ensure Venn diagram and text are side by side
    'height': '500px',                    # Set a fixed height for the container
    'flex-basis': '50%',                  # Ensure this container takes up 50% of the larger container
    'box-sizing': 'border-box',           # Include padding and border in width/height
          'flex-shrink': '1',
    'alignItems': 'center',               # Center items vertically
    'justifyContent': 'space-between'     # Space between the two elements
})


## Create cards
def company_page_generator(company_data, df, page, model_type_list):

    print(df.shape, "Second")

    # Name header. Improve this
    name_header = html.H1(children = company_data["Names"], style = {'text-align': 'center', 'font-size': '36px'})

    # Row 1: Sales and Assets with trend lines
    row1 = html.Div([
        sales_assets_trend_card(company_data, page, "Sales"),
        sales_assets_trend_card(company_data, page, "Asset")
    ], style={'display': 'flex'})

    # Row 2: Firmographic info: Location, Sector, Industry, Size
    row2 = html.Div([
        html.Div([
            html.H3("Sector", style={'text-align': 'center', 'font-size': '28px'}),
            html.P(company_data["Sector"], style={'text-align': 'center', 'font-size': '24px'}),
            ], style = CARD_STYLE),
        html.Div([
            html.H3("Industry", style={'text-align': 'center', 'font-size': '28px'}),
            html.P(company_data["Industry"], style={'text-align': 'center', 'font-size': '24px'}),
            ], style = CARD_STYLE),
        location_card(company_data),
        html.Div([
            html.H3("Company Size", style={'text-align': 'center', 'font-size': '28px'}),
            html.P(company_data["Size"], style={'text-align': 'center', 'font-size': '24px'}),
            ], style = CARD_STYLE),
    ], style={'display': 'flex'})

    # Row 3: Propensity radars
    row3 = html.Div([
        propensity_radar_cards(company_data, "Sales"),
        propensity_radar_cards(company_data, "Asset"),
        propensity_radar_cards(company_data, "Borrow"),
        propensity_radar_cards(company_data, "Shrink"),
        ], style={'display': 'flex','width': '100%'})

    # Row 4 & 5: Driver heatmaps
    row4 = html.Div([
        barplot_driver_cards(company_data, "Sales", page),
        radialplot_driver_cards(company_data, "Asset"),
        ], style={'display': 'flex','width': '100%', })
    row5 = html.Div([
        radialplot_driver_cards(company_data, "Shrink"),
        barplot_driver_cards(company_data, "Borrow", page),
        ], style={'display': 'flex','width': '100%', })
    
    # Row 6: Dist plot and Competitor web
    row6 = html.Div([
        competitor_network_cards(df[df["Names"].isin(company_data["Competitors"].split(";") + [company_data["Names"]])].copy(),
                                 company_data["Names"], page, model_type_list),
        bucket_dist_cards(company_data, page,cntry_size_dist_metadata, cntry_size_sector_dist_metadata, glb_size_dist_metadata, glb_size_sector_dist_metadata)
    ], style={'display': 'flex','width': '100%'})

    # Row 7: Sankey plots
    row7 = html.Div([
        sankey_plot_cards(company_data, BACKGROUND_COLOR, model_type_list)
    ], style = {'display': 'flex','width': '100%'})
    
    # Row 8: Sector tree maps
    row8 = html.Div([
        tree_plot_cards(company_data["Country"], "Country", "Count", 
                    "Sector", "Growth Rate", normalize = True, background_color = BACKGROUND_COLOR, show_colorbar = False)
    ], style = {'display': 'flex','width': '100%'})

    # Row 9: Risk Segments
    row9 = html.Div([
        risk_segmentation_cards(company_data, color_mapping_risk, position_mapping_risk, 
                                scenario_order_risk, scenario_label_risk, segment_names,
                               BACKGROUND_COLOR),
        venn_narrative_cards(company_data, narrative, BACKGROUND_COLOR, 
                             scenario_order_risk, color_mapping_risk, segment_names)
    ], style = {'display': 'flex',            # Flex layout for the two main containers
    'flexDirection': 'row',       # Ensure containers are side by side
    'width': '100%',              # Full width of the parent container
    'max-width': '100%',
    'box-sizing': 'border-box',   # Include padding and border in width calculation
    'alignItems': 'center',       # Center vertically
    'justifyContent': 'space-between'  # Space them evenly
               })

    return html.Div([name_header, row1, row2, row3, row4, row5, row6, row7, row8, row9], style = {'marginTop' : '-30px'})
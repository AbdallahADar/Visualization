import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State, ALL
import dash_daq as daq
import pandas as pd
import json
import numpy as np
import itertools
import matplotlib
matplotlib.use('Agg')  # Use the non-GUI backend

import Network_Plots as NPlots
import Driver_Plots as DPlots
import DistMatrix_Plots as DMPlots
import Silhouette_Plots as SPlots
import RadarMeter_Plots as RPlots
import Geographical_Plots as GPlots
import AppSetup_Optimized as AppSetup
import Setup
from Setup import OKAY_BUTTON_STYLE, SECTOR_CONTAINER_STYLE, COLOR_BUTTON_STYLE, BOX_STYLE_FULL, HOVER_STYLE, PRINT_STYLE, APP_BACKGROUND_COLOR, NEXT_BUTTON_STYLE, model_type_list, category_colors, sectors_ndy
from Setup import glb_rates_metadata, state_rates_metadata, us_counties_metadata, nuts1_rates_metadata, nuts2_rates_metadata, nuts3_rates_metadata

## Load in example table of metadata
df_global = Setup.df_large

## Full df for reference
df_full = df_global[["Names", "SalesP", "AssetP", "BorrowP", "ShrinkP"]].copy()

# Sort dataframe by base category order
model = "Sales" # Base model type

df_global = Setup.model_type_prep(df_global, model)

INITIAL_POOL = len(df_global) # Number of firms initially available

# Initialize selected status
initial_selected = {}

# External stylesheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialize Dash app
app = dash.Dash(__name__)

app.index_string = Setup.index_string

# Layout of the app
app.layout = html.Div(
    id = "app-container",
    children = [
    # Store relevant state variables
    dcc.Store(id = "selected-status", data = initial_selected),  # Store dict with name status
    dcc.Store(id = "selected-companies", data = []),  # Store selected companies
    dcc.Store(id = "model-mode", data = model), # Store model mode
    dcc.Store(id = "page", data = 0),  # Store current page for grid display
    dcc.Store(id = "dataframe-store", data = df_global["Names"].values.tolist()),  # Store dataframe as dict. Now we use global variables to avoid loading and reloading code
    dcc.Store(id = "dataframe-store-full", data = []),  # Store full dataframe as dict for reference. Now we use global variables to avoid loading and reloading code
    dcc.Store(id = 'selected-sectors', data = []),  # Store to keep track of selected sectors
    dcc.Store(id = 'selected-industries', data = []),  # Store to keep track of selected industries
    dcc.Store(id = "selected-geography", data = {}), # Store geographical data
    dcc.Store(id = 'step', data = 'maps1'),  # Track current step: 'sectors' or 'industries'
    dcc.Store(id='counter-store', data=INITIAL_POOL), # Track count of available firms
    dcc.Store(id='selected-size', data="Large"), # Store selected size
    dcc.Store(id='toggle-reference', data=False), # Store selected size

    html.Div(
        [],
        style = {'marginTop': '10px'},    # Add distance from the top of the page
    ),

    # Geographical plots container
    html.Div(
        dcc.Graph(id = 'map', 
                  figure = GPlots.plot_global_country(background_color = APP_BACKGROUND_COLOR).update_layout(clickmode='event+select')),
        style = {'display': 'flex',
                 'justifyContent': 'center',  # Horizontally center the graph
                 'alignItems': 'center', # Vertically center the graph
                'backgroundColor': APP_BACKGROUND_COLOR,
                'margin-bottom':'5px'}  
    ),

    # Sector/NDY Grids
    AppSetup.initial_sector_ndy_grid(),

    # Size page
    AppSetup.initial_size_boxes_upper(),
    AppSetup.initial_size_boxes_lower(),

    # Print page before moving to names
    html.Div(id = 'display-out', style = {'display' : 'none'}),

    # "Okay" Button used for grid selection
    html.Button('Okay', id = 'okay-button', 
                n_clicks = 0, style = OKAY_BUTTON_STYLE), # This block is initially hidden

    # Model mode buttons
    AppSetup.initial_model_mode_button(model), # Hidden in the beginning

    # Category selection/deselection buttons
    AppSetup.initial_category_button(),

    # Display Names
    # id: names-container
    AppSetup.initial_bubble_elements(),

    # Company page display
    html.Div(id='grid-output',
             style={'textAlign': 'center'}),

    # "Okay" Button. This block is initially hidden
    html.Button('Okay', id = 'okay-button2', 
                n_clicks = 0, style = OKAY_BUTTON_STYLE), # This is initially hidden

    # Toggle switch card
    # id = "toggle-switch-card"
    AppSetup.toggle_switch_card(),

    # Counter display
    AppSetup.initial_counter_display(INITIAL_POOL),

    # Next button for switching between companies
    # html.Button('Next', id='next-button', 
    #             style={'marginTop': '20px', 'display': 'none', 'marginLeft': 'auto', 'marginRight': 'auto'}),
    html.Div([
        html.Button("➤", id='next-button', n_clicks=0, style={'display' : 'none'}),
    ], style={'textAlign': 'left', 'marginTop': '20px'}),  # Left-align the button and add top margin



        
], style={
    'backgroundColor': APP_BACKGROUND_COLOR,  # Set the very light grey background color here
})

######### APP UPDATE FUNCTION ###########

@app.callback(
    [
        Output('button-sales', 'style'), # Sales button hidder or shown
        Output('button-asset', 'style'), # Asset button hidder or shown
        Output('button-borrow', 'style'), # Borrow button hidder or shown
        Output('button-shrink', 'style'), # Shrink button hidder or shown 
        Output('model-mode', 'data'), # Track model mode
        Output('selected-status', 'data'), # Track selected status of firms
        Output('names-container', 'children'), # What names to show for selection
        Output('btn-green', 'style'), # Green button hidder or shown
        Output('btn-yellow', 'style'), # Yellow button hidder or shown
        Output('btn-orange', 'style'), # Orange button hidder or shown
        Output('btn-red', 'style'), # Red button hidder or shown
        Output('okay-button2', 'style'), # Okay button 2 hidden or shown
        Output('selected-companies', 'data'), # Track of selected companies
        Output('page', 'data'), # Page number tracker
        Output('grid-output', 'children'), # Company display page
        Output('dataframe-store', 'data'), # Keep track of dataframe
        Output('names-container', 'style'), # Show or hide names container
        Output('map', 'figure'), # What map plot to display
        Output('map', 'style'), # Map plot hidden or shown
        Output('okay-button', 'style'), # Okay button hidden or shown
        Output('selected-sectors', 'data'), # Selected sectors to keep track of
        Output('sector-container', 'children'), # Sector grid layout updated
        Output('sector-container', 'style'), # Overall grid info to hide or show it
        Output('selected-industries', 'data'), # Selected industries to keep track of
        Output('selected-geography', 'data'), # Selected geographies
        Output('step', 'data'), # Track which step: 'plot' or 'sectors' or 'industries'
        Output('counter-display', 'children'), # What counter value to display
        Output('counter-display', 'style'), # The counter style
        Output('counter-store', 'data'), # Counter data
        Output('large-box-size', 'style'), # Large size box style
        Output('medium-box-size', 'style'), # Medium size box style
        Output('small-box-size', 'style'), # Small size box style
        Output('micro-box-size', 'style'), # Micro size box style
        Output('display-out', 'children'), # Selected output display
        Output('display-out', 'style'), # Selected output display style
        Output('selected-size', 'data'), # Selected size
        Output('next-button', 'style'), # Next button style
        Output('toggle-switch-card', 'style'), # Toggle switch card style
        Output('toggle-switch', 'value'),  # Get the current state of the switch
        Output('toggle-reference', 'data'),  # Get the current state of the switch
     ],
    [
        Input('button-sales', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        Input('button-asset', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        Input('button-borrow', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        Input('button-shrink', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        State('model-mode', 'data'),
        State('selected-status', 'data'),
        State('names-container', 'children'),
        Input('btn-green', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        Input('btn-yellow', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        Input('btn-orange', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        Input('btn-red', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        Input({'type': 'name-bubble', 'index': ALL}, 'n_clicks'),
        Input('okay-button2', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        State('selected-companies', 'data'),
        State('page', 'data'),
        State('dataframe-store', 'data'),
        State('dataframe-store-full', 'data'),
        Input('map', 'clickData'), # If the plot has been clicked
        State('step', 'data'),
        State('selected-geography', 'data'),
        Input('okay-button', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        State('selected-sectors', 'data'),
        State('selected-industries', 'data'),
        Input({'type': 'sector-box', 'index': ALL}, 'n_clicks'), # Selected sectors from the grid
        Input({'type': 'industry-box', 'index': ALL}, 'n_clicks'), # Selected industries from the grid
        State('counter-store', 'data'), # Counter value
        Input('large-box-size', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        Input('medium-box-size', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        Input('small-box-size', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        Input('micro-box-size', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        State('selected-size', 'data'), # Track selected size
        Input('next-button', 'n_clicks'), # n_clicks are needed to identify if a button is clicked
        Input('toggle-switch', 'value'),  # Get the current state of the switch
        State('toggle-reference', 'data'),
    ]
)
def update_app(sales_clicks, asset_clicks, borrow_clicks, shrink_clicks, 
               mode, selected_status, names_container,
               green_btn, yellow_btn, orange_btn, red_btn,
               bubble_clicks, okay_clicks2, selected_companies,
               page, df_names, in2, click_data, step, selected_geography,
               okay_clicks, selected_sectors, selected_industries,
               sector_grid_clicks, industry_grid_clicks,
               counter_value, 
               large_clicks, medium_clicks, small_clicks, micro_clicks,
               selected_size, 
               next_clicks,
               toggle_value, toggle_reference):

    global df_global

    # Default return: To return when nothing is to be done
    ret = ([dash.no_update] * 4 +  # The 4 model type buttons style
           [mode, selected_status, names_container] +  # Model mode, selected status, and bubble container
           [dash.no_update] * 5 +  # The 4 color buttons style & Okay button 2 style
           [selected_companies, page] +  # Selected companies tracker and page number
           [dash.no_update] +  # Company display page
           [df_names] +  # The dataframe
           [dash.no_update] +  # Show or hide names container
           [dash.no_update] * 2 +  # Maps figure and style
           [dash.no_update] +  # Okay button 1 style
           [selected_sectors] +  # Selected sectors to keep track of
           [dash.no_update] * 2 +  # Sector container children and style
           [selected_industries, selected_geography, step] +  # Selected industry, geography, and step
           [dash.no_update, dash.no_update, counter_value] + # Counter child, counter style, counter value 
           [dash.no_update] * 4 + # Size boxes style
           [dash.no_update] * 2 + # Print page display child and style
           [selected_size] + # Selected style
           [dash.no_update] + # Upper size box style
           [dash.no_update] + # toggle-switch-card display
           [toggle_value, toggle_reference]) # Toggle value and reference

    # Need for update
    if toggle_value != toggle_reference:

        toggle_reference = not toggle_reference

        # Global map
        if step == "maps1":
            # hotzones or not
            if toggle_value:
                fig = GPlots.plot_global_country_hotzones(glb_rates_metadata, APP_BACKGROUND_COLOR).update_layout(clickmode='event+select')
            else:
                fig = GPlots.plot_global_country(background_color = APP_BACKGROUND_COLOR).update_layout(clickmode='event+select')
    
        # National / NUTS1 map
        if step == "maps2":
    
            # US States plot
            if selected_geography["Country"] == "USA":
                if toggle_value:
                    fig = GPlots.plot_usa_states_hotzones(state_rates_metadata, APP_BACKGROUND_COLOR)
                else:
                    fig = GPlots.plot_usa_states(background_color = APP_BACKGROUND_COLOR)
    
            # NUTS 1
            elif selected_geography["Country"] in GPlots.nuts_countries:
                if toggle_value:
                    fig = GPlots.plot_nuts_country_hotzones(selected_geography["Country"], nuts1_rates_metadata, 1, background_color = APP_BACKGROUND_COLOR)
                else:
                    fig = GPlots.plot_nuts_country(selected_geography["Country"], 1, background_color = APP_BACKGROUND_COLOR)
    
        # Sub-National / NUTS2 maps
        if step == "maps3":
    
            # US Subnational plot
            if selected_geography["Country"] == "USA":
                if toggle_value:
                    fig = GPlots.plot_usa_subnational_hotzones(us_counties_metadata[selected_geography["State"]], 
                                                               selected_geography["State"], APP_BACKGROUND_COLOR)
                else:
                    fig = GPlots.plot_usa_subnational(selected_geography["State"], background_color = APP_BACKGROUND_COLOR)
    
            # NUTS 1
            elif selected_geography["Country"] in GPlots.nuts_countries:
                if toggle_value:
                    fig = GPlots.plot_nuts_country_hotzones(selected_geography["Country"], nuts2_rates_metadata, 2, selected_geography["NUTS1"],background_color = APP_BACKGROUND_COLOR)
                else:
                    fig = GPlots.plot_nuts_country(selected_geography["Country"], 2, selected_geography["NUTS1"], background_color = APP_BACKGROUND_COLOR)
    
        # NUTS3 maps
        if step == "maps4":
            if selected_geography["Country"] in GPlots.nuts_countries:
                
                if toggle_value:
                    fig = GPlots.plot_nuts_country_hotzones(selected_geography["Country"], nuts3_rates_metadata, 3, selected_geography["NUTS1"], 
                                               selected_geography["NUTS2"],
                                               background_color = APP_BACKGROUND_COLOR)
                else:
                    fig = GPlots.plot_nuts_country(selected_geography["Country"], 3, 
                                               selected_geography["NUTS1"], 
                                               selected_geography["NUTS2"],
                                               background_color = APP_BACKGROUND_COLOR)

        return ([dash.no_update] * 4 +  
           [mode, selected_status, names_container] +  
           [dash.no_update] * 5 +  
           [selected_companies, page] +  
           [dash.no_update] +  
           [df_names] +  
           [dash.no_update] +  
           [fig, dash.no_update] + # New map 
           [dash.no_update] +  
           [selected_sectors] +  
           [dash.no_update] * 2 +  
           [selected_industries, selected_geography, step] +  
           [dash.no_update, dash.no_update, counter_value] + 
           [dash.no_update] * 4 + 
           [dash.no_update] * 2 + 
           [selected_size] + 
           [dash.no_update] + 
           [dash.no_update] +
            [toggle_value, toggle_reference])

    # Callback
    ctx = dash.callback_context


    # Nothing triggered = Nothing to be done
    if not ctx.triggered:
        return ret

    # If we are on the global map and clicked on the map
    if step == "maps1" and click_data:

        # Save selected country
        selected_geography["Country"] = click_data["points"][0]["location"]

        # Update df_names
        df_names = df_global[df_global["Country"] == selected_geography["Country"]]["Names"].values.tolist()

        # Case 1: Clicked on USA so we display US States
        if selected_geography["Country"] == "USA":
            
            # Plot usa states
            fig = GPlots.plot_usa_states(background_color = APP_BACKGROUND_COLOR)

            # New map plotted so reset toggle value and reference
            toggle_value = False
            toggle_reference = False

            return ([dash.no_update] * 4 + 
            [mode, selected_status, names_container] + 
            [dash.no_update] * 5 + 
            [selected_companies, page] + 
            [dash.no_update] + 
            [df_names] + # Updated df
            [dash.no_update] + 
            [fig, dash.no_update] +  # New map
            [dash.no_update] + 
            [selected_sectors] +  
            [dash.no_update] * 2 +  
            [selected_industries, selected_geography, "maps2"] + # Updated step and geography
            [f"{len(df_names):,}", AppSetup.counter_out_style(len(df_names), INITIAL_POOL), len(df_names)] + # Update counter child, counter style and counter value
            [dash.no_update] * 4 +
            [dash.no_update] * 2 +
            [selected_size] +
            [dash.no_update]*2 + 
            [toggle_value, toggle_reference]) # Update toggle_value and toggle_reference
        
        # Case 2: European country selected so we plot NUTS1
        elif selected_geography["Country"] in GPlots.nuts_countries:

            # Plot NUTS1
            fig = GPlots.plot_nuts_country(selected_geography["Country"], 1, background_color = APP_BACKGROUND_COLOR)

            # New map plotted so reset toggle value and reference
            toggle_value = False
            toggle_reference = False

            return ([dash.no_update] * 4 + 
            [mode, selected_status, names_container] + 
            [dash.no_update] * 5 + 
            [selected_companies, page] + 
            [dash.no_update] + 
            [df_names] + # Updated df
            [dash.no_update] + 
            [fig, dash.no_update] +  # New map
            [dash.no_update] + 
            [selected_sectors] + 
            [dash.no_update] * 2 + 
            [selected_industries, selected_geography, "maps2"] + # Updated step and geography
            [f"{len(df_names):,}", AppSetup.counter_out_style(len(df_names), INITIAL_POOL), len(df_names)] + # Update counter child, counter style and counter value
            [dash.no_update] * 4 +
            [dash.no_update] * 2 +
            [selected_size] +
            [dash.no_update]*2 + 
            [toggle_value, toggle_reference]) # Update toggle_value and toggle_reference

        # Case 3: Move to sector/ndy grid
        else:

            # New map plotted so reset toggle value and reference
            toggle_value = False
            toggle_reference = False
            
            return ([dash.no_update] * 4 + 
            [mode, selected_status, names_container] + 
            [dash.no_update] * 5 + 
            [selected_companies, page] + 
            [dash.no_update] + 
            [df_names] + # Updated df
            [dash.no_update] + 
            [dash.no_update, {'display' : 'none'}] +  # Hide map
            [{**OKAY_BUTTON_STYLE, 'display' : 'flex'}] +  # Display okay button 1
            [selected_sectors] + 
            [dash.no_update, {**SECTOR_CONTAINER_STYLE, 'display' : 'grid'}] + # Define grid & Show sector & NDY grid
            [selected_industries, selected_geography, "sectors"] +  # Updated step and geography
            [dash.no_update, dash.no_update, counter_value] +
            [dash.no_update] * 4 +
            [dash.no_update] * 2 +
            [selected_size] +
            [dash.no_update] +
            [{'display':'none'}] + # Hide toggle switch
            [toggle_value, toggle_reference]) # Update

    # If current step is maps2, we are displaying US States or NUTS1. Move to next geo granularity aka counties & NUTS2
    if step == "maps2" and click_data:

        # Case 1: Clicked on US States so we display US counties
        if selected_geography["Country"] == "USA":

            # Save selected state
            selected_geography["State"] = click_data["points"][0]["location"]

            # Plot usa cities
            fig = GPlots.plot_usa_subnational(selected_geography["State"], background_color = APP_BACKGROUND_COLOR)

            # New map plotted so reset toggle value and reference
            toggle_value = False
            toggle_reference = False

            return ([dash.no_update] * 4 + 
            [mode, selected_status, names_container] + 
            [dash.no_update] * 5 + 
            [selected_companies, page] + 
            [dash.no_update] + 
            [df_names] + 
            [dash.no_update] + 
            [fig, dash.no_update] +  # New map
            [dash.no_update] + 
            [selected_sectors] + 
            [dash.no_update] * 2 + 
            [selected_industries, selected_geography, "maps3"] + # Updated step and geography
            [f"{len(df_names):,}", AppSetup.counter_out_style(len(df_names), INITIAL_POOL), len(df_names)] + # Update counter child, counter style and counter value
            [dash.no_update] * 4 +
            [dash.no_update] * 2 +
            [selected_size] +
            [dash.no_update]*2 + 
            [toggle_value, toggle_reference]) # Update
        
        # Case 2: Clicked on NUTS1 so we display NUTS2
        elif selected_geography["Country"] in GPlots.nuts_countries:

            # Save selected NUTS2
            selected_geography["NUTS1"] = click_data["points"][0]["location"]

            # Plot NUTS2
            fig = GPlots.plot_nuts_country(selected_geography["Country"], 2, selected_geography["NUTS1"], background_color = APP_BACKGROUND_COLOR)

            # New map plotted so reset toggle value and reference
            toggle_value = False
            toggle_reference = False

            return ([dash.no_update] * 4 + 
            [mode, selected_status, names_container] + 
            [dash.no_update] * 5 + 
            [selected_companies, page] + 
            [dash.no_update] + 
            [df_names] + 
            [dash.no_update] + 
            [fig, dash.no_update] +  # New map
            [dash.no_update] + 
            [selected_sectors] +  
            [dash.no_update] * 2 +  
            [selected_industries, selected_geography, "maps3"] + # Updated step and geography
            [f"{len(df_names):,}", AppSetup.counter_out_style(len(df_names), INITIAL_POOL), len(df_names)] + # Update counter child, counter style and counter value
            [dash.no_update] * 4 +
            [dash.no_update] * 2 +
            [selected_size] +
            [dash.no_update]*2 + 
            [toggle_value, toggle_reference]) # Update
            
    # If current step is maps3, we are displaying US Counties or NUTS2. Move to next geo granularity which is NUTS3
    if step == "maps3" and click_data:

        # Case 1: US County was clicked so we save data and dispay sector/ndy grid
        if selected_geography["Country"] == "USA":

            # Save selected state. This one uses hovertext
            selected_geography["City"] = click_data["points"][0]["hovertext"]

            # New map plotted so reset toggle value and reference
            toggle_value = False
            toggle_reference = False

            return ([dash.no_update] * 4 + 
            [mode, selected_status, names_container] + 
            [dash.no_update] * 5 + 
            [selected_companies, page] + 
            [dash.no_update] + 
            [df_names] + 
            [dash.no_update] + 
            [dash.no_update, {'display' : 'none'}] +  # Hide map
            [{**OKAY_BUTTON_STYLE, 'display' : 'flex'}] +  # Display okay button 1
            [selected_sectors] + 
            [dash.no_update, {**SECTOR_CONTAINER_STYLE, 'display' : 'grid'}] + # Define grid & Show sector & NDY grid
            [selected_industries, selected_geography, "sectors"] + # Updated step and geography
            [f"{len(df_names):,}", AppSetup.counter_out_style(len(df_names), INITIAL_POOL), len(df_names)] + # Update counter child, counter style and counter value
            [dash.no_update] * 4 +
            [dash.no_update] * 2 +
            [selected_size] +
            [dash.no_update] + 
            [{'display':'none'}] + # Hide toggle switch
            [toggle_value, toggle_reference]) # Update
        
        # CAse 2: NUTS2 was clicked so we save data and display NUTS3
        elif selected_geography["Country"] in GPlots.nuts_countries:

            # Save selected NUTS2
            selected_geography["NUTS2"] = click_data["points"][0]["location"]

            # Plot NUTS3
            fig = GPlots.plot_nuts_country(selected_geography["Country"], 3, 
                                           selected_geography["NUTS1"], 
                                           selected_geography["NUTS2"],
                                           background_color = APP_BACKGROUND_COLOR)

            # New map plotted so reset toggle value and reference
            toggle_value = False
            toggle_reference = False

            return ([dash.no_update] * 4 + 
            [mode, selected_status, names_container] + 
            [dash.no_update] * 5 + 
            [selected_companies, page] + 
            [dash.no_update] + 
            [df_names] + 
            [dash.no_update] + 
            [fig, dash.no_update] +  # New map
            [dash.no_update] + 
            [selected_sectors] + 
            [dash.no_update] * 2 + 
            [selected_industries, selected_geography, "maps4"] + # Updated step and geography
            [f"{len(df_names):,}", AppSetup.counter_out_style(len(df_names), INITIAL_POOL), len(df_names)] + # Update counter child, counter style and counter value
            [dash.no_update] * 4 +
            [dash.no_update] * 2 +
            [selected_size] +
            [dash.no_update]*2 + 
            [toggle_value, toggle_reference]) # Update
    
    # If current step is maps4, we are displaying NUTS3 and we want to move onto sector/ndy grid
    if step == 'maps4' and click_data:

        # Save selected NUTS2
        selected_geography["NUTS3"] = click_data["points"][0]["location"]

        # New map plotted so reset toggle value and reference
        toggle_value = False
        toggle_reference = False
        
        return ([dash.no_update] * 4 + 
        [mode, selected_status, names_container] + 
        [dash.no_update] * 5 + 
        [selected_companies, page] + 
        [dash.no_update] + 
        [df_names] + 
        [dash.no_update] + 
        [dash.no_update, {'display' : 'none'}] + # Hide map
        [{**OKAY_BUTTON_STYLE, 'display' : 'flex'}] + # Display okay button 1
        [selected_sectors] + 
        [dash.no_update, {**SECTOR_CONTAINER_STYLE, 'display' : 'grid'}] + # Define grid & Show sector & NDY grid
        [selected_industries, selected_geography, "sectors"] + # Updated step
        [f"{len(df_names):,}", AppSetup.counter_out_style(len(df_names), INITIAL_POOL), len(df_names)] + # Update counter child, counter style and counter value
        [dash.no_update] * 4 +
        [dash.no_update] * 2 +
        [selected_size] +
        [dash.no_update] + 
        [{'display':'none'}] + # Hide toggle switch
        [toggle_value, toggle_reference]) # Update
    
    # If the current step is sector and the grid was clicked, we update the grid colors to reflect selection
    if step == 'sectors' and ctx.triggered and 'sector-box' in ctx.triggered[0]['prop_id']:
        
        # Selected sector on grid
        clicked_index = json.loads(ctx.triggered[0]['prop_id'].split('.')[0])['index']
        print(ctx.triggered[0]['prop_id'])
        selected_sector = sectors_ndy[clicked_index]["name"]

        # Toggle the selected sector
        # If a sector is selected add it for tracking
        # If a sector was already selected, deselect it
        if selected_sector in selected_sectors:
            selected_sectors.remove(selected_sector)
        else:
            selected_sectors.append(selected_sector)

        # Update the sector grid with new colors
        sector_children = AppSetup.sector_ndy_containers(selected_sectors)
        
        return ([dash.no_update] * 4 + 
        [mode, selected_status, names_container] + 
        [dash.no_update] * 5 + 
        [selected_companies, page] + 
        [dash.no_update] + 
        [df_names] + 
        [dash.no_update] + 
        [dash.no_update] * 2 + 
        [dash.no_update] +
        [selected_sectors] + # Update selected sectors
        [sector_children, dash.no_update] + # Update grid and maintain style
        [selected_industries, selected_geography, step] +
        [dash.no_update, dash.no_update, counter_value] +
        [dash.no_update] * 4 +
        [dash.no_update] * 2 +
        [selected_size] +
        [dash.no_update] +
        [dash.no_update] + 
        [toggle_value, toggle_reference])

    # Get clicked id
    clicked_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Handle case when the okay button is clicked and we are on sector grid. Move to ndy grid.
    # Hide the sector grid and display industry grid of industries in the selected sectors
    if clicked_id == 'okay-button' and step == "sectors":

        # Update df
        df_names = df_global[(df_global["Country"] == selected_geography["Country"]) & (df_global["Sector"].isin(selected_sectors))]["Names"].values.tolist()

        industry_children = AppSetup.associated_ndy_grid(selected_sectors)

        return ([dash.no_update] * 4 + 
        [mode, selected_status, names_container] + 
        [dash.no_update] * 5 + 
        [selected_companies, page] + 
        [dash.no_update] + 
        [df_names] + 
        [dash.no_update] + 
        [dash.no_update] * 2 + 
        [dash.no_update] + 
        [selected_sectors] + 
        [industry_children, {**SECTOR_CONTAINER_STYLE, 'display': 'grid'}] +  # Update grid and reload grid style
        [selected_industries, selected_geography, "industries"] + # Update step
        [f"{len(df_names):,}", AppSetup.counter_out_style(len(df_names), INITIAL_POOL), len(df_names)] + # Update counter child, counter style and counter value
        [dash.no_update] * 4 +
        [dash.no_update] * 2 +
        [selected_size] +
        [dash.no_update] +
        [dash.no_update] + 
        [toggle_value, toggle_reference])
        
    # If current step is industries and the grid was clicked: Updated the grid colors to show selection
    if step == 'industries' and 'industry-box' in ctx.triggered[0]['prop_id']:

        # Selected industry on grid
        clicked_index = json.loads(ctx.triggered[0]['prop_id'].split('.')[0])['index']

        # Identify the selected industry and its sector color
        selected_industry = None
        sector_color = None
        industry_counter = 0
        for sector in sectors_ndy:
            if sector["name"] in selected_sectors:
                for industry in sector["industries"]:
                    if industry_counter == clicked_index:
                        selected_industry = industry
                        sector_color = sector["color"]
                        break
                    industry_counter += 1
            if selected_industry:
                break
        
        # Toggle the selected industry
        # If a industry is selected add it for tracking
        # If a industry was already selected, deselect it
        if selected_industry in selected_industries:
            selected_industries.remove(selected_industry)
        else:
            selected_industries.append(selected_industry)

        # Update the industry grid with the new selection and color change
        industry_children = AppSetup.associated_ndy_grid(selected_sectors, selected_industries)

        return ([dash.no_update] * 4 + 
        [mode, selected_status, names_container] + 
        [dash.no_update] * 5 + 
        [selected_companies, page] + 
        [dash.no_update] + 
        [df_names] + 
        [dash.no_update] + 
        [dash.no_update] * 2 + 
        [dash.no_update] + 
        [selected_sectors] + 
        [industry_children, dash.no_update] + # Update grid
        [selected_industries, selected_geography, "industries"] + # Selected industries updated
        [dash.no_update, dash.no_update, counter_value] + 
        [dash.no_update] * 4 +
        [dash.no_update] * 2 +
        [selected_size] +
        [dash.no_update] +
        [dash.no_update] + 
        [toggle_value, toggle_reference])

    # Handle case when the okay button is clicked and we are on ndy grid. Move to size page
    # Hide the sector grid and display industry grid of industries in the selected sectors
    if clicked_id == 'okay-button' and step == "industries":

        # Update df
        df_names = df_global[(df_global["Country"] == selected_geography["Country"]) & (df_global["Sector"].isin(selected_sectors)) & (df_global["Industry"].isin(selected_industries))]["Names"].values.tolist()

        # Define style for size boxes
        size_styles = {
            'large': {**BOX_STYLE_FULL['large']},
            'medium': {**BOX_STYLE_FULL['medium']},
            'small': {**BOX_STYLE_FULL['small']},
            'micro': {**BOX_STYLE_FULL['micro']},
            }

        return ([dash.no_update]*4 + 
        [mode, selected_status, names_container] +
        [dash.no_update] * 5 + 
        [selected_companies, page] + 
        [dash.no_update] + 
        [df_names] +
        [dash.no_update] + 
        [dash.no_update] * 2 + 
        [dash.no_update] + 
        [selected_sectors] + 
        [[], {"display" : 'none'}] + # Update grid with empty list and hide plot
        [selected_industries, selected_geography, "size"] + # Update step 
        [f"{len(df_names):,}", AppSetup.counter_out_style(len(df_names), INITIAL_POOL), len(df_names)] + # Update counter child, counter style and counter value
        [size_styles['large'], size_styles['medium'], size_styles['small'], size_styles['micro']] + # Updated size box styles
        [dash.no_update] * 2 +
        [selected_size] +
        [dash.no_update] +
        [dash.no_update] + 
        [toggle_value, toggle_reference])

    # Handle cases when size boxes are clicked
    if step == "size" and "-size" in clicked_id:

        size_styles = {
            'large': {**BOX_STYLE_FULL['large']},
            'medium': {**BOX_STYLE_FULL['medium']},
            'small': {**BOX_STYLE_FULL['small']},
            'micro': {**BOX_STYLE_FULL['micro']},
            }

        # Save selected size
        selected_size = clicked_id.replace('-box-size', '')

        # Slightly zoom in to the selection
        size_styles[selected_size].update(HOVER_STYLE)

        return ([dash.no_update]*4 + 
        [mode, selected_status, names_container] +
        [dash.no_update] * 5 + 
        [selected_companies, page] + 
        [dash.no_update] + 
        [df_names] +
        [dash.no_update] + 
        [dash.no_update] * 2 + 
        [dash.no_update] + 
        [selected_sectors] + 
        [dash.no_update] * 2 +
        [selected_industries, selected_geography, step] +
        [f"{len(df_names):,}", AppSetup.counter_out_style(len(df_names), INITIAL_POOL), len(df_names)] + # Update counter child, counter style and counter value
        [size_styles['large'], size_styles['medium'], size_styles['small'], size_styles['micro']] + # Updated size box styles
        [dash.no_update] * 2 +
        [selected_size] + # Selected size updated
        [dash.no_update] +
        [dash.no_update] + 
        [toggle_value, toggle_reference])

    # Handle cases when okay button is pressed on size page. We move on to name print page
    if clicked_id == "okay-button" and step == "size":

        print_page_child = AppSetup.print_page(selected_sectors, selected_industries, selected_geography, selected_size)

        df_names = df_global[(df_global["Country"] == selected_geography["Country"]) & (df_global["Sector"].isin(selected_sectors)) & (df_global["Industry"].isin(selected_industries)) & (df_global["Size"] == selected_size.capitalize())]["Names"].values.tolist()

        selected_status = {i: False for i in df_names}

        return ([dash.no_update]*4 + 
        [mode, selected_status, names_container] +
        [dash.no_update] * 5 + 
        [selected_companies, page] + 
        [dash.no_update] + 
        [df_names] +
        [dash.no_update] + 
        [dash.no_update] * 2 + 
        [dash.no_update] + 
        [selected_sectors] + 
        [dash.no_update] * 2 +
        [selected_industries, selected_geography, "print"] + # Update step
        [f"{len(df_names):,}", AppSetup.counter_out_style(len(df_names), INITIAL_POOL), len(df_names)] + # Update counter child, counter style and counter value
        [{'display' : 'none'}]*4 + # Updated size box styles
        [print_page_child, {**PRINT_STYLE}] + # Update print page
        [selected_size] +
        [dash.no_update] +
        [dash.no_update] + 
        [toggle_value, toggle_reference])

    if clicked_id == "okay-button" and step == "print":

        df = df_global[df_global["Names"].isin(df_names)][["Names", "Category"]].copy()

        # Define names container
        names_container = AppSetup.bubble_element_child(df)

        return ([AppSetup.model_mode_button_style(mode == "Sales"), 
                AppSetup.model_mode_button_style(mode == "Asset"), 
                AppSetup.model_mode_button_style(mode == "Borrow"), 
                AppSetup.model_mode_button_style(mode == "Shrink")] + # Display the category buttons
        [mode, selected_status, names_container] + # Updated names container
        [{**COLOR_BUTTON_STYLE, 'backgroundColor': category_colors['Green']},
         {**COLOR_BUTTON_STYLE, 'backgroundColor': category_colors['Yellow']},
         {**COLOR_BUTTON_STYLE, 'backgroundColor': category_colors['Orange']},
         {**COLOR_BUTTON_STYLE, 'backgroundColor': category_colors['Red']}
        ] + # Display the color buttons
        [{**OKAY_BUTTON_STYLE, 'display': 'flex'}] + # Display okay button 2
        [selected_companies, page] + 
        [dash.no_update] + 
        [df_names] +
        [{'textAlign': 'center', 'display': 'flex', 'flexWrap': 'wrap', 
          'justifyContent': 'center', 'margin_top':'15px'}] + # Start displaying the names container
        [dash.no_update] * 2 + 
        [{'display' : 'none'}] + # Hide okay button 1
        [selected_sectors] + 
        [dash.no_update] * 2 +
        [selected_industries, selected_geography, "finished"] + # Update step and it is no longer used
        [f"{len(df_names):,}", AppSetup.counter_out_style(len(df_names), INITIAL_POOL), len(df_names)] + # Update counter child, counter style and counter value
        [{'display' : 'none'}]*4 + 
        [[], {'display' : 'none'}] + # Hide print page
        [selected_size] +
        [dash.no_update] +
        [dash.no_update] + 
        [toggle_value, toggle_reference])

    # The mode selection buttons start with button, other buttons have a different starting expression for easy differentiation
    if clicked_id.startswith('button-'):  # Check that a color button was clicked

        # Extract selected mode
        mode_clicked = clicked_id.split('-')[1].capitalize()

        # Check if the selected mode is the current mode only so return everything as is
        if mode == mode_clicked:
            return ret

        ## Continued from if a different mode was selected

        # Deselect all the selected ones by setting it to initial value which is all False
        selected_status_new = {i:False for i,j in selected_status.items()}

        # Update model mode parameter for tracking
        mode = mode_clicked

        # Reorder the dataframe using the new mode column
        df = df_global[df_global["Names"].isin(df_names)][["Names", "Category", mode+"P"]].copy()
        df = Setup.model_type_prep(df, mode)

        # Update the bubble selections
        names_container = AppSetup.bubble_element_child(df, selected_status_new)

        # Update the style of the buttons to reflect what was selected
        return ([AppSetup.model_mode_button_style(mode == "Sales"), 
                AppSetup.model_mode_button_style(mode == "Asset"), 
                AppSetup.model_mode_button_style(mode == "Borrow"), 
                AppSetup.model_mode_button_style(mode == "Shrink")] + # Display the category buttons with updated mode
        [mode, selected_status_new, names_container] + # Mode, selected status and names container are updated
        [dash.no_update] * 5 +
        [selected_companies, page] + 
        [dash.no_update] + 
        [df_names] + 
        [dash.no_update] + 
        [dash.no_update] * 2 + 
        [dash.no_update] + 
        [selected_sectors] + 
        [dash.no_update] * 2 +
        [selected_industries, selected_geography, step] + # Update step and it is no longer used
        [dash.no_update, dash.no_update, counter_value] +
        [dash.no_update] * 4 +
        [dash.no_update] * 2 +
        [selected_size] +
        [dash.no_update] +
        [dash.no_update] + 
        [toggle_value, toggle_reference])
    
    # Handle color category click
    if clicked_id.startswith('btn-'):  # Check that a color button was clicked

        # Extract color category
        category_clicked = clicked_id.split('-')[1].capitalize()

        df = df_global[df_global["Names"].isin(df_names)][["Names", "Category"]].copy()

        # Whether the clicked category should select or deselct
        toggle_select = not all([selected_status[name] for name in df[df["Category"] == category_clicked]["Names"]])

        # Update the grid selections status
        for name in df[df['Category'] == category_clicked]['Names']:
            selected_status[name] = toggle_select

        # Update names container bubble colors based on selection status
        names_container = AppSetup.bubble_element_child(df, selected_status)

        return ([dash.no_update] * 4 +
        [mode, selected_status, names_container] + # Selected status and names container are updated
        [dash.no_update] * 5 +
        [selected_companies, page] + 
        [dash.no_update] + 
        [df_names] + 
        [dash.no_update] + 
        [dash.no_update] * 2 + 
        [dash.no_update] + 
        [selected_sectors] + 
        [dash.no_update] * 2 + 
        [selected_industries, selected_geography, step] +
        [dash.no_update, dash.no_update, counter_value] +
        [dash.no_update] * 4 +
        [dash.no_update] * 2 +
        [selected_size] +
        [dash.no_update] +
        [dash.no_update] + 
        [toggle_value, toggle_reference])

    
    # Handle cases when a name bubble is clicked.
    if 'name-bubble' in clicked_id:

        # Get index of clicked bubble
        name_clicked = json.loads(clicked_id)['index']

        # Toggle on/off
        selected_status[name_clicked] = not selected_status[name_clicked]

        df = df_global[df_global["Names"].isin(df_names)][["Names", "Category"]].copy()

        # Update names container bubble colors based on selection status
        names_container = AppSetup.bubble_element_child(df, selected_status)

        return ([dash.no_update] * 4 + 
        [mode, selected_status, names_container] + # Selected status and names container are updated
        [dash.no_update] * 5 +
        [selected_companies, page] + 
        [dash.no_update] + 
        [df_names] + 
        [dash.no_update] + 
        [dash.no_update] * 2 + 
        [dash.no_update] + 
        [selected_sectors] + 
        [dash.no_update] * 2 + 
        [selected_industries, selected_geography, step] + 
        [dash.no_update, dash.no_update, counter_value] +
        [dash.no_update] * 4 +
        [dash.no_update] * 2 +
        [selected_size] +
        [dash.no_update] +
        [dash.no_update] + 
        [toggle_value, toggle_reference])
    

    # Handle case when the okay button is clicked: Move to company page and hide the model mode and color category buttons
    if clicked_id == 'okay-button2':

        # Start tracking selected names
        selected_companies = [name for name, selected in selected_status.items() if selected]

        # Return everything as is
        if not selected_companies:
            return ret

        # Get the first company info
        first_company = selected_companies[0]
        company_data = df_global[df_global['Names'] == first_company].copy().iloc[0]

        # Okay button new style: Hidden
        # new_style = {**OKAY_BUTTON_STYLE, 'display': 'none'}

        # Get the cards for this particular company
        cards = AppSetup.company_page_generator(company_data, df_full, page, model_type_list)

        return ([{'display' : 'none'}] * 4 +  # Hide mode buttons
        [mode, selected_status, []] +  # Update names container with empty list
        [{'display' : 'none'}] * 5 + # hide 4 color category buttons & okay button 2
        [selected_companies, page] +  # Selected companies updated
        [cards] +  # Company page displayed
        [df_names] + 
        [dash.no_update] + 
        [dash.no_update] * 2 + 
        [dash.no_update] + 
        [selected_sectors] + 
        [dash.no_update] * 2 + 
        [selected_industries, selected_geography, step] + 
        [dash.no_update, {'display' : 'none'}, counter_value] + # Hide the counter
        [dash.no_update] * 4 +
        [dash.no_update] * 2 +
        [selected_size] +
        [{**NEXT_BUTTON_STYLE}] +
        [dash.no_update] + 
        [toggle_value, toggle_reference])

    # If the next button is clicked then we move on to the next company
    if clicked_id == "next-button":

        # Get new page and relevant company data
        page = (page + 1) % len(selected_companies)
        company = selected_companies[page]
        company_data = df_global[df_global['Names'] == company].copy().iloc[0]

        # Get the cards for this particular company
        cards = AppSetup.company_page_generator(company_data, df_full, page, model_type_list)

        return ([dash.no_update] * 4 + 
        [mode, selected_status, names_container] + 
        [dash.no_update] * 5 +
        [selected_companies, page] + # page updated
        [cards] +  # Company page displayed
        [df_names] + 
        [dash.no_update] + 
        [dash.no_update] * 2 + 
        [dash.no_update] + 
        [selected_sectors] + 
        [dash.no_update] * 2 + 
        [selected_industries, selected_geography, step] + 
        [dash.no_update, dash.no_update, counter_value] +
        [dash.no_update] * 4 +
        [dash.no_update] * 2 +
        [selected_size] +
        [dash.no_update] +
        [dash.no_update] + 
        [toggle_value, toggle_reference])

    # If everything passes through, return default
    return ret

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
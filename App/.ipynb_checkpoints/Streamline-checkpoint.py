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

class StateManager:
    # Initialize state
    def __init__(self):
        self.df_names = df_global["Names"].values.tolist()
        self.mode = "Sales"
        self.selected_status = {}
        self.names_container = []
        self.selected_companies = []
        self.page = 0
        self.step = "startPage"
        self.selected_geography = {}
        self.selected_sectors = []
        self.selected_industries = []
        self.counter = INITIAL_POOL
        self.selected_size = "large"
        self.toggle_value = False # Is always False to begin with
        self.toggle_reference = False
        self.fig = AppSetup.placeholder()
        self.curr_step = "startPage"

        # Never returned or updated
        self._background_color = APP_BACKGROUND_COLOR
        self._full_count = INITIAL_POOL

    def return_init(self):
        # Initialize / Reinitialize variables that are mostly not updated.
        # We will update them manually if need be
        self.sales_button_style = dash.no_update
        self.asset_button_style = dash.no_update
        self.borrow_button_style = dash.no_update
        self.shrink_button_style = dash.no_update
        self.color_buttons_style = dash.no_update
        self.okay_button2 = dash.no_update
        self.grid_output = dash.no_update
        self.names_container_style = dash.no_update
        self.fig_style = dash.no_update
        self.okay_button = dash.no_update
        self.sector_children = dash.no_update
        self.sector_grid_style = dash.no_update
        self.counter_display = dash.no_update
        self.counter_style = dash.no_update
        self.large_button_style = dash.no_update
        self.medium_button_style = dash.no_update
        self.small_button_style = dash.no_update
        self.micro_button_style = dash.no_update
        self.selection_print_child = dash.no_update
        self.selection_print_style = dash.no_update
        self.next_button = dash.no_update
        self.toggle_card = dash.no_update
        self.start_page_children = dash.no_update
        self.start_page_style = dash.no_update

    def exploratory_selection(self):

        print("TRIGGERED")
        self.start_page_style = {"display":"none"}
        print("TRIGGERED2")
        self.fig = GPlots.plot_global_country(background_color = APP_BACKGROUND_COLOR).update_layout(clickmode='event+select')
        self.fig_style = {**Setup.geofig_styling, 
                          "backgroundColor":APP_BACKGROUND_COLOR}
        self.step = "maps1"

        print("WENT THROUGH")
        # Start showing hotzones toggle and display counter
        self.toggle_card = Setup.hotzone_toggle
        self.counter_style = AppSetup.counter_out_style(1, 1)

    def update_geo(self, click_data):
        if self.step == "maps1":
            self.selected_geography["Country"] = click_data["points"][0]["location"]
            self.step_next = "maps2" if self.selected_geography["Country"] in np.append(["USA"],GPlots.nuts_countries) else "sectors"
        elif self.step == "maps2" and self.selected_geography["Country"] == "USA":
            self.selected_geography["State"] = click_data["points"][0]["location"]
            self.step_next = "maps3"
        elif self.step == "maps3" and self.selected_geography["Country"] == "USA":
            self.selected_geography["City"] = click_data["points"][0]["hovertext"]
            self.step_next = "sectors"
        elif self.step in ["maps2", "maps3", "maps4"] and self.selected_geography["Country"] in GPlots.nuts_countries:
            level_key = f"NUTS{int(self.step[-1]) - 1}"
            self.selected_geography[level_key] = click_data["points"][0]["location"]
            self.step_next = f"maps{int(self.step[-1]) + 1}" if self.step != "maps4" else "sectors"

    def update_geofigure(self):

        # Choose metadata
        if self.step == "maps1":
            self.fig = GPlots.App_Plot_Handling(self.step, self.toggle_value, self.selected_geography, self._background_color, glb_rates_metadata if self.toggle_value else None)
            
        elif self.step == "maps2" and self.selected_geography["Country"] == "USA":
            self.fig = GPlots.App_Plot_Handling(self.step, self.toggle_value, self.selected_geography, self._background_color, state_rates_metadata if self.toggle_value else None)
            
        elif self.step == "maps3" and self.selected_geography["Country"] == "USA":
            self.fig = GPlots.App_Plot_Handling(self.step, self.toggle_value, self.selected_geography, self._background_color, us_counties_metadata if self.toggle_value else None)
            
        elif self.step == "maps2" and self.selected_geography["Country"] in GPlots.nuts_countries:
            self.fig = GPlots.App_Plot_Handling(self.step, self.toggle_value, self.selected_geography, self._background_color, nuts1_rates_metadata if self.toggle_value else None)

        elif self.step == "maps3" and self.selected_geography["Country"] in GPlots.nuts_countries:
            self.fig = GPlots.App_Plot_Handling(self.step, self.toggle_value, self.selected_geography, self._background_color, nuts2_rates_metadata if self.toggle_value else None)

        elif self.step == "maps4" and self.selected_geography["Country"] in GPlots.nuts_countries:
            self.fig = GPlots.App_Plot_Handling(self.step, self.toggle_value, self.selected_geography, self._background_color, nuts3_rates_metadata if self.toggle_value else None)

    def steps_align(self):
        self.step = self.step_next

    def toggle_reset(self):
        self.toggle_value = False
        self.toggle_reference = False

    def update_names_old(self, df_global, filter_col, dict_key, name_col):

        self.df_names = df_global[df_global[filter_col] == self.selected_geography[dict_key]][name_col].values.tolist()

    def update_names(self, df_global):

        if self.step in ["maps1", "maps2", "maps3", "maps4"]:
            self.df_names = df_global[df_global["Country"] == self.selected_geography["Country"]]["Names"].values.tolist()

        elif self.step == "sectors":
            self.df_names = df_global[(df_global["Country"] == self.selected_geography["Country"]) & (df_global["Sector"].isin(self.selected_sectors))]["Names"].values.tolist()

        elif self.step == "industries":
            self.df_names = df_global[(df_global["Country"] == self.selected_geography["Country"]) & (df_global["Sector"].isin(self.selected_sectors)) & (df_global["Industry"].isin(self.selected_industries))]["Names"].values.tolist()

        elif self.step == "size":
            self.df_names = df_global[(df_global["Country"] == self.selected_geography["Country"]) & (df_global["Sector"].isin(self.selected_sectors)) & (df_global["Industry"].isin(self.selected_industries)) & (df_global["Size"] == self.selected_size.capitalize())]["Names"].values.tolist()
            

        # Update counter and counter style
        self.counter_display = f"{len(self.df_names):,}"
        self.counter_style = AppSetup.counter_out_style(len(self.df_names), self._full_count)
        self.counter = len(self.df_names)

    def update_selected_sectors(self, clicked_index):
        
        selected_sector = sectors_ndy[clicked_index]["name"]

        # Toggle the selected sector
        # If a sector is selected add it for tracking
        # If a sector was already selected, deselect it
        if selected_sector in self.selected_sectors:
            self.selected_sectors.remove(selected_sector)
        else:
            self.selected_sectors.append(selected_sector)

        # Update the sector grid with new colors
        self.sector_children = AppSetup.sector_ndy_containers(self.selected_sectors)

    def updated_selected_industries(self, clicked_index = None):

        # Make the sector children empty
        self.sector_children = []

        if clicked_index is None:
            self.sector_children = AppSetup.associated_ndy_grid(self.selected_sectors)

        else:
            # Identify the selected industry and its sector color
            selected_industry = None
            sector_color = None
            industry_counter = 0
            for sector in sectors_ndy:
                if sector["name"] in self.selected_sectors:
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
            if selected_industry in self.selected_industries:
                self.selected_industries.remove(selected_industry)
            else:
                self.selected_industries.append(selected_industry)

        # Update the industry grid with the new selection and color change
        self.sector_children = AppSetup.associated_ndy_grid(self.selected_sectors, self.selected_industries)

    def size_matrix_update(self, BOX_STYLE_FULL, HOVER_STYLE):
        self.large_button_style, self.medium_button_style, self.small_button_style, self.micro_button_style = [
    {**BOX_STYLE_FULL[size], **(HOVER_STYLE if size == self.selected_size else {})}
    for size in ['large', 'medium', 'small', 'micro']]

    def display_print_page(self):
        self.selection_print_child = AppSetup.print_page(self.selected_sectors, self.selected_industries, self.selected_geography, self.selected_size)

        # Hide the size panels
        self.large_button_style = {"display": "none"}
        self.medium_button_style = {"display": "none"}
        self.small_button_style = {"display": "none"}
        self.micro_button_style = {"display": "none"}
                
    def update_bubbles_mode(self, df, mode_clicked):

        # Check if the selected mode is a different mode to run anything
        if self.mode != mode_clicked:
            
            self.mode = mode_clicked

            # Reorder the dataframe using the new mode column
            df = df[df["Names"].isin(self.df_names)][["Names", "Category", self.mode+"P"]].copy()
            df = Setup.model_type_prep(df, self.mode)

            # Deselect all the selected ones by setting it to initial value which is all False
            self.selected_status = {i:False for i,j in self.selected_status.items()}
            
            # Update the bubble selections
            self.names_container = AppSetup.bubble_element_child(df, self.selected_status)

    def update_bubbles_color(self, df, category_clicked):

        # Reorder the dataframe using the new mode column
        df = df[df["Names"].isin(self.df_names)][["Names", "Category", self.mode+"P"]].copy()
        df = Setup.model_type_prep(df, self.mode)

        # Whether the clicked category should select or deselct
        toggle_select = not all([self.selected_status[name] for name in df[df["Category"] == category_clicked]["Names"]])

        # Update the grid selections status
        for name in df[df['Category'] == category_clicked]['Names']:
            self.selected_status[name] = toggle_select

        # Update names container bubble colors based on selection status
        self.names_container = AppSetup.bubble_element_child(df, self.selected_status)

    def update_bubbles_click(self, df, name_clicked):

        # Reorder the dataframe using the new mode column
        df = df[df["Names"].isin(self.df_names)][["Names", "Category", self.mode+"P"]].copy()
        df = Setup.model_type_prep(df, self.mode)

        # Toggle on/off
        self.selected_status[name_clicked] = not self.selected_status[name_clicked]
        # Update names container bubble colors based on selection status
        self.names_container = AppSetup.bubble_element_child(df, self.selected_status)

    def update_name_bubbles(self, df_global, clicked = None, triggered_id = None):

        if clicked is None:
            df = df_global[df_global["Names"].isin(self.df_names)][["Names", "Category"]].copy()
            self.names_container = AppSetup.bubble_element_child(df, self.selected_status)

        else:
            if triggered_id.startswith("button-"):                
                self.update_bubbles_mode(df_global, clicked)
                
            elif triggered_id.startswith("btn-"):
                self.update_bubbles_color(df_global, clicked)
                
            elif "name-bubble" in triggered_id:
                self.update_bubbles_click(df_global, json.loads(triggered_id)['index'])

    def names_bubbles_buttons(self, hide = False):

        if hide:
            self.sales_button_style = {'display' : 'none'}
            self.asset_button_style = {'display' : 'none'}
            self.borrow_button_style = {'display' : 'none'}
            self.shrink_button_style = {'display' : 'none'}
            self.color_buttons_style = {'display' : 'none'}
        else:
            self.sales_button_style = AppSetup.model_mode_button_style(self.mode == "Sales")
            self.asset_button_style = AppSetup.model_mode_button_style(self.mode == "Asset")
            self.borrow_button_style = AppSetup.model_mode_button_style(self.mode == "Borrow")
            self.shrink_button_style = AppSetup.model_mode_button_style(self.mode == "Shrink")
            self.color_buttons_style = {'textAlign': 'center'}

    def initial_company_page(self, df_global, df_full, model_type_list):

        self.names_container = []

        self.selected_companies = [name for name, selected in self.selected_status.items() if selected]

        if self.selected_companies:
            self.company_data = df_global[df_global['Names'] == self.selected_companies[0]].copy().iloc[0]

            self.grid_output = AppSetup.company_page_generator(self.company_data, df_full, self.page, model_type_list)

    def update_company_page(self, df_global, df_full, model_type_list):

        # Get new page and relevant company data
        self.page = (self.page + 1) % len(self.selected_companies)

        self.selected_companies = [name for name, selected in self.selected_status.items() if selected]

        if self.selected_companies:
            self.company_data = df_global[df_global['Names'] == self.selected_companies[self.page]].copy().iloc[0]

            self.grid_output = AppSetup.company_page_generator(self.company_data, df_full, self.page, model_type_list)
        
    def to_dict(self):

        # Skip vars that are app attributes as they are extra and reset every time
        vars_to_skip = ["sales_button_style", "asset_button_style", "borrow_button_style", "shrink_button_style", "color_buttons_style", "okay_button2", "grid_output", "names_container_style", "fig_style", "okay_button", "sector_children", "sector_grid_style", "counter_display", "counter_style", "large_button_style", "medium_button_style", "small_button_style", "micro_button_style", "selection_print_child", "selection_print_style", "next_button", "toggle_card", "start_page_children", "start_page_style"]
        # Serialize instance variables, handling any complex types if needed
        return {k: v for k, v in self.__dict__.items() if k not in vars_to_skip}

    @classmethod
    def from_dict(cls, data):
        # Create an instance from a dictionary, handling any complex types if needed
        instance = cls()
        instance.__dict__.update(data)
        return instance
    
    def return_list(self):

        ## Match current step to step
        self.curr_step = self.step

        return [
            self.sales_button_style, self.asset_button_style, 
            self.borrow_button_style, self.shrink_button_style,
            self.names_container,
            self.color_buttons_style,
            self.okay_button2, 
            self.grid_output, 
            self.names_container_style,
            self.fig, self.fig_style,
            self.okay_button, 
            self.sector_children, self.sector_grid_style,
            self.counter_display, self.counter_style, 
            self.large_button_style, self.medium_button_style,
            self.small_button_style, self.micro_button_style,
            self.selection_print_child, self.selection_print_style,
            self.next_button,
            self.toggle_card, self.toggle_value,
            self.start_page_children, self.start_page_style,
            ]

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
    dcc.Store(id = "state-manager"), # Stored data full

    html.Div(
        id = "start-page",
        style = {'display': 'flex', 'height': '100vh', 'overflow': 'hidden'},
        children = [
            # Left half for exploratory search
            html.Div(
                id = "exploratory-half",
                children = html.H2("Exploratory Search",
                                  style = {'color': 'white', 'font-size': '2.5em'}),
                style = Setup.exploratory_half,
            ),
            # Right half for targeted search
            html.Div(
                id = "targeted-half",
                children = html.H2("Targeted Search",
                                  style = {'color': 'white', 'font-size': '2.5em'}),
                style = Setup.targeted_half,
            ),
        ]
    ),

    # html.Div([],style = {'marginTop': '10px'},    # Add distance from the top of the page
    # ),

    # Geographical plots container
    html.Div(
        id = "map-overall",
        children = [dcc.Graph(id = 'map', 
                  figure = AppSetup.placeholder()
                 ),
                   ],
        style = {'display': 'none'}  
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
    # id: category-btns
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
    # Initially hidden
    AppSetup.toggle_switch_card(),

    # Counter display
    AppSetup.initial_counter_display(INITIAL_POOL),

    # Next button for switching between companies
    html.Div([
        html.Button("➤", id='next-button', n_clicks=0, style={'display' : 'none'}),
    ], 
             # style={'textAlign': 'left', 'marginTop': '20px'}
            ),  # Left-align the button and add top margin

    
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
        Output('names-container', 'children'), # What names to show for selection
        Output('color-buttons', 'style'), #
        Output('okay-button2', 'style'), # Okay button 2 hidden or shown
        Output('grid-output', 'children'), # Company display page
        Output('names-container', 'style'), # Show or hide names container
        Output('map', 'figure'), # What map plot to display
        Output('map-overall', 'style'), # Map plot hidden or shown
        Output('okay-button', 'style'), # Okay button hidden or shown
        Output('sector-container', 'children'), # Sector grid layout updated
        Output('sector-container', 'style'), # Overall grid info to hide or show it
        Output('counter-display', 'children'), # What counter value to display
        Output('counter-display', 'style'), # The counter style
        Output('large-box-size', 'style'), # Large size box style
        Output('medium-box-size', 'style'), # Medium size box style
        Output('small-box-size', 'style'), # Small size box style
        Output('micro-box-size', 'style'), # Micro size box style
        Output('display-out', 'children'), # Selected output display
        Output('display-out', 'style'), # Selected output display style
        Output('next-button', 'style'), # Next button style
        Output('toggle-switch-card', 'style'), # Toggle switch card style
        Output('toggle-switch', 'value'),  # Get the current state of the switch
        Output('start-page', 'children'),
        Output('start-page', 'style'),
        Output('state-manager', 'data'),
     ],
    [
        Input('state-manager', "data"),
        Input('button-sales', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        Input('button-asset', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        Input('button-borrow', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        Input('button-shrink', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        Input('btn-green', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        Input('btn-yellow', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        Input('btn-orange', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        Input('btn-red', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        Input({'type': 'name-bubble', 'index': ALL}, 'n_clicks'),
        Input('okay-button2', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        Input('map', 'clickData'), # If the plot has been clicked
        Input('okay-button', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        Input({'type': 'sector-box', 'index': ALL}, 'n_clicks'), # Selected sectors from the grid
        Input({'type': 'industry-box', 'index': ALL}, 'n_clicks'), # Selected industries from the grid
        Input('large-box-size', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        Input('medium-box-size', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        Input('small-box-size', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        Input('micro-box-size', 'n_clicks'), # n_clicks are needed to identify if a button is clicked 
        Input('next-button', 'n_clicks'), # n_clicks are needed to identify if a button is clicked
        Input('toggle-switch', 'value'),  # Get the current state of the switch
        Input("exploratory-half", "n_clicks"),
        Input("targeted-half", "n_clicks"),
    ]
)
def update_app(stored_data,
               sales_clicks, asset_clicks, borrow_clicks, shrink_clicks, 
               green_btn, yellow_btn, orange_btn, red_btn,
               bubble_clicks, okay_clicks2, 
               click_data, 
               okay_clicks, 
               sector_grid_clicks, industry_grid_clicks,
               large_clicks, medium_clicks, small_clicks, micro_clicks,
               next_clicks,
               toggle_value,
               exploratory_clicks, 
               targeted_clicks
              ):

    global df_global

    SM = StateManager.from_dict(stored_data) if stored_data else StateManager()

    print("-----------")
    print(SM.curr_step)

    # Callback
    ctx = dash.callback_context

    # Nothing triggered = Nothing to be done
    if not ctx.triggered:
        SM.return_init()
        return SM.return_list() + [SM.to_dict()]

    # Define trigger id
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    print(triggered_id)

    # Update toggle values
    SM.toggle_value = toggle_value

    # Initialize extra inputs
    SM.return_init()

    if exploratory_clicks and SM.curr_step == "startPage":

        SM.exploratory_selection()

    elif targeted_clicks and SM.curr_step == "startPage":
        pass

    # If toggle value and reference mismatch, trigger a plot
    elif toggle_value != SM.toggle_reference and SM.curr_step in ["maps1", "maps2", "maps3", "maps4"]:

        SM.toggle_reference = not SM.toggle_reference
        SM.update_geofigure()

    # If we are on the maps step and clicked on the map
    elif SM.curr_step in ["maps1", "maps2", "maps3", "maps4"] and click_data:

        SM.toggle_reset()
        SM.update_geo(click_data)
        SM.update_names(df_global) # Update df_names and the counter value and container
        SM.steps_align()
        SM.update_geofigure()
        

        # Moved on to next graph so make necessary updates
        if SM.step == "sectors":
            SM.fig_style = {'display' : 'none'} # Hide map
            SM.fig = None # Get rid of fig so that less data is carried over
            SM.okay_button = {**OKAY_BUTTON_STYLE, 'display' : 'flex'} # Display okay button 1
            SM.sector_grid_style = {**SECTOR_CONTAINER_STYLE, 'display' : 'grid'} # Define grid & show it
            SM.toggle_card = {'display' : 'none'} # Hide toggle

    # If the current step is sector and the grid was clicked, we update the grid colors to reflect selection
    elif SM.curr_step == "sectors" and "sector-box" in triggered_id:
        clicked_index = json.loads(triggered_id)["index"]
        SM.update_selected_sectors(clicked_index)

    # Handle case when the okay button is clicked and we are on sector grid. Move to ndy grid.
    # Hide the sector grid and display industry grid of industries in the selected sectors
    elif triggered_id == "okay-button" and SM.curr_step == "sectors":

        SM.update_names(df_global)
        SM.updated_selected_industries()
        SM.sector_grid_style = {**SECTOR_CONTAINER_STYLE, 'display' : 'grid'} # Reload grid style
        SM.step = "industries"

    # If current step is industries and the grid was clicked: Updated the grid colors to show selection
    elif SM.curr_step == "industries" and "industry-box" in triggered_id:

        clicked_index = json.loads(triggered_id)["index"]
        SM.updated_selected_industries(clicked_index)

    # Handle case when the okay button is clicked and we are on ndy grid. Move to size page
    # Hide the sector grid and display industry grid of industries in the selected sectors
    elif triggered_id == 'okay-button' and SM.curr_step == "industries":

        SM.update_names(df_global)
        SM.sector_children = [] # Industry grid info dropped
        SM.sector_grid_style = {"display" : 'none'} # Hide sector ndy grid
        SM.step = "size"
        SM.size_matrix_update(BOX_STYLE_FULL, HOVER_STYLE)

    # Handle cases when size boxes are clicked
    elif SM.curr_step == "size" and "-size" in triggered_id:
        SM.selected_size = triggered_id.replace('-box-size', '') # Update selected size
        SM.size_matrix_update(BOX_STYLE_FULL, HOVER_STYLE)

    # Handle cases when okay button is pressed on size page. We move on to name print page
    elif triggered_id == "okay-button" and SM.curr_step == "size":

        SM.update_names(df_global)
        SM.display_print_page()
        SM.selection_print_style = {**PRINT_STYLE} # Display print page
        SM.step = "print"
        SM.selected_status = {i: False for i in SM.df_names}

    # Going beyond print page is displaying the name containers
    elif triggered_id == "okay-button" and SM.curr_step == "print":

        SM.update_name_bubbles(df_global)
        SM.names_bubbles_buttons()
        SM.okay_button2 = {**OKAY_BUTTON_STYLE, 'display': 'flex'} # Display okay button 2
        SM.okay_button = {'display' : 'none'} # Hide okay button 1
        SM.names_container_style = {'textAlign': 'center', 'display': 'flex', 'flexWrap': 'wrap', 
          'justifyContent': 'center', 'margin_top':'15px'}
        SM.selection_print_style = {'display' : 'none'}
        SM.step = "bubbles"

    # Interact with bubble containers
    elif triggered_id.startswith('button-') or triggered_id.startswith('btn-') or 'name-bubble' in triggered_id:

        choice_clicked = triggered_id.split('-')[1].capitalize() # Extract selection
        SM.update_name_bubbles(df_global, choice_clicked, triggered_id)
        SM.names_bubbles_buttons()

    # Handle case when the okay button is clicked: Move to company page and hide the model mode and color category buttons
    elif triggered_id == 'okay-button2':

        SM.initial_company_page(df_global, df_full, model_type_list)
        SM.names_bubbles_buttons(hide = True)
        SM.okay_button2 = {"display":"none"}
        SM.counter_style = {"display":"none"} # Hide counter
        SM.next_button = {**NEXT_BUTTON_STYLE}
        SM.names_container_style = {"display":"none"}

    # If the next button is clicked then we move on to the next company
    elif triggered_id == "next-button":        

        SM.update_company_page(df_global, df_full, model_type_list)

    print("END REACHED")
    # Overall return
    return SM.return_list() + [SM.to_dict()]

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
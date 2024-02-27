'''
Build a Dashboard Application with Plotly Dash
----------------------------------------------
In this lab, you will be building a Plotly Dash 
application for users to perform interactive visual analytics 
on SpaceX launch data in real-time.
'''
import pandas as pd
from dash import dash,dcc,html,Input, Output
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

sites=spacex_df['Launch Site'].unique().tolist()
site_dropdown_options=[]
site_dropdown_options.append({'label': 'All Sites', 'value': 'All'})
for site in sites:
    site_dropdown_options.append({'label': site, 'value': site })

app.layout = html.Div(children=[
    html.Div([
        html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36','font-size': 40}),
    ]),
    
    html.Div([
        # TASK 1: Add a Launch Site Drop-down Input Component
        dcc.Dropdown(
                id = 'site-dropdown',
                options = site_dropdown_options,
                placeholder = 'Select a Launch Site here',
                searchable = True ,
                clearable = False,
                value = 'All'
            ),
        # TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown
        html.Div(dcc.Graph(id='success-pie-chart')),
    ], style={'padding': '0 30px'}),

    html.Div([
        # TASK 3: Add a Range Slider to Select Payload
        html.Div("Payload range (Kg):"),
        html.Div([
            dcc.RangeSlider(
                id = 'payload_slider',
                min = 0,
                max = 10000,
                step = 1000,
                marks = {
                        0: '0',
                        1000: '1000',
                        2000: '2000',
                        3000: '3000',
                        4000: '4000',
                        5000: '5000',
                        6000: '6000',
                        7000: '7000',
                        8000: '8000',
                        9000: '9000',
                        10000: '10000'},
                value = [min_payload,max_payload]
            ),
        ]),

        # TASK 4: Add a callback function to render the success-payload-scatter-chart scatter plot
        html.Div(dcc.Graph(id = 'success-payload-scatter-chart')),
    ]),
],style={'padding': '0 20px'})

# TASK 2: success-pie-chart callback based on selected site dropdown
@app.callback(
     Output(component_id = 'success-pie-chart', component_property = 'figure'),
     [Input(component_id = 'site-dropdown', component_property = 'value')]
)
def update_piegraph(site_dropdown):
    if (site_dropdown == 'All' or site_dropdown == 'None'):
        launch_sites  = spacex_df[spacex_df['class'] == 1] # All Success only for all sites.
        fig = px.pie(
                launch_sites,
                names = 'Launch Site',
                values= 'class',
                title = 'Total Success Launches by All Sites',
            )
    else:
        single_site  = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        fig = px.pie(
                single_site,
                names = 'class',
                title = 'Total Success Launches for Site &#8608; '+site_dropdown,
                hole = .2
            )
    return fig

# TASK 3, 4: Range Slider or Scatter Chart Callback
@app.callback(
     Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
     [Input(component_id = 'site-dropdown', component_property = 'value'), 
     Input(component_id = "payload_slider", component_property = "value")]
)
def update_scattergraph(site_dropdown,payload_slider):
    if (site_dropdown == 'All' or site_dropdown == 'None'):
        low, high = payload_slider
        all_sites  = spacex_df
        loadrange = (all_sites['Payload Mass (kg)'] > low) & (all_sites['Payload Mass (kg)'] < high)
        fig = px.scatter(
                all_sites[loadrange], 
                x = "Payload Mass (kg)", 
                y = "class",
                title = 'Correlation - Payload vs Success - All Sites',
                color="Booster Version Category",
                size='Payload Mass (kg)',
            )
    else:
        low, high = payload_slider
        single_site  = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        loadrange = (single_site['Payload Mass (kg)'] > low) & (single_site['Payload Mass (kg)'] < high)
        fig = px.scatter(
                single_site[loadrange],
                x = "Payload Mass (kg)",
                y = "class",
                title = 'Correlation - Payload vs Success - Site &#8608; '+site_dropdown,
                color="Booster Version Category",
                size='Payload Mass (kg)',
            )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
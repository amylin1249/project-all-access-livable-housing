from pathlib import Path
from dash import Dash, html, dcc, Input, Output
from visualize import create_tract_map, create_scatterplot
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
import sys
import shapefile
import folium
import webbrowser
import geopandas as gpd
import altair as alt
from altair_saver import save
import seaborn as sns
import matplotlib.pyplot as plt
from pyproj import Transformer, CRS
from shapely import geometry
from shapely.ops import transform
import dash_vega_components as dvc
import calendar

from datatypes import (
    MERGED_SF_TRACTS_SHP,
    MERGED
)

my_chart = create_tract_map(
    source_file=MERGED, 
    start_date="2020-01", 
    end_date="2024-12", 
    col_name="eviction_rate", 
    agg="sum"
)

app = Dash(__name__)

app.layout = html.Div([
    html.H1("San Francisco Housing & Eviction Dashboard",style={'textAlign': 'center', 'color': '#2c3e50'}),
    
    # one line in between
    html.Br(),

    # text
    html.Div([
        html.Hr(), # Horizontal line
        html.P("This dashboard visualizes housing conditions and homelessness trends in San Francisco."),
        html.P([
            "Use the ", 
            html.B("dropdown and date inputs below"), 
            " to select the data type and time period. The ", 
            html.B("map"), 
            " will update automatically based on your selection."
        ], style={'fontSize': '16px', 'lineHeight': '1.5'}),
        html.Hr(), # Horizontal line
    ], style={'padding': '10px 40px', 'color': '#34495e'}),

    # data select dropdown
    html.Div([
        html.Label("Select Data:"),
        dcc.Dropdown(
            id='column-dropdown',
            options=[
                {"label": "Homelessness", "value": 'estimate'},
                {"label": "Eviction Rate", "value": 'eviction_rate'},
                {"label": "Median Rent", "value": 'median_rent'},
            ],
            value="estimate"
            
        ),
        # one line in between
        html.Br(), 

        # date select dropdown
        html.Div([
            # Start date
            html.Div([
                html.Label("Start Period:"),
                dcc.Dropdown(
                    id="start-year",
                    options=[{"label": str(y), "value": str(y)} for y in range(2020, 2025)],
                    value="2020",
                    style={"width": "120px", "display": "inline-block"}
                ),
                dcc.Dropdown(
                    id="start-month",
                    options=[{"label": calendar.month_name[m], "value": f"{m:02d}"} for m in range(1, 13)],
                    value='01', 
                    style={'width': '150px', 'display': 'inline-block', 'marginLeft': '10px'}
                ),
            ], style={'display': 'inline-block'}),

            # end date
            html.Div([
                html.Label("End Period:", style={'marginLeft': '30px'}),
                dcc.Dropdown(
                    id='end-year',
                    options=[{'label': str(y), 'value': str(y)} for y in range(2020, 2026)],
                    value='2020',
                    style={'width': '120px', 'display': 'inline-block', 'marginLeft': '10px'}
                ),
                dcc.Dropdown(
                    id="end-month",
                    options=[{"label": calendar.month_name[m], "value": f"{m:02d}"} for m in range(1, 13)],
                    value='02', 
                    style={'width': '150px', 'display': 'inline-block', 'marginLeft': '10px'}
                ),
            ], style={'display': 'inline-block'}),
        ]),
    ], style={'padding': '20px', 'backgroundColor': '#f9f9f9'}),
    
    
    html.Div([
        # left : map
        html.Div([
            dvc.Vega(id='sf-map', spec={})
        ], style={'width': '50%', 'padding': '10px', 'border': '1px solid #ddd', 'borderRadius': '10px'}),
        
        # right : scatter plot
        html.Div([
            html.H3("Scatter Plot", style={'textAlign': 'center', 'color': '#2c3e50'}),
            html.Hr(),
            # Placeholder for scatter
            html.Div(
                id='scatter-plot-placeholder',
                children=[
                    html.P("Scatter Plot is being prepared...", 
                           style={'textAlign': 'center', 'marginTop': '120px', 'color': '#999', 'fontStyle': 'italic'}),
                    html.P("(e.g., Median Rent vs. Eviction Rate)", 
                           style={'textAlign': 'center', 'color': '#ccc', 'fontSize': '12px'})
                ],
                style={
                    'height': '450px', 
                    'backgroundColor': '#fcfcfc', 
                    'border': '2px dashed #3498db',
                    'borderRadius': '10px',
                    'display': 'flex',
                    'flexDirection': 'column',
                    'justifyContent': 'center'
                }
            )
        ], style={'width': '50%', 'padding': '10px', 'marginLeft': '20px'})

    ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'flex-start', 'padding': '20px'})
])


@app.callback(
    [Output("sf-map", 'spec'), # update
     Output("scatter-plot-placeholder", "spec")],
    [Input('column-dropdown', 'value'), # change in column
     Input('start-year', 'value'),
     Input('start-month', 'value'),
     Input('end-year', 'value'),     # change in start-date
     Input('end-month', 'value')]       # change in end-date
)

def update_map(selected_col, start_year, start_month, end_year, end_month):
    """automatically called when the value property of the dropdwon component changes
    """
    start = f"{start_year}-{start_month}-01"
    last_day = calendar.monthrange(int(end_year), int(end_month))[1]
    end= f"{end_year}-{end_month}-{last_day}"

    new_chart = create_tract_map(
        source_file=MERGED, 
        start_date=start, 
        end_date=end, 
        col_name=selected_col, 
        agg="sum"
    )
    empty_scatter = {}
    return new_chart.to_dict(), empty_scatter

if __name__ == "__main__":
    app.run(debug=True)
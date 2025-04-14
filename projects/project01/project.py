# project.py


import pandas as pd
import numpy as np
from pathlib import Path

###
from collections import deque
from shapely.geometry import Point
###

import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
pd.options.plotting.backend = 'plotly'

import geopandas as gpd

import warnings
warnings.filterwarnings("ignore")


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def create_detailed_schedule(schedule, stops, trips, bus_lines):
    # Merge schedule with stops
    merged = schedule.merge(stops, on='stop_id', how='left')
    
    # Merge with trips
    merged = merged.merge(trips, on='trip_id', how='left')
    
    # Filter by bus lines
    merged = merged[merged['route_id'].isin(bus_lines)]
    
    # Sort by route_id (in the order of bus_lines), trip_id, and stop_sequence
    merged['route_id'] = pd.Categorical(merged['route_id'], categories=bus_lines, ordered=True)
    merged = merged.sort_values(['route_id', 'trip_id', 'stop_sequence'])
    
    # Set trip_id as the index
    merged = merged.set_index('trip_id')
    
    return merged

def visualize_bus_network(bus_df):
    # Assign colors to bus lines
    colors = px.colors.qualitative.Plotly
    bus_lines = bus_df['route_id'].unique()
    color_map = {line: colors[i % len(colors)] for i, line in enumerate(bus_lines)}
    
    # Load the shapefile for San Diego city boundary
    san_diego_boundary_path = 'data/data_city/data_city.shp'
    san_diego_city_bounds = gpd.read_file(san_diego_boundary_path).to_crs("EPSG:4326")
    
    fig = go.Figure()
    
    # Add city boundary
    fig.add_trace(go.Choroplethmapbox(
        geojson=san_diego_city_bounds.__geo_interface__,
        locations=san_diego_city_bounds.index,
        z=[1] * len(san_diego_city_bounds),
        colorscale="Greys",
        showscale=False,
        marker_opacity=0.5,
        marker_line_width=1,
    ))
    
    # Add bus stops for each route
    for line in bus_lines:
        route_data = bus_df[bus_df['route_id'] == line]
        fig.add_trace(go.Scattermapbox(
            lat=route_data['stop_lat'],
            lon=route_data['stop_lon'],
            mode='markers',
            marker=dict(size=8, color=color_map[line]),
            name=f"Bus Line {line}",
            text=route_data['stop_name']
        ))
    
    # Update layout
    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            center={"lat": bus_df['stop_lat'].mean(), "lon": bus_df['stop_lon'].mean()},
            zoom=10,
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    
    return fig


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def find_neighbors(station_name, detailed_schedule):
    ...


def bfs(start_station, end_station, detailed_schedule):
    ...


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def simulate_bus_arrivals(tau, seed=12):
    
    np.random.seed(seed) # Random seed -- do not change
    
    ...


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def simulate_wait_times(arrival_times_df, n_passengers):

    ...

def visualize_wait_times(wait_times_df, timestamp):
    ...

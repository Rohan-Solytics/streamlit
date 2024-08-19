import ipyleaflet
from ipywidgets import Layout, widgets, HBox, VBox, Button
from ipyleaflet import Map, GeoJSON, Choropleth, WidgetControl, LegendControl, basemaps, basemap_to_tiles
import json
import pandas as pd
from streamlit.components.v1 import html as st_html
import streamlit as st
# import streamlit.components.v1 as components
# from streamlit_ipywidgets import st_ipywidgets

# Correct path for the uploaded GeoJSON file 
geojson_file_path = 'geojson3/data_2020.geojson'

# Load GeoJSON data
with open(geojson_file_path, 'r') as file: 
    geojson_data = json.load(file)



def on_marker_click(properties,sidebar):
    content = f"""
    <div>
        <h4 style="margin-bottom: 8px; text-align:center; font-weight:bold; font-size: larger;">{properties['Name']}</h4>"
        <div style="text-align:center; font-weight:bold; font-size: large;">{properties['ZIP Code']}</div>"
    
        <table style="width: 100%;">
        <tr>
            <th><b>Year</b></th>
            <th><b>LTV</b></th>
            <th><b>PD</b></th>
            <th><b>PD FR</b></th>
            <th><b>History</b></th>
            <th><b>Decision</b></th>
        </tr>
    """
    for year in ['2020', '2025', '2030', '2035', '2040', '2045', '2050']:
        ltv = f"{float(properties.get(f'LTV {year}', 0)):.3g}"  # Convert to float and format
        pd = f"{float(properties.get(f'PD {year}', 0)):.3g}"  # Convert to float and format
        pd_fr_value = properties.get(f'PD_FR_{year}', '')  # Retrieve PD_FR value
        pd_fr = f"{float(pd_fr_value) if pd_fr_value else 0:.3g}"  # Convert to float and format, or use 0 if not available
        decision = 'Approve' if pd_fr_value and float(pd_fr_value) < 0.5 else 'Deny'  # Check if PD_FR is available and less than 0.5
        content += f"<tr><td>{year}</td><td>{ltv}</td><td>{pd}</td><td>{pd_fr}</td><td>{properties.get('Credit History', '')}</td><td>{decision}</td></tr>"
    content += "</table></div>"
    sidebar.value = content

# Function to create and add a marker to the map
def create_marker(lat, lon, properties,m,sidebar):
    
    if lat is not None and lon is not None:
        marker=ipyleaflet.Marker(location=(lat, lon), draggable=False)
        marker.properties = properties
        # print(marker.properties)
        # Correctly define the handle_click function to accept any additional keyword arguments 
        def handle_click(*args, **kwargs):
            on_marker_click(marker.properties,sidebar)
        
        #Assign the event handler to the marker
        marker.on_click(handle_click)
        m.add_layer(marker)
        pass



#Function to determine color based on urban flood susceptibilit 
def get_color(value):
    """Returns a color based on urban flood susceptibility."""
    if value is None:
        return '#999999' # Gray for undefined values
    elif value < 8.0:
        return '#c6dbef'
    elif value < 8.2:
        return '#9ecae1'
    elif value < 8.4:
        return '#6baed6'
    elif value < 8.6: 
        return '#4292c6' 
    elif value < 8.8:
        return '#217165' 
    elif value < 9.0:
        return '#08519c'
    elif value < 9.1:
        return '#084594'
    elif value < 9.2:
        return '#083066'
    elif value < 9.3:
        return '#872457'
    elif value < 9.4:
        return '#061844'
    elif value < 9.5:
        return '#051031'
    elif value < 9.6:
        return '#04081e'
    elif value < 9.7:
        return '#03060b'
    elif value <9.8:
        return '#020404'
    elif value <9.9:
        return '#010203'
    else: # For 9.9 to 10.0
        return '#000102'

# Style callback function to style features dynamically
def style_function(feature):
    suscep = feature['properties'].get('urban_flood_suscep', None) 
    return {
    'fillColor': get_color(suscep),
    'color': 'black', # Border color
    'weight': 0.1,
    'fillopacity': 0.6
    }

def flood_predictions(properties_df): # import from risk_visuls file-----------
    
    # Define the center of the map (Chicago's latitude and longitude)
    chicago_center = [41.8781, -87.6298]

    # Define the initial zoom level
    initial_zoom_level = 11

    # Create a Folium map centered on Chicago with a zoom lock
    m = ipyleaflet.Map(
        center=tuple(chicago_center), 
        zoom=initial_zoom_level,  # Use the initial zoom level
        layout = Layout(height='800px'))
    
    sidebar = widgets.HTML(value="Click a property to begin.", layout=Layout(width='330px', height='100%', overflow='auto'))
    
    # Iterate over the DataFrame to create and add markers
    for index, row in properties_df.iterrows():
        # print('row: ', row)
        create_marker(row["latitude"], row["longitude"], row.to_dict(),m, sidebar)
    
    
    nominatim_geocoding_url = 'https://nominatim.openstreetmap.org/search'

    
    # Create a GeoJSON layer with dynamic styling 
    geojson_layer = GeoJSON(
        data=geojson_data,
        style_callback=style_function
    )

    # Add the GeoJSON Layer to the map
    m.add_layer(geojson_layer)

    # HBox Layout is adjusted to accommodate the map's new height.
    hbox_layout= Layout(display='flex', flex_flow="row", height='800px', align_items='stretch') # Match the height with the map height 
    hbox = HBox([sidebar, m], layout=hbox_layout)
    
    st_html(m, height=500, width=500)


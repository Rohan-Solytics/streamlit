import os
from datetime import datetime
import streamlit as st
import pandas as pd
import geopandas as gpd
from folium.plugins import TimestampedGeoJson
import folium
from branca.colormap import linear
from shapely.geometry import mapping
import matplotlib.cm as cm


from artifacts import properties_df, geojson_directory

def create_timestamped_geojson_map(geojson_directory, properties_df):
    # Combine features for all years into a single list
    all_features = []

    # Define the center of the map (Chicago's latitude and longitude)
    chicago_center = [41.8781, -87.6298]

    # Define the initial zoom level
    initial_zoom_level = 11

    # print(properties_df)

    # Create a Folium map centered on Chicago with a zoom lock
    m = folium.Map(
        location=chicago_center, 
        zoom_start=initial_zoom_level,  # Use the initial zoom level
        tiles='OpenStreetMap', 
        attr='Map data © OpenStreetMap contributors',
        min_zoom=initial_zoom_level  # Lock the zoom level to prevent zooming out further
    )

    # Iterate over each GeoJSON file in the directory
    for file_name in os.listdir(geojson_directory):
        if file_name.endswith('.geojson'):
            file_path = os.path.join(geojson_directory, file_name)

            # Extract the year from the file name (assuming it follows a specific format)
            year = int(file_name.split('_')[1].split('.')[0])  # Convert the year to an integer

            # Read the GeoJSON file
            geojson_data = gpd.read_file(file_path)

            # Convert the year to a datetime object
            timestamp = datetime(year, 1, 1)

            # Define color scale based on the filtered data
            linear_scale = linear.Blues_09.scale(
                geojson_data['urban_flood_suscep'].min(),
                geojson_data['urban_flood_suscep'].max()
            )

            # Convert GeoJSON to a list of features for the current year
            features = []
            for _, row in geojson_data.iterrows():
                feature = {
                    'type': 'Feature',
                    'geometry': mapping(row['geometry']),
                    'properties': {
                        'time': timestamp.strftime('%Y-%m-%d'),  # Use a different format for the period
                        'tooltip': f"<b>Community Name:</b> {row['community']}<br/><b>Urban Flood Susceptibility:</b> {row['urban_flood_suscep']}",
                        'style': {
                            'color': linear_scale(row['urban_flood_suscep']) if pd.notnull(row['urban_flood_suscep']) else '#ffffff00',
                            'weight': 0.5,
                            'fillOpacity': 1 if pd.notnull(row['urban_flood_suscep']) else 0,
                        }
                    }
                }
                features.append(feature)

            # Add the features to the all_features list
            all_features.extend(features)

    # Add the TimestampedGeoJson layer for all years
    TimestampedGeoJson(
        {'type': 'FeatureCollection', 'features': all_features},
        period='P5Y',  # Specify the time interval (adjust as needed)
        add_last_point=False,
        auto_play=False,
        loop=False,
        max_speed=1,
        loop_button=True,
        date_options='YYYY',
        time_slider_drag_update=True,
    ).add_to(m)

    # Add color scale to map
    linear_scale.add_to(m)

    for index, row in properties_df.iterrows():
        if not pd.isna(row['latitude']) and not pd.isna(row['longitude']):
            # Extract LTV and PD values and corresponding years
            ltv_years = ['LTV 2020', 'LTV 2025', 'LTV 2030', 'LTV 2035', 'LTV 2040', 'LTV 2045', 'LTV 2050']
            pd_years = ['PD 2020', 'PD 2025', 'PD 2030', 'PD 2035', 'PD 2040', 'PD 2045', 'PD 2050']
            pdfr_years = ['PD_FR_2020', 'PD_FR_2025', 'PD_FR_2030', 'PD_FR_2035', 'PD_FR_2040', 'PD_FR_2045', 'PD_FR_2050']
            
            ltv_values = [f"{row[year]:.3g}" for year in ltv_years]  # Format to 3 significant figures
            pd_values = [f"{row[year]:.3g}" for year in pd_years]
            pdfr_values = [f"{row[year]:.3g}" for year in pdfr_years]    # Format to 3 significant figures
            credit_history = row['Credit History']

            # pd_fr = f"{float(pd_fr_value) if pd_fr_value else 0:.3g}"  # Convert to float and format, or use 0 if not available
            
            # pd_binary is now processed inside the loop for adding rows

            html_content = f"""
            <div>
                <h4 style="margin-bottom: 8px; text-align:center; font-weight:bold; font-size: larger;">{row['Name']}</h4>
                <div style="text-align:center; font-weight:bold; font-size: large;">{row['ZIP Code']}</div>
            
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

            # Add rows for LTV, PD values, credit history, and PD binary for each year
            for year, ltv, pd_value,pdfr_value in zip(ltv_years, ltv_values, pd_values,pdfr_values):
                # Process pd_binary for each row
                decision,color = ('Approve','green') if pdfr_value and float(pdfr_value) < 0.6 else ('Deny','red')  # Check if PD_FR is available and less than 0.5
            
                # pd_display, pd_color = ('YES', 'green') if  == 1 else ('NO', 'red')
                html_content += f"<tr><td><strong>{year[-4:]}</strong></td><td style='text-align: center;'>{ltv}</td><td style='text-align: center;'>{pd_value}</td><td style='text-align: center;'>{pdfr_value}</td><td style='text-align: center;'>{credit_history}</td><td style='text-align: center; color: {color};'>{decision}</td></tr>"

            # Close the table and div tags after appending all rows
            html_content += """
                </table>
            </div>"""
            # fol_df = pd.read_html(html_content)
            # Create and add the popup to the marker
            popup = folium.Popup(html_content, max_width=300)
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=popup,
                icon=folium.Icon(color='blue', icon='home')
            ).add_to(m)

    return m

def app():

    st.markdown(
                    """
                    <div style='background-color: #AECDFC; border-radius: 5px; padding: 1px;'>
                        <h1 style='text-align: center; font-size: 28px; color: black;'>Hazard Risk Visualization Map</h1>
                    </div>
                    <p></p>
                    """,
                    unsafe_allow_html=True)
    folium_map = create_timestamped_geojson_map(geojson_directory, properties_df)
    st.components.v1.html(folium_map._repr_html_(), width=850, height=700)

if __name__ == "__main__":
    app()

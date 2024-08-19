import streamlit as st
import json
import pandas as pd
import base64
from get_locations_properties import get_lat_long

from artifacts import map_data, portfolio_data

# Custom CSS style for the container and table header
custom_css = """
<style>
    .custom-container {
        max-height: 400px;
        overflow-y: scroll;
        position: relative;
        border-radius: 10px;
        border: 1px solid #ccc;
        margin: 0 auto; /* Center the container horizontally */
        width: 80%; /* Adjust the width of the container */
        margin-right: 10%; /* Push the container slightly to the right */
    }

    th, td {
        font-size: 14px;
        padding: 8px; /* Add padding for better readability */
        text-align: left; /* Align text to the left */
    }
    .download-button {
        position: absolute;
        top: -10px;
        right:90px;
        font-size: 18px;
    }
    thead {
        position: sticky;
        top: 0;
        background-color: #005f69;
        color: white;
    }
</style>
"""
custom_css1 = """
<style>
    .custom-container {
        max-height: 400px;
        overflow-y: scroll;
        position: relative;
        border-radius: 10px;
        border: 1px solid #ccc;
    }

    th, td {
        font-size: 14px;
        padding: 8px; /* Add padding for better readability */
        text-align: left; /* Align text to the left */
    }
    .download-button {
        position: absolute;
        top: -10px;
        right:10px;
        font-size: 18px;
    }
    thead {
        position: sticky;
        top: 0;
        background-color: #005f69;
        color: white;
    }
</style>
"""

def app():

    st.markdown(
                    """
                    <div style='background-color: #AECDFC; border-radius: 5px; padding: 1px;'>
                        <h1 style='text-align: center; font-size: 28px; color: black;'>Data Sources</h1>
                    </div>

                    <p></p>
                    <p></p>
                    
                    """,
                    unsafe_allow_html=True)
    
    with st.expander("Please select the information"):
        selected_city = st.selectbox('Select City', ['Chicago'], placeholder='Select City',index=None)

        if selected_city == 'Chicago':
            selected_data = st.selectbox('Select Data Source', ['Portfolio Data','Map Data'], placeholder='Select Data',index=None)
            
            if selected_data == 'Portfolio Data':
                # Inject custom CSS into the Streamlit app
                st.markdown(custom_css1, unsafe_allow_html=True)
                

                # Rename the index column to "Row_Id"
                portfolio_data.index.name = "Row_Id"

                # Create HTML table with custom header row
                html_table = f'<div class="custom-container"><table class="dataframe">'
                html_table += '<thead><tr>'
                html_table += '<th>Row_Id</th>'  # Add the custom index column header
                for col_name in portfolio_data.columns:
                    html_table += f'<th>{col_name}</th>'
                html_table += '</tr></thead>'

                # Add table rows with concatenated values
                for _, row in portfolio_data.iterrows():
                    html_table += '<tr>'
                    html_table += f'<td>{row.name}</td>'  # Display the index name
                    for col_value in row.values:
                        html_table += f'<td>{col_value}</td>'
                    html_table += '</tr>'

                html_table += '</table></div>'

                # Add a download button with a custom download icon in a square box
                st.markdown('<div class="download-button"><a href="data:file/csv;base64,{}" download="table.csv">⬇️</a></div>'.format(
                    base64.b64encode(portfolio_data.to_csv(index=True, encoding='utf-8').encode()).decode()),
                    unsafe_allow_html=True
                )
                st.markdown(html_table, unsafe_allow_html=True)
                # st.dataframe(portfolio_data)

            elif selected_data == 'Map Data':
                map_df = map_data[['Name','ZIP Code','latitude','longitude']]

                # Inject custom CSS into the Streamlit app
                st.markdown(custom_css, unsafe_allow_html=True)
                

                # Rename the index column to "Row_Id"
                map_df.index.name = "Row_Id"

                # Create HTML table with custom header row
                html_table = f'<div class="custom-container"><table class="dataframe">'
                html_table += '<thead><tr>'
                html_table += '<th>Row_Id</th>'  # Add the custom index column header
                for col_name in map_df.columns:
                    html_table += f'<th>{col_name}</th>'
                html_table += '</tr></thead>'

                # Add table rows with concatenated values
                for _, row in map_df.iterrows():
                    html_table += '<tr>'
                    html_table += f'<td>{row.name}</td>'  # Display the index name
                    for col_value in row.values:
                        html_table += f'<td>{col_value}</td>'
                    html_table += '</tr>'

                html_table += '</table></div>'

                # Add a download button with a custom download icon in a square box
                st.markdown('<div class="download-button"><a href="data:file/csv;base64,{}" download="table.csv">⬇️</a></div>'.format(
                    base64.b64encode(map_df.to_csv(index=True, encoding='utf-8').encode()).decode()),
                    unsafe_allow_html=True
                )
                st.markdown(html_table, unsafe_allow_html=True)
                #st.dataframe(map_df)
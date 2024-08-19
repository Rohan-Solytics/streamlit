import streamlit as st
from synthetic_pd import synthetic_pd_calc, synthetic_pd_flood_calc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from create_pred_df import create_predictions_data
import base64

from artifacts import chicago_properties

# Custom CSS style for the container and table header
custom_css = """
<style>
    .custom-container {
        margin: 0 auto; /* Center the container horizontally */
        width: 80%; /* Adjust the width of the container */
        margin-right: -5%; /* Push the container slightly to the right */
    }
    th, td {
        font-size: 14px;
        padding: 8px; /* Add padding for better readability */
        text-align: left; /* Align text to the left */
    }
    .download-button {
        position: absolute;
        top: -10px;
        right: 200px;
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


data = chicago_properties

# pdmodel_df = pd.read_csv('predicted_pd.csv')

def select_company(name_key,dt):
    selected_property = st.selectbox(name_key, dt['Name'].unique().tolist(), placeholder='Select Property from Portfolio',index=None)

    prop_df = dt[dt['Name'] == selected_property]

    return selected_property,prop_df

def app():
    st.markdown(
                    """
                    <div style='background-color: #AECDFC; border-radius: 5px; padding: 1px;'>
                        <h1 style='text-align: center; font-size: 28px; color: black;'>Model Estimation</h1>
                    </div>
                    <p></p>
                    """,
                    unsafe_allow_html=True)
    
    with st.expander("Probability of Default Calculation for Properties"):
        # st.info('Probability of Default Calculation for Properties')
        model_index = st.selectbox('Select Model', ['LogisticRegression'], placeholder='Model name', index=None)
        tech_index = st.selectbox('Select Preprocessing technique', ['OneHotEncoder'], placeholder='Select preprocessing technique', index=None)
        
        if model_index == 'LogisticRegression' and tech_index == 'OneHotEncoder':

            pd_model = st.selectbox('Select matrix',['Predictions'], placeholder='matrix to display', index=None)    
            if pd_model == 'Predictions':
                    pd_data = data[['Name','ZIP Code','LTV 2020','LTV 2025','LTV 2030','LTV 2035','LTV 2040','LTV 2045','LTV 2050','PTI','PD','Credit History','Borrower']]
                    df = synthetic_pd_calc(pd_data)
                    # st.info('PD Predictions Table')
                    key = 'Select Property'
                    prop_name, prop_df = select_company(key,df)

                    if prop_name is None:
                        pass
                    else:

                        st.write(f"ZIP Code for {prop_name}: {int(prop_df['ZIP Code'])}")

                        df = create_predictions_data(prop_name,prop_df, hz='pd_model')

                        # Inject custom CSS into the Streamlit app
                        st.markdown(custom_css, unsafe_allow_html=True)
                        

                        # Rename the index column to "Row_Id"
                        df.index.name = "Row_Id"

                        # Create HTML table with custom header row
                        html_table = f'<div class="custom-container"><table class="dataframe">'
                        html_table += '<thead><tr>'
                        html_table += '<th>Row_Id</th>'  # Add the custom index column header
                        for col_name in df.columns:
                            html_table += f'<th>{col_name}</th>'
                        html_table += '</tr></thead>'

                        # Add table rows with concatenated values
                        for _, row in df.iterrows():
                            html_table += '<tr>'
                            html_table += f'<td>{row.name}</td>'  # Display the index name
                            for col_value in row.values:
                                html_table += f'<td>{col_value}</td>'
                            html_table += '</tr>'

                        html_table += '</table></div>'

                        # Add a download button with a custom download icon in a square box
                        st.markdown('<div class="download-button"><a href="data:file/csv;base64,{}" download="table.csv">⬇️</a></div>'.format(
                            base64.b64encode(df.to_csv(index=True, encoding='utf-8').encode()).decode()),
                            unsafe_allow_html=True
                        )
                        st.markdown(html_table, unsafe_allow_html=True)
                        #st.dataframe(df)
        
            risk_hazard = st.selectbox('Select Risk Hazard',['Flood risk'], placeholder='Risk hazard name', index=None)
            if risk_hazard == 'Flood risk':
                    pd_flooddata = data[['Name','ZIP Code','LTV 2020','LTV 2025','LTV 2030','LTV 2035','LTV 2040','LTV 2045','LTV 2050','PTI','PD','Credit History','Borrower','flood_risk']]
                    flood_df = synthetic_pd_flood_calc(pd_flooddata)
                    # st.info('PD Predictions Table')
                    key = 'Select Flood Property'
                    prop_name, prop_df = select_company(key,flood_df)

                    if prop_name is None:
                        pass
                    else:

                        st.write(f"ZIP Code for {prop_name}: {int(prop_df['ZIP Code'])}")

                        df = create_predictions_data(prop_name,prop_df, hz='flood')

                                                # Inject custom CSS into the Streamlit app
                        st.markdown(custom_css, unsafe_allow_html=True)
                        

                        # Rename the index column to "Row_Id"
                        df.index.name = "Row_Id"

                        # Create HTML table with custom header row
                        html_table = f'<div class="custom-container"><table class="dataframe">'
                        html_table += '<thead><tr>'
                        html_table += '<th>Row_Id</th>'  # Add the custom index column header
                        for col_name in df.columns:
                            html_table += f'<th>{col_name}</th>'
                        html_table += '</tr></thead>'

                        # Add table rows with concatenated values
                        for _, row in df.iterrows():
                            html_table += '<tr>'
                            html_table += f'<td>{row.name}</td>'  # Display the index name
                            for col_value in row.values:
                                html_table += f'<td>{col_value}</td>'
                            html_table += '</tr>'

                        html_table += '</table></div>'

                        # Add a download button with a custom download icon in a square box
                        st.markdown('<div class="download-button"><a href="data:file/csv;base64,{}" download="table.csv">⬇️</a></div>'.format(
                            base64.b64encode(df.to_csv(index=True, encoding='utf-8').encode()).decode()),
                            unsafe_allow_html=True
                        )
                        st.markdown(html_table, unsafe_allow_html=True)
                        #st.dataframe(df)

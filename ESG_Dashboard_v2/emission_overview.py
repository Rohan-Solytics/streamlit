import streamlit as st
import pandas as pd
from data_display import display_sector

df4 = pd.read_csv('esg_data/co2_comps.csv')
def app():
    container = st.container()

    # Centered text in the floating container
    with container:
        
        st.markdown(
            """
            <div style="text-align: center;">
                <h2>Emission Forecasting Dashboard</h2>
            </div>

            <div style="text-align: justify;">
            <p>The Emission Forecasting dashboard is mainly used for analytics of carbon emission data by organizations and forecasting their future emissions,
                which help us to know the wealth of organization based on its performance.
            </p>
            </div>
            """,

            unsafe_allow_html=True
        )

        st.image('images/dash_2.jpg', use_column_width=True)
        # col1, col2  = st.columns(2)

        # with col1:
        #     st.image('data.png',use_column_width=True)
            
        # with col1:
        #     # index='sectors_Bar_visual'
        #     st.image('sect_bar.png',use_column_width=True)

        # with col2:
        #     st.image('newplot.png',use_column_width=True)


        # with col2:
        #     pass

        

        # # Display image below the text
        
        # st.markdown(
        #     """
        #     <div style="text-align: justify;">
        #     <p>

        #         Created by Solytics partners: https://www.solytics-partners.com/

        #         Codes for refrence : https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

        #     </p>
        #     </div>
        #     """,

        #     unsafe_allow_html=True
        # )

import streamlit as st
import pandas as pd
from est_model import est_model, select_company, scen_func
from action_scenarios import action_scenarios
from ifrs_metrics import predict_data_prep
from prediction_slope import PredSlope

from data_import import df4

def app():
    container = st.container()

    # Centered text in the floating container
    with container:
        st.markdown("<h1 style='text-align: left; color: red; font-size:30px'>Report Emissions for Organizations</h1>", unsafe_allow_html=True)
    
        
        name = 'Select company to display Sustainability report'
        company, comp_df = select_company(name, df4)

        if company is None:
            pass
        else:
            new_df = comp_df.reset_index(drop=True)
            st.dataframe(new_df)
            col1,col2 = st.columns(2)
            with col1:
                model_frame, net_zero_frame = est_model(comp_df,company)
                final_data_df = predict_data_prep(model_frame, net_zero_frame)
                obj = PredSlope(final_data_df)
                fig = obj.main()
                st.plotly_chart(fig, use_container_width=True,theme="streamlit")

            with col2:

                model_frame, net_zero_frame = est_model(comp_df,company)
                final_data_df = predict_data_prep(model_frame, net_zero_frame)
                selected_region = st.selectbox('Select region of Scenario', ['UK','USA'], placeholder='Select region',index=None)
                if selected_region == 'UK':
                    scen_df = scen_func(final_data_df)
                    fig = action_scenarios(scen_df)
                    st.plotly_chart(fig, use_container_width=True)
                
                elif selected_region == 'USA':
                    st.info('Tax data not uploaded for USA region')
                
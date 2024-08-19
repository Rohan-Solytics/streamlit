import streamlit as st
from est_model import est_model, select_company, scen_func
from action_scenarios import action_scenarios
from emission_plots import PlotDF
import pandas as pd
from data_import import df4


def predict_data_prep(model_frame,net_zero_frame):
    slope_df = pd.merge(model_frame,net_zero_frame, on='company_name',how='left')
    filter_companies = slope_df.groupby(['company_name','net_zero_pledge_year'],as_index=False).agg({'net_zero_pledge_year':'first'})
    final_data_df = pd.DataFrame()
    create_data = []
    for i,row in filter_companies.iterrows():
        
        co = row['company_name']
        filt_df = slope_df[slope_df['company_name'] == co]
        df_index = filt_df.index[filt_df['Flag']=='Meet'][0]
        new_df = filt_df.loc[:df_index]
        new_df['yearly_sum'][df_index] = 0
        # new_df['pred_yr_to_meet'] = new_df['year'].where(new_df['Flag']=='Meet',new_df['year'].tolist()[-1])
        create_data.append(new_df)

    final_data_df = pd.concat(create_data, ignore_index=True)
    return final_data_df

def app():
    st.markdown("<h1 style='text-align: left; color: red; font-size:30px'>Emission Intensity and Scenario Analysis</h1>", unsafe_allow_html=True)
    
    emit_tab,price_tab = st.tabs(['Emission Intensity', 'Carbon Tax'])
 
    with emit_tab:
        key1 = f""" Display Emission Intensity Analysis."""
        # st.info(key1)
        name = 'Select Company to display emission intensity'
        company,comp_df = select_company(name,df4)
        if company is None:
            pass
        else:
            model_frame, net_zero_frame = est_model(comp_df,company)
            est_df = model_frame[model_frame['Data_path']=='Inherent']
            emission_intensity = pd.merge(est_df,net_zero_frame, on='company_name',how='left')
            emission_intensity['emissions_per_mil_revenue'] = emission_intensity.apply(lambda x: x['yearly_sum']/x['revenue__mil_$'], axis=1)
            
            obj = PlotDF(emission_intensity,'scatterline')
            fig = obj.main()
            st.plotly_chart(fig,use_container_width=True)


    with price_tab:
        name='Select Company for Analysing Action Scenario'
        company,comp_df = select_company(name,df4)
        if company is None:
            pass
        else:
            model_frame, net_zero_frame = est_model(comp_df,company)
            final_data_df = predict_data_prep(model_frame, net_zero_frame)
            selected_region = st.selectbox('Select region of Scenario', ['UK','USA'], placeholder='Select region',index=None)
            if selected_region == 'UK':
                scen_df = scen_func(final_data_df)
                fig = action_scenarios(scen_df)
                st.plotly_chart(fig, use_container_width=True)
            
            elif selected_region == 'USA':
                st.info('Tax data not uploaded for USA region')
        
         
    
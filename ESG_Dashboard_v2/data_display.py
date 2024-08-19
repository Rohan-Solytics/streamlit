import streamlit as st
import pandas as pd
from est_model import est_model
from scope_percent import PcPlot, percentile_calc
import plotly.graph_objects as go
from emission_sources_stack import PlotSources
from prediction_slope import PredSlope
from emission_plots import PlotDF
import numpy as np
import os
from scipy.stats import percentileofscore
from data_import import df1,df2,df3,df4


def select_company(name_key,data):
    selected_company = st.selectbox(name_key, data['company_name'].unique(), placeholder='Select Company',index=None)

    comp_df = data[data['company_name'] == selected_company]

    return selected_company,comp_df


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
        # new_df['pred_yr_to_meet'] = new_df['year'].where(new_df['Flag']=='Meet',new_df['year'].tolist()[-1])
        create_data.append(new_df)

    final_data_df = pd.concat(create_data, ignore_index=True)
    return final_data_df

def display_sector(data,index):
        # st.markdown("<h1 style='text-align: left; color: red; font-size:30px'>Step 2: sector Wise Emission</h1>", unsafe_allow_html=True)
        # st.markdown("<h1 style='text-align: left; color: black; font-size:15px'>Emission Analysis for each sector</h1>", unsafe_allow_html=True)
        ['Sector emissions','Sectors_bar_visuals','Sectors_scope_pie_visuals','Sector_percentile_visuals','Sector_emission_sources','Companies_scope_pie_visuals','Companies_emission_distribution_visuals','Companies_emission_predictions','Companies_Rank transition probability']
        sector_emission = data.groupby('sector',as_index=False)['yearly_sum'].sum()
        # selected_key = st.selectbox('Select Company Name', model_data.keys())
        # filter_df = model_data[selected_key]
        if index == 'Sector_emissions':
            st.write(sector_emission)

        if index == 'Sectors_bar_visuals':
            fig = go.Figure(data=[go.Bar(
            x= sector_emission['sector'],
            y= sector_emission['yearly_sum'],
            hovertext= sector_emission['yearly_sum'],  # Text to display on hover
            marker_color='rgb(55, 83, 109)'  # Color of the bars
            )])

            # Update layout for better visualization
            fig.update_layout(
                title='Bar plot shows sectors and their emission values',
                xaxis=dict(title='sectors'),  # Label for x-axis
                yaxis=dict(title='Total Emission'),      # Label for y-axis
                plot_bgcolor='rgb(230, 230, 230)',  # Background color of the plot
                width = 800,
                height = 500,
            )
            st.plotly_chart(fig,use_container_width=True)
        
        if index == 'Sectors_scope_pie_visuals':
            sc_df = data.groupby(['sector'],as_index=False).agg({'yearly_sum':'sum','s1':'sum','s2':'sum','s3':'sum'})
        
            pc_obj = PcPlot(sc_df, 'sector')
            fig_ = pc_obj.main()
            st.plotly_chart(fig_,use_container_width=True)
        
        if index == 'Companies_scope_pie_visuals':
            c_df = data.groupby(['sector','company_name'],as_index=False).agg({'yearly_sum':'sum','s1':'sum','s2':'sum','s3':'sum'})
            pc_obj1 = PcPlot(c_df, 'company_name')
            fig_1 = pc_obj1.main()
            st.plotly_chart(fig_1,use_container_width=True)
       
        
        if index == 'Sector_percentile_visuals':
        

            fig_2 = percentile_calc(data)
            st.plotly_chart(fig_2,use_container_width=True)

        if index == 'Sector_emission_sources':
            selected_sector = st.selectbox('Select sector Name', data['sector'].unique().tolist())

            emit_src_ef = data[data['sector'] == selected_sector]
        
            plotobj = PlotSources(emit_src_ef)
            fig_3 = plotobj.main()
            st.plotly_chart(fig_3,use_container_width=True)
        
        if index ==  'Companies_emission_distribution_visuals':
            name = 'Select Company for Emission Distribution'
            company,comp_df = select_company(name,df4)
            if company is None:
                pass
            else:
                model_frame, net_zero_frame = est_model(comp_df,company)
                model_df = pd.merge(model_frame,net_zero_frame, on='company_name',how='left')
                
                snerario_pie_df = model_df[model_df['Data_path']=='Inherent']
            
                st.write(snerario_pie_df)
                obj = PlotDF(snerario_pie_df,'pie')
                fig = obj.main()
                st.plotly_chart(fig, use_container_width=True)

        if index == 'Companies_emission_predictions':
            name='Select Company for Analysing Prediction Slope'
            company,comp_df = select_company(name,df4)
            if company is None:
                pass
            else:
            
                model_frame, net_zero_frame = est_model(comp_df,company)
                final_data_df = predict_data_prep(model_frame, net_zero_frame)
                obj = PredSlope(final_data_df)
                fig = obj.main()
                st.plotly_chart(fig, use_container_width=True,theme="streamlit")

        if index == 'Companies_Rank transition probability':
            rank_pivot = pd.pivot_table(data=df4,index=['company_name'], columns='year',values='yearly_sum', aggfunc='sum').reset_index()
            rank_pivot.columns = ['company_name','Sum_2016','Sum_2017','Sum_2018','Sum_2019','Sum_2021','Sum_2022']
            colmns = [col for col in rank_pivot.columns if col.startswith('Sum')]
            for col in colmns:
                ele = col.split('_')[-1]
                percentile_scores = rank_pivot[col].apply(lambda x: np.maximum(np.ceil(percentileofscore(rank_pivot[col],x)/10),1))
                rank_pivot[ele+'_rank'] = percentile_scores
            
            selected_company = st.selectbox('Select Company to display Transition Probability', rank_pivot['company_name'].tolist(), index=None)
            if selected_company is None:
                pass
            else:
                rank_df = rank_pivot[rank_pivot['company_name'] == selected_company]
                st.write(rank_df)
                obj = PlotDF(rank_df,'matrix')
                fig = obj.main()
                st.plotly_chart(fig, use_container_width=True)

def app():


    st.markdown("<h1 style='text-align: left; color: red; font-size:30px'>Emission Data Analysis</h1>", unsafe_allow_html=True)
    
    key1_tab,key2_tab,key3_tab = st.tabs(['Actual Data', 'Forecasted Data', 'Analytics'])
 
    with key1_tab:
        
        index = st.selectbox("Let's Explore the Data", ['Carbon Emission Data','Organization Data', 'Portfolio Data','Model Data'], placeholder="Select data to display",index=None)
     
        if index == 'Carbon Emission Data':
        
            key1 = f""" Display Carbon Emission's data."""
            st.dataframe(df1)
        
        if index == 'Organization Data':
        
            key2 = f""" Display Organization's data."""
            st.dataframe(df2)
        
        if index == 'Portfolio Data':

            key3 = f""" Display Portfolio's data."""
            st.dataframe(df3)
        
        if index == 'Model Data':

            key4 = f""" Display Model's data."""
            st.dataframe(df4)

    with key2_tab:
        # st.info("Display Forecasted data")
        est_key =  f""" Display Forecasted data."""
        name = 'Company Name'
        company,comp_df = select_company(name,df4)

        if company is None:
            pass
        else:
            model_frame, net_zero_frame = est_model(comp_df,company)
            st.dataframe(model_frame)    

    with key3_tab:
        # st.info("Display Carbon Footprint")
        index = st.selectbox('Select emission matrix',['Sector_emissions','Sectors_bar_visuals','Sectors_scope_pie_visuals','Sector_percentile_visuals','Sector_emission_sources','Companies_scope_pie_visuals','Companies_emission_distribution_visuals','Companies_emission_predictions','Companies_Rank transition probability'], index=None, placeholder='Analysis to do...')
        
        display_sector(df4,index)

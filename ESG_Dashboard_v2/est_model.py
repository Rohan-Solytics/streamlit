import pandas as pd
from statsmodels.tsa.holtwinters import Holt
import streamlit as st
import numpy as np

def meet_net_zero(diff,flg):

        if diff >= 0 and flg == 'Meet':
            return 'Yes'
        else:
            return 'No'

def meet_pred_yr(yr,flg):
    if flg == 'Meet':
        return yr

def forecasting(data):
    holt_model = Holt(data)
    holt_fit = holt_model.fit()

    # Forecast the next 21 values
    forecast_values = holt_fit.forecast(steps=80)
    return forecast_values

def select_company(name_key,data):
    selected_company = st.selectbox(name_key, data['company_name'].unique().tolist(), placeholder='Select Company',index=None)

    comp_df = data[data['company_name'] == selected_company]

    return selected_company,comp_df


def scen_func(main_df):
    main_df['early_action'] = list(np.ceil(np.linspace(30,900,len(main_df['year']))).astype(int))

    main_df['early_carbon_tax'] = main_df['yearly_sum'] * main_df['early_action']
    
    action_upto_2030 = main_df.loc[main_df['year']<2031]
    action_after_2030 = main_df.loc[main_df['year']>=2031]
    action_upto_2030['late_action'] = 0
    action_after_2030['late_action'] = list(np.ceil(np.linspace(30,1100,len(action_after_2030['year']))).astype(int))

    late_act_df = pd.concat([action_upto_2030,action_after_2030], axis=0)
    main_df['late_action'] = late_act_df['late_action']
    main_df['late_action_carbon_tax'] = main_df['yearly_sum'] * main_df['late_action']
    main_df['no_add_action_carbon_tax'] = 30 * main_df['yearly_sum']
    

    return main_df
    # main_df[['company_name','year','net_zero_pledge_year','yearly_sum','Data_path','Flag','early_action','early_carbon_tax','late_action','late_action_carbon_tax']].to_excel('early_late_action.xlsx',index=False)
# def scen_func(main_df):
#     new_df = {}
#     j = 12
#     for i in main_df['yearly_sum'].tolist():
#         x = 30 * i
#         y = 30 * j
        
#         if 'early_action' not in new_df:
#             new_df['early_action'] = []
#         if 'late_action' not in new_df:
#             new_df['late_action'] = []

#         if 'no_add_action' not in new_df:
#             new_df['no_add_action'] = []

#         if i > 2030:
#             new_df['late_action'].append(y)
#             j += 1
#         else:
#             new_df['late_action'].append(30)
            
#         new_df['early_action'].append(x)
#         new_df['no_add_action'].append(30)

#     scenario_df = pd.concat([main_df,pd.DataFrame(new_df)], axis=1)
#     return scenario_df

def est_model(comp_df,selected_company):
        # comp_years = co2_comps.groupby(['company_name','net_zero_pledge_year'], as_index=False).agg({'net_zero_pledge_year':'first'})

        # comp_years = co2_comps.drop(co2_comps[co2_comps['company_name'] == 'Berkshire Hathaway Inc.'].index)
        
        
        net_zero_df = pd.DataFrame()
        # main_dict_df = defaultdict()
        # for idx,row in comp_years.iterrows():
        # co = row['company_name']
        yr = int(comp_df['net_zero_pledge_year'].unique())
        
        # comp_df = co2_comps[co2_comps['company_name']==co]

        ### emission prediction
        data = comp_df['s1'] + comp_df['s2'] + comp_df['s3'] 

        forecast_values = forecasting(data)
        revenue_forecast = forecasting(comp_df['revenue__mil_$'])
        production_forecast = forecasting(comp_df['production_volume_mil_units'])
        
        
        last_year = comp_df['year'].max()
        next_df = pd.DataFrame({'year': range(last_year+1, last_year+81),'yearly_sum': forecast_values,'revenue__mil_$':revenue_forecast,'production_volume_mil_units':production_forecast, 'company_name':selected_company, 'net_zero_pledge_year':yr})

        comp_df = comp_df.drop(['sector','type','s1','s2','s3','services_provided',	'headquarters_location'], axis=1)
        
        main_df = pd.concat([comp_df, next_df], ignore_index=True)

        main_df['Diff_NetZero_emipred'] = main_df['net_zero_pledge_year'] - main_df['year']

        main_df['Flag'] = main_df['yearly_sum'].apply(lambda x: 'Meet' if x<=0 else 'NotYet')
        main_df['Data_path'] = main_df.apply(lambda x: 'Inherent' if x['year'] <= last_year else 'Forecasted', axis=1)
        
        # main_dict_df[co] = main_df

        new_data_df = pd.DataFrame({
        'company_name' :selected_company,
        # 'net_zero_pledge_year' : yr,
        'Able_to_meet' : main_df.apply(lambda x: meet_net_zero(x['Diff_NetZero_emipred'],x['Flag']), axis=1),
        'pred_yr_to_meet' : main_df.apply(lambda x: meet_pred_yr(x['year'],x['Flag']), axis=1),
        })
        
        emissions_pred_df_0 = new_data_df.dropna(axis=0, how='any')
        emissions_pred_df_0 = emissions_pred_df_0.iloc[0]

        emissions_pred_df = pd.DataFrame([emissions_pred_df_0], columns=new_data_df.columns)
        net_zero_df = pd.concat([net_zero_df,emissions_pred_df], ignore_index=True)
        
        
        return main_df,net_zero_df
import streamlit as st
import pandas as pd

def create_predictions_data(prop_name,properties, hz=None):

    columns = ['Year','LTV','PD','History','Decision'] # PD FR
    # pred_df = pd.DataFrame(columns=columns)
    df_lst = []

    for year in ['2020', '2025', '2030', '2035', '2040', '2045', '2050']:
        
        temp_df = {}
        ltv = f"{float(properties.get(f'LTV {year}', 0)):.3g}"  # Convert to float and format
        
        if hz == 'pd_model':
            probd = f"{float(properties.get(f'PD {year}', 0)):.3g}"  # Convert to float and format
        elif hz == 'flood':
            pd_fr_value = properties.get(f'PD_FR_{year}', '')  # Retrieve PD_FR value
            probd = f"{float(pd_fr_value) if float(pd_fr_value) else 0:.3g}"  # Convert to float and format, or use 0 if not available
        
        decision = 'Approve' if probd and float(probd) < 0.5 else 'Deny'  # Check if PD_FR is available and less than 0.5
        

        temp_df['Year'] = year
        temp_df['LTV'] = ltv
        if hz == 'pd_model':
            temp_df['PD'] = probd
        elif hz == 'flood':
            temp_df['PD FR'] = probd
        temp_df['History'] = properties['Credit History'].iloc[0]
        temp_df['Decision'] = decision
        
        df = pd.DataFrame([temp_df])
        df_lst.append(df)

    pred_df =  pd.concat(df_lst)
    return pred_df 
    
  
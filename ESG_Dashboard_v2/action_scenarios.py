import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def action_scenarios(scen_df):
    # Create a Plotly figure for temperature increase plot
    fig = go.Figure()
    
    # final_yr = scen_df['year'].max()
    # early_action_x = [2021, 2026, 2031, final_yr]
    # late_action_x = [2031,2036, final_yr]
    

    # early_action_y = [30,210,300,900]#list(np.linspace(30,900,4))
    # late_action_y = [30,500,1100]#list(np.linspace(30,1100,3))

    early_action_carbon_tax = []
    
    # calculate temperature increase, total emissions, reduction needed to meet target
    # calc_temp = [val * 0.0001 for val in below_degree_df['yearly_sum']]

    # emission_lst = below_degree_df['yearly_sum'].tolist()
    # recuction_lst = [(val -(target_temprature/0.0001)) for val in emission_lst]

    # emits = [f'Total Emission: {round(i,2)}' for i in emission_lst]
    # reducts = [f'Reduction_in_emission_needed: {round(i,2)}' for i in recuction_lst]

    # if selected_scenario !='Below 2 degree Celcius':
    
    #     below_degree_df['risk_transition'] = below_degree_df.apply(lambda x: 'transition risk assigned' if x['Able_to_meet'] == 'Yes' else 'Delayed Transition risk', axis=1)
    
    # below_degree_df['risk_transition'] = 
    # Add temperature increase trace
    # hovertext=[(i,j) for i,j in zip(emits,reducts)]
    fig.add_trace(go.Scatter(x=scen_df['year'], y=scen_df['early_carbon_tax'],
                            mode='lines',
                            name='Early Action'))
    fig.add_trace(go.Scatter(x=scen_df['year'], y=scen_df['late_action_carbon_tax'],
                            mode='lines',
                            name='Late Action'))
    fig.add_trace(go.Scatter(x=scen_df['year'], y=scen_df['no_add_action_carbon_tax'],
                            mode='lines',
                            name='No Additional Action'))

    
    fig.update_layout(
                    title='Carbon pricing scenarios',
                    xaxis_title='year',
                    yaxis_title='carbon pricing',
                    showlegend=True,
                    legend=dict(x=1, y=0.98),
                    # annotations= generate_annotations(below_degree_df,company) if selected_scenario !='Below 2 degree Celcius' else None
                    )#grid=dict(visible=True))

    # Show plot
    return fig


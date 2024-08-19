
import plotly.graph_objects as go

class PredSlope(object):

    def __init__(self, df=None):
        self.df = df

    def generate_annotations(self,selected_company):
        annote_add = []
        selected_df = self.df[self.df['company_name'] == selected_company]
        for i, row in selected_df.iterrows():
            annote_add.append(dict(x= 1, y= 0.99, xref='paper', yref='paper', text=f'Net Zero Pledge Year: {row["net_zero_pledge_year"]}<br>Prediction to meet Pledge Year: {int(row["pred_yr_to_meet"])}', showarrow=False))
    

        return annote_add


    def create_plot_data(self):

        # Create figure
        
        traces = []
        # Add traces for each company
        for company in self.df['company_name'].unique():
            company_data = self.df[self.df['company_name'] == company]

            current_data = company_data.loc[:company_data.index[company_data['Data_path']=='Inherent'][-1]]#[company_data['year'] <= company_data["net_zero_pledge_year"].max()]
            # forecasted_data = company_data[company_data['year'] >= company_data["net_zero_pledge_year"].max()]
            forecasted_data = company_data.loc[company_data.index[company_data['Data_path']=='Forecasted'][0]-1:company_data.index[company_data['Data_path']=='Forecasted'][-1]]
            
            pledge_year_range = list(range(forecasted_data['year'].min(),forecasted_data['net_zero_pledge_year'].max()+1))
            
            
            forecasted_data['yearly_sum'] = forecasted_data.apply(lambda x: 0 if x['yearly_sum'] < 0 else x['yearly_sum'], axis=1)
            
            
            if max(pledge_year_range) in forecasted_data['year'].tolist():
                # print('in extended')
                # extended_emissions = forecasted_data.apply(lambda x: slope_dff(max_emit,x['yearly_sum']),axis=1).tolist()
                extended_emissions = list(forecasted_data['yearly_sum'].loc[:forecasted_data['year'].eq(max(pledge_year_range)).idxmax()]) #+ #[0] * (forecasted_data['net_zero_pledge_year'].max() - max(pledge_year_range))
            else:
                # print('not in extended')
                extended_emissions = list(forecasted_data['yearly_sum'].loc[:forecasted_data['year'].eq(forecasted_data['year'].max()).idxmax()]) + [0] * (forecasted_data['net_zero_pledge_year'].max() - forecasted_data['year'].max())

            pledge_emission = extended_emissions[-1]
            # pledge_year = max(pledge_year_range)
            start_emission = extended_emissions[0]
            emission_slopelst = [abs(pledge_emission - x) for x in extended_emissions]

            default_color = 'red'
            default_size = 8
            default_symb = 'circle'
            
            # Create a list of colors for all points with default color
            colors = [default_color] * (len(forecasted_data['year']) - 1) + ['red']  # Set the last point's color to blue
            sizes = [default_size] * (len(forecasted_data['year']) - 1) + [default_size]  # Set the size of the last point to be double
            labels = [None] * (len(forecasted_data['year']) - 1) + [str(forecasted_data['year'].max())]  # Set the size of the last point to be double
             

            traces.append(go.Scatter(x=current_data['year'], y=current_data['yearly_sum'], mode='lines+markers', name=f'{company} - Actual path', visible='legendonly'))
            traces.append(go.Scatter(
                x=forecasted_data['year'], 
                y=forecasted_data['yearly_sum'],
                text=labels,
                textposition='top center',
                line=dict(color='red'),
                marker=dict(color=colors,size=sizes), 
                mode='lines+markers+text', name=f'{company} - Forecasted path based on current emissions', 
                visible='legendonly',
                textfont=dict(
                    color='black',     # Set text color
                    size=12            # Set text size
                )))
            traces.append(go.Scatter(
                x= [pledge_year_range[0],max(pledge_year_range)], #[pledge_year_range[0]] 
                y=  [start_emission,emission_slopelst[-1]], #[emission_slopelst[0]]
                mode='lines+markers+text', name=f'{company} - Inherent path towards Net Zero Pledge', 
                visible='legendonly',
                line=dict(color='green'),
                text=[pledge_year_range[0],max(pledge_year_range)],
                textposition='top center',
                marker=dict(color=['green','green'],size=[8,8]), 
                textfont=dict(
                    color='black',     # Set text color
                    size=12            # Set text size
                )
                ))
            
            layout = go.Layout(
                title=f'Emissions for {company}',
                xaxis=dict(title='year', tickmode='linear'),
                yaxis=dict(title='Emissions'),
                height = 500,
                width = 1000,
                annotations = self.generate_annotations(company))

        fig = go.Figure(data=traces,layout=layout)
        fig.data[0].visible = True
        fig.data[1].visible = True
        fig.data[2].visible = True
        # fig.data[3].visible = True
        return fig
    
    # def create_figure(self,fig):

        
        
    #     # Set the first company's data to be visible initially
    #     fig.data[0].visible = True
    #     fig.data[1].visible = True
    #     fig.data[2].visible = True
    #     fig.data[3].visible = True

    #     # Create dropdown menu
    #     buttons = []
    #     for company in self.df['company_name'].unique():
    #         visibility = [False] * len(self.df['company_name'].unique()) * 4
    #         # print(df['company_name'].unique().tolist().index(company))
    #         visibility[self.df['company_name'].unique().tolist().index(company) * 4] = True
    #         visibility[self.df['company_name'].unique().tolist().index(company) * 4 + 1] = True
    #         visibility[self.df['company_name'].unique().tolist().index(company) * 4 + 2] = True
    #         visibility[self.df['company_name'].unique().tolist().index(company) * 4 + 3] = True
    #         buttons.append(dict(method='update',
    #                             label=company,
    #                             args=[{'visible': visibility},
    #                                 {'title': f'{company} Emissions', 'annotations':self.generate_annotations(company)}]))

    #     button_layer_1_height = 1.3
    #     fig.update_layout(
    #         updatemenus=[
    #             dict(
    #                 buttons=buttons,
    #                 direction="down",
    #                 pad={"r": 10, "t": 10},
    #                 showactive=True,
    #                 x=0.2,
    #                 xanchor="left",
    #                 y=button_layer_1_height,
    #                 yanchor="top",
    #             ),
    #         ]
    #     )

    #     # Show figure
    #     return fig

    def main(self):
        fig = self.create_plot_data()
        # new_fig = self.create_figure(fig)
        return fig






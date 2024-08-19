
import numpy as np
import plotly.graph_objects as go

class PlotDF(object):

    def __init__(self,df=None, plotname = None):
        self.df = df
        self.plotname = plotname

    
    def calculate_transition_probabilities(self,ranks):
        num_years = len(ranks)
        transition_matrix = np.zeros((num_years, num_years))
    
        for i in range(num_years):
            for j in range(num_years):
                from_rank = ranks[i]
                to_rank = ranks[j]
                count = sum(1 for k in range(num_years - 1) if ranks[k] == from_rank and ranks[k + 1] == to_rank)
                transition_matrix[i][j] = count / (num_years - 1)
    
        return transition_matrix
        

    def generate_annotations(self,selected_company):
        annote_add = []
        for i, row in self.df.iterrows():
        
            annote_add.append(dict(x= 1, y= 0.99, xref='paper', yref='paper', text=f'Net Zero Pledge Year: {row["net_zero_pledge_year"]}<br>Prediction to meet Pledge Year: {int(row["pred_yr_to_meet"])}', showarrow=False))
    
        return annote_add



    def plot_predictions(self,companies):
        # Create traces for each company
        traces = []
        for company in companies:
            df_company = self.df[self.df['company_name'] == company]

            if self.plotname == 'bar':
                traces.append(go.Bar(
                    x=df_company['year'],
                    y=df_company['yearly_sum'],
                    name=company,
                    hovertemplate='year: %{x}<br>' +
                                  'Emissions: %{y}<extra></extra>'
                ))
                
            elif self.plotname == 'pie':
                traces.append(go.Pie(
                    labels=df_company['year'],
                    values= round(df_company['yearly_sum'],2),
                    hoverinfo= 'text + percent',  # Additional information to display on hover
                    text = round(df_company['yearly_sum'],2),
                    hole=0,  # Set to a value between 0 and 1 to create a donut chart (e.g., 0.4 for a hole)
                    marker=dict(
                        line=dict(
                            color='black',  # Border color
                            width=1  # Border width
                        )
                    )
                ))
            elif self.plotname == 'scatterline':
                traces.append(go.Scatter(
                    x=df_company['year'],
                    y=df_company['emissions_per_mil_revenue'],
                    name=company,
                    mode='lines+markers',
                    hovertemplate='year: %{x}<br>' +
                                  'Emissions_per_mil_revenue: %{y}<extra></extra>'
                ))

            elif self.plotname == 'matrix':
                rank_lst = df_company[['2016_rank', '2017_rank', '2018_rank',	'2019_rank', '2021_rank', '2022_rank']]
                ranks = np.array(rank_lst)[0]
        
                transition_probabilities = self.calculate_transition_probabilities(ranks)
                traces.append(go.Table(
                    header=dict(values=[" <b>To<b> <br> <b>From<b>"] + [str(year) for year in ['2016', '2017', '2018','2019', '2021', '2022']]),
                    cells=dict(values=[['2016', '2017', '2018','2019', '2021', '2022']] + [[f"{prob:.2f}" for prob in row] for row in transition_probabilities]),
                ))
                # traces.append(go.Heatmap(z=transition_probabilities,
                #      x=['2016', '2017', '2018','2019', '2021', '2022'],
                #      y=['2016', '2017', '2018','2019', '2021', '2022'],
                #      colorscale='Viridis'
                # ))


        return traces

    def create_layout(self,companies):
        # Create layout

        if self.plotname == 'matrix':
            layout = go.Layout(title= f'Transition Probability Matrix for 3M Company',
                       xaxis=dict(title=f'From State'),
                       yaxis=dict(title=f'To State'),
                       # height = 800,
                       # width = 1000,
                       )
                       
        else:

            layout = go.Layout(
                title=f'Emissions for {companies[0]}',
                xaxis=dict(title='year', tickmode='linear'),
                yaxis=dict(title='Emissions'),
                height = 500,
                width = 1000,
                annotations= self.generate_annotations(companies),
                )

        return layout

    def create_figure(self,traces,layout):
    
        fig = go.Figure(data=traces, layout=layout)
       
        return fig

    def main(self):
        companies = self.df['company_name'].unique()
        trcs = self.plot_predictions(companies)
        layout = self.create_layout(companies)
        fig = self.create_figure(trcs,layout)
        return fig

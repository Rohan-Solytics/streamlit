
import numpy as np
import plotly.graph_objects as go


class PlotSources(object):
    
    
    def __init__(self,df=None):
        # Create the Plotly figure
        self.fig = go.Figure()
        self.df = df
    

        
    def plotValues(self, sectors):
        # Add stacked bar traces for each sector
        for sector in sectors:
            sector_data = self.df[self.df['sector'] == sector]
            traces = []
            for company in sector_data['company_name'].unique():
                company_data = sector_data[sector_data['company_name'] == company]
                traces.append(go.Bar(
                    x=company_data['s1'],
                    y=company_data['services_provided'],
                    name=company,
                    hovertext=company_data['company_name'],
                    opacity=0.7,
                    orientation = 'h',
                ))
            for trace in traces:
                self.fig.add_trace(trace)
        
    
    
    def update_plot(self):
    
        # Update the layout
        self.fig.update_layout(
            barmode='stack',
            # width = 1200,
            # height = 500,
            
        )
        
        # Update the legend to show company names
        self.fig.update_layout(
            legend_title="Companies",
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1.02,
                xanchor="right",
                x=1.5
            )
        )
        
        # Show the plot
        # self.fig.show()
        return self.fig
    
    def main(self):
        # Create a list of sectors for the dropdown menu
        sectors = self.df['sector'].unique().tolist()
        self.plotValues(sectors)
        fig = self.update_plot()
        return fig
        # plot(fig, filename='stackbar.html', auto_open=True)


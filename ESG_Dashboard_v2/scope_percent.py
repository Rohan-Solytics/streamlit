import plotly.graph_objects as go
import streamlit as st
import plotly.express as px

def percentile_calc(data):

    # Calculate the percentiles for each category
    percentiles = data.groupby('sector')['yearly_sum'].quantile([0.25, 0.5, 0.75]).reset_index()

    # Plotting
    fig = px.box(data, x='sector', y='yearly_sum', points=False, title='Yearly Sum Distribution for Different Sectors')

    # Add scatter points for percentiles
    fig.add_trace(px.scatter(percentiles, x='sector', y='yearly_sum', color='level_1', 
                            color_continuous_scale='viridis', 
                            labels={'yearly_sum': 'yearly Sum', 'level_1': 'Percentile'}).data[0])

    fig.update_layout(height = 700, width = 1000)

    # Update hover info to display percentile information
    fig.update_traces(hovertemplate='<b>Category</b>: %{x}<br><b>yearly Sum</b>: %{y}<br><b>Percentile</b>: %{marker.color}')

    return fig


class PcPlot(object):

    def __init__(self, df=None, colname=None):
        self.df = df
        self.colname = colname


    def create_figure(self, traces, colname):
        
        fig = go.Figure()
        for trace in traces:
            fig.add_trace(trace)
    
       
        
        # Update layout to include dropdown
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=[
                        dict(
                            label=var,
                            method='update',
                            args=[{'visible': [True if trace.name.startswith(var) else False for trace in fig.data]},
                                  {'title': f"{var}    sector: {self.df[self.df[colname] == var]['sector'].tolist()[0]} - S1, S2 and S3 Comparison",
                                  } if colname == 'company_name' else {'title': f'{var} - S1, S2 and S3 Comparison'}] #'annotations':self.generate_annotations(var)
                        ) for var in self.df[colname].unique()
                    ],
                    direction='down',
                    showactive=True,
                    x=1.0,
                    xanchor='right',
                    y=1.15,
                    yanchor='top',
                     
                )

            ]
        )
        
        # Update layout
        fig.update_layout(
            title= 'S1, S2 and S3 Comparison',
            # xaxis=dict(title='sector'),
            # yaxis=dict(title='Emissions'),
            # barmode='stack',
            height = 500,
            width = 1100,
            # annotations = generate_annotations(df_cs1['company_name'].iloc[0])
        )
        
        # Show plot
        return fig

    def calc_pc(self,colname):
        traces = []
        for var in self.df[colname].unique():
            # for metric in ['s1','yearly_sum']:
            yearly_sum = self.df[self.df[colname] == var]['yearly_sum']
            s1_sum = self.df[self.df[colname] == var]['s1']
            s2_sum = self.df[self.df[colname] == var]['s2']
            s3_sum = self.df[self.df[colname] == var]['s3']
            
            s1_percentage = (s1_sum / yearly_sum) * 100
            s2_percentage = (s2_sum / yearly_sum) * 100
            s3_percentage = (s3_sum / yearly_sum) * 100
            # yearly_sum_percentage = 100 - s1_percentage
        
            if colname == 'company_name':
                sec = self.df[self.df[colname] == var]['sector']
                trace_name = f"{var}-{sec} - yearly_sum: {yearly_sum}, s1: {s1_sum}, s2: {s2_sum}, s3: {s3_sum}"
            else:
                trace_name = f"{var} - yearly_sum: {yearly_sum}, s1: {s1_sum}, s2: {s2_sum}, s3: {s3_sum}"
                
            traces.append(go.Pie(
                labels= ['S1','S2','S3'],
                values=[float(s1_percentage),float(s2_percentage),float(s3_percentage)],
                name= trace_name,
                text = [round(s1_sum,2),round(s2_sum,2),round(s3_sum,2)],
                hoverinfo= 'label + percent + text',  # Additional information to display on hover
                textinfo = 'label + percent',
                hole=0,  # Set to a value between 0 and 1 to create a donut chart (e.g., 0.4 for a hole)
                marker=dict(
                    line=dict(
                        color='black',  # Border color
                        width=1  # Border width
                    )
                )
            ))
        return traces
        
    def main(self):
        trcs = self.calc_pc(self.colname)
        fig_ = self.create_figure(trcs,self.colname)
        return fig_

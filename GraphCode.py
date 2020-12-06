#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 11:11:28 2020

@author: laurenkirsch
"""

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
pd.options.plotting.backend = "plotly"
pio.renderers.default = "browser"


try:
        app = dash.Dash(__name__)
    
        app.layout = html.Div([
            html.Label('Search Box'),
        dcc.Input(id="search_gene", 
                  type="text",
                  value = '',
                  placeholder="Type a human gene name",
                  debounce = True,
                  minLength = 0, maxLength = 50,
                  autoComplete='on',
                  size='40'),            
        html.Br(),
        html.Div([
            html.Div([
            dcc.Graph(id='mygraph')])])    
        ])           
                              
        @app.callback(
            Output('mygraph', 'figure'),
            [Input('search_gene', 'value')])
        def update_output(search_gene):
            df = pd.read_csv('list_out.txt', sep = '\t', dtype=str)
            df = df.transpose().reset_index().rename(columns={'index':'Date'})
            new_header = df.iloc[0] 
            df = df[1:] 
            df.columns = new_header
            df = df.iloc[0:600]
            df = df.set_index('Date')

            
            lookup_df = pd.read_csv('Gene_Lookup.csv', dtype = str)
            link = lookup_df.set_index('Approved_Symbol').Linked_Genes.str.split('|').to_dict()
            
            link_date = lookup_df.set_index('Approved_Symbol').Date_Name_Changed.to_dict()
            
            
            if search_gene:
                search_gene = (search_gene).upper()
                #search_gene='BRCA2'
                syns = link[search_gene]
                date = link_date[search_gene]
            
                trace1 = go.Scatter(x=df.index, 
                                    y = df[search_gene], 
                                    line_shape='linear', 
                                    line = dict(color='steelblue'), 
                                    name = search_gene)

                fig = go.Figure()
                fig.add_trace(trace1)
                
                for i in syns:
                    try:
                        fig.add_trace(go.Scatter(x=df.index, 
                        y = df[i], 
                        line_shape='linear', 
                        line = dict(color='black', dash = 'dash'), 
                        name = i))
                    except:
                        pass
                
                fig.update_layout(title="Human Gene Name Occurances Per Month", xaxis_title="Date", yaxis_title="Count")
                
                fig.add_shape(type="line", name = 'Date Human Genome Sequenced',
                              x0='2003-4', y0= '-10', x1='2003-4', y1=100,
                              line=dict(color="lightblue",width=3))
                
                fig.add_shape(type="line", name = 'Date Name Changed',
                              x0=date, y0='-10', x1=date, y1=100,
                              line=dict(color="blue",width=3))
                    
            elif search_gene is None or len(search_gene) == 0:
                df1 = pd.read_csv('list_out1.txt', sep='\t', dtype=str)
                df1 = df1.set_index('Date')
                fig = px.line(df1, x=df1.index, y=df1.columns)
                fig.update_layout(title="Human Gene Name Occurances Per Month", xaxis_title="Date", yaxis_title="Count", height = 600)
                fig.add_shape(type="line", name = 'Date Name Standardized',
                              x0='2016-5', y0= '-10', x1='2016-5', y1=100,
                              line=dict(color="darkblue",width=3))
                fig.add_shape(type="line", name = 'Date Human Genome Sequenced',
                              x0='2003-4', y0= '-10', x1='2003-4', y1=100,
                              line=dict(color="lightblue",width=3))
                
            return fig
                    
                
        if __name__ == '__main__':
            app.run_server(debug=True)

except:
    pass


#===========================#
# IMPORT MODULES AND FILES
#==========================#
# DROPDOWN: https://pbpython.com/plotly-dash-intro.html

# import modules
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go
import cufflinks as cf
cf.set_config_file(offline=True)


# import data
data = pd.read_csv('CALENDAR_DATA.csv')
data.head()

# transform in time and select time
strer = lambda x: str(x)
slicer = lambda x: x[len(x)-8:len(x)]

data['TIME_DURATION'] = data['TIME_DURATION'].apply(strer)
data['TIME_DURATION'] = data['TIME_DURATION'].apply(slicer)
data['TIME_DURATION'] = pd.to_datetime(data['TIME_DURATION']).dt.hour
data['TIME_DURATION']

# group to plot
group = pd.DataFrame(data['TIME_DURATION'].groupby(data['SUMMARY']).sum())
group.reset_index(inplace=True)
group = group[group.TIME_DURATION > 20]

gdt = group.copy()
gdt.sort_values('TIME_DURATION', inplace=True)

df = pd.DataFrame(np.random.rand(6, 3),
                columns=['A', 'B', 'C'])


fig1 = df.iplot(kind='bar', 
                barmode='stack',
                title='Stacked Bar Chart with Random Data',
                asFigure=True)

#==========================#
# APPLICATION
#========================#

tipo = 'Número de horas trabalhadas'

app = dash.Dash()

# type of solicitation
sol = ['teste1', 'teste2']


'''
html.Div(children='symbol do graph:'),
dcc.Input(id='input', value='', type='text'),
html.Div(id='output-graph')
'''

#----------- BODY
app.layout = html.Div([
    html.H2("Solicitações na Prefeitura do Recife"),
    html.Div([
            dcc.Dropdown(
                id="input",
                options=[{
                    'label': i,
                    'value': i
                } for i in sol],
                value='All Managers'), ],

        style={'width': '25%',
               'display': 'inline-block'}),
    html.Div(id='output-graph')
])


@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
)

def update_graph(input_data):

        return dcc.Graph(id='example-graph',
                figure={
                    'data': [
                        {'x': gdt.TIME_DURATION, 'y': gdt.SUMMARY, 'type': 'bar', 'name': tipo, 'orientation': 'h'},
                    ],
                    'layout': {
                        'margin':{
                            'l': 200
                        },
                        'title' : tipo,
                        'height': 600,
                        'yaxis': {
                            'title': 'Atividades'
                        }
                    }
                        #'type': 'date',
                        #'tickformat': '%M:%Y'
                    
                }
    )
    


if __name__ == '__main__':
    app.run_server(debug=True)



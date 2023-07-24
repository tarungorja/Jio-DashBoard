# visit http://127.0.0.1:8050/ in your web browser.
import pathlib
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from datetime import datetime
from datetime import date
import dash_auth


app=dash.Dash(__name__,title="MyCSVapp",external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions = True,prevent_initial_callbacks=True)
server=app.server
username=[["1234567890","1234567890"]]
auth=dash_auth.BasicAuth(app,username)


#data
df = pd.read_csv('random_data.csv')
df['Year'] = pd.to_datetime(df['Date']).dt.year
avg_data = df.groupby('Year').mean(numeric_only=True).reset_index()
# def load_data(data_file: str) -> pd.DataFrame:
#     '''
#     Load data from /data directory
#     '''
#     PATH = pathlib.Path(__file__).parent
#     DATA_PATH = PATH.joinpath("data").resolve()
#     return pd.read_csv(DATA_PATH.joinpath(data_file))

#data
# df = load_data('random_data.csv')
# df['Year'] = pd.to_datetime(df['Date']).dt.year
# avg_data = df.groupby('Year').mean(numeric_only=True).reset_index()



#style
smart_battery_dashboard_style={
    "textAlign": "center",
    'font-family': 'Comic Sans MS',
    "display": "inline-block", 
    "vertical-align": "middle",
    'font-size': '65px'
}

np.random.seed(42)
random_x = np.random.randint(1,101,100)
random_y = np.random.randint(1,101,100)
parameters_plot=html.Div([
        html.P("This is the content of Parameters Plot"),
        dcc.Graph(id='parameters_plot'),
    ]),

frequency_histograms=html.Div([
        html.P("This is the content of Frequency Histograms"),
        html.Div(id='frequency_histograms')
        #dcc.Graph(id='frequency_histograms'),
    ]),

data_availability=html.Div([
        html.P("This is the content of Data Availability"),        
        dcc.Graph(
            id='bar-chart',
            figure={
                'data': [
                    go.Bar(
                        x=avg_data['Year'],
                        y=avg_data[column],
                        name=column
                    ) for column in avg_data.columns[1:]
                ],
                'layout': go.Layout(
                    title='Average Parameters by Year',
                    xaxis={'title': 'Year'},
                    yaxis={'title': 'Average Value'},
                    barmode='group',
                    height=500
                )
            }
        )
    ]),        


app.layout = html.Div([
    dcc.Location(id='url'),
    html.Div([
        html.Img(src=r"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRdXp6BcRI1EEjzO07AoWD7IzzA7P77po_UUn1rxtE&s", alt='Jio',style={"padding":"10px"}),
        html.H1("Smart Battery Dashboard", style=smart_battery_dashboard_style),
    ],style={'background-color': '#C0F94F',"textAlign": "center"}),
    html.Br(),
    
    html.H1("Stationary Battery Analysis", style={"text-align": "center"}),
    html.Br(),
    
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='parameter_no',
                options=[{'label': col, 'value': col} for col in df.columns[1:5]],
                value="Parameter1"
            )
        ],
        style={'width': '30%', 'display': 'inline-block',"vertical-align": "middle"}),
        
        html.Div("  From  ",style={'display': 'inline-block',"margin-left":"40px"}),
        html.Div([
            dcc.DatePickerSingle(
                id='pick_start_date',
                min_date_allowed=min(df['Date']),
                max_date_allowed=max(df['Date']),
                initial_visible_month=min(df['Date']),
                display_format='DD-MM-YY',
                date=date(2017, 8, 25)
            ),
        ],
        style={'width': '15%', 'display': 'inline-block'}),
        
        html.Div("  To  ",style={'display': 'inline-block'}),
        html.Div([
            dcc.DatePickerSingle(
                id='pick_end_date',
                min_date_allowed=min(df['Date']),
                max_date_allowed=max(df['Date']),
                initial_visible_month=max(df['Date']),
                display_format='DD-MM-YY',
                date=date(2018, 8, 25)
            ),
        ],
        style={'width': '15%', 'display': 'inline-block'}),
        html.Button('Submit', id='submit', n_clicks=0,style={'display': 'inline-block',}),
        
    ],style={"textAlign": "center"}),
    html.Br(),
    
    html.Div([
        dbc.Nav([
            dbc.NavLink("Parameters Plot",href='/',active="exact"),
            dbc.NavLink("Frequency Histograms",href='/frequency_histograms',active="exact"),
            dbc.NavLink("Data Availability",href='/data_availability',active="exact"),
        ],pills=True,),
        html.Hr(style={'padding':'0',"margin":"0"}),
    ]),
    html.Div(id="page_content", style={"textAlign":'center'}),
    
   
])


@app.callback(Output("page_content", "children"),
              [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return parameters_plot
    elif pathname == "/frequency_histograms" :
        return frequency_histograms
    elif pathname == "/data_availability" :
        return data_availability
    return "404-error"

@app.callback(Output("parameters_plot","figure"),
             [Input("submit","n_clicks")],
             [State("parameter_no","value")],
             [State("pick_start_date",'date')],
             [State("pick_end_date",'date')])
def page_output1(n_clicks,column,start_date,end_date):
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df[column], mode='lines', name=column))
    fig.update_layout(
        title='Line Graph: Date vs. {}'.format(column),
        xaxis_title='Date',
        yaxis_title=column,
        height=500
    )
    
    return fig

@app.callback(Output("frequency_histograms","children"),
             [Input("submit","n_clicks")],
             [State("parameter_no","value")],
             [State("pick_start_date",'date')],
             [State("pick_end_date",'date')])
def page_output2(n_clicks,tower,start_date,end_date):
        return "This is the info of the Frequency Histograms of {}, from {} to {}, No of clicks = {}".format(tower,start_date,end_date,n_clicks)

# @app.callback(Output("data_availability","children"),
#              [Input("submit","n_clicks")],
#              [State("parameter_no","value")],
#              [State("pick_start_date",'date')],
#              [State("pick_end_date",'date')])
# # def page_output3(n_clicks,tower,start_date,end_date):
#         return "This is the info of the data_availability of {}, from {} to {}, No of clicks = {}".format(tower,start_date,end_date,n_clicks)    


if __name__ == "__main__":
    app.run_server(debug=True)
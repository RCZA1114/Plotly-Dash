 # Import libraries
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
from datetime import date, timedelta
from data import get_data #Im getting data from the 24 hour FIle
import chart_studio
import chart_studio.plotly as py
import chart_studio.tools as tls


while True:
    data = pd.read_csv("2023.csv")

    data['Date/Time'] = pd.to_datetime(data['Date/Time'])
    

    app = Dash()

    measurement = dcc.Dropdown(
        options = ['PM2.5', 'VOC', 'Humidity', 'Temperature', 'Pressure'],
        value = 'PM2.5'
    )

    

    towers = dcc.Dropdown(
        options = data['Tower ID'].unique(),
        value = 'Tower 5'
    )

    day = dcc.DatePickerSingle(
            min_date_allowed=date(2023, 1, 10),
            date=date(2023, 10, 12)
        )

    app.layout = html.Div(children=[
        html.H1(children='Tower Stuff'),
        measurement,
        towers,
        day,
        dcc.Graph(id='price-graph'),
        dcc.Interval(
            id='interval-component',
            interval=600*1000, # in milliseconds
            n_intervals=0
        )
    ])

    @app.callback(
        Output(component_id='price-graph', component_property='figure'),
        #Input(component_id=towers, component_property='value'),
        Input(component_id=measurement, component_property='value'),
        Input(component_id=day, component_property='date'),
        Input('interval-component', 'n_intervals'),
        
    )
    def update_graph(measure, dayz, n):
        
        user = 'ramoncarlos1114'
        api = 'Gl8JjwU6YCm3k4vm8Na8'
        chart_studio.tools.set_credentials_file(username=user, api_key=api)
        dayz = pd.to_datetime(dayz)
        data['Date/Time'] = pd.to_datetime(data['Date/Time'])
        start = dayz-timedelta(hours=24)
        tfh = data[(data['Date/Time'] >= start) & (data['Date/Time'] <= dayz)]
        line_fig = px.scatter(tfh,
                            x='Date/Time', y= measure,
                            color='Tower ID',
                            title=f'Analysis of towers')
        
        fig = py.plot(line_fig, filename = 'test graph', auto_open=False)
        #return fig
        return line_fig

    
    if __name__ == '__main__':
            app.run(debug=True, host='13.228.225.19')

    

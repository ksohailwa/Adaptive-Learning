import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_html_components as html
import urllib.parse
from sqlalchemy import create_engine, text
import dash_bootstrap_components as dbc
import random

# loading Data from DB
params = urllib.parse.quote_plus(r'Driver={ODBC Driver 18 for SQL Server};Server=tcp:adaptive-learning-server.database.windows.net,1433;Database=adaptive_learning_db;Uid=superadmin;Pwd=Poorpassword@2024;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
engine_azure = create_engine(conn_str, echo=True)

connection = engine_azure.connect()
print("Connection successful !!!!")

app = dash.Dash(__name__)

# List of material types
material_types = [
    "Visual Materials",
    "Interactive Materials",
    "Written-Based Materials",
    "Hands-on Materials",
    "Collaborative Materials",
    "Auditory Materials"
]

# Select a random recommendation
#random_recommendation="Hands-on Materials"
random_recommendation = random.choice(material_types)

layout = html.Div([
    html.H2("Here is your recommendation:", style={'textAlign': 'center', 'fontSize': '1.5em'}),
    html.H3("Based on your responses, our recommendation for you is:", style={'textAlign': 'center'}),
    html.H4(random_recommendation, style={'textAlign': 'center', 'color': 'red'}),
    html.H4(id='random-recommendation', style={'textAlign': 'center', 'color': 'red'}),
    html.Div(" ", style={'marginTop': '20px'}),
    html.Div(style={'textAlign': 'center'}, children=[
        html.Div("Give us a thumbs up if you find it helpful or not?", style={'marginTop': '20px'}),
        html.Div([
            html.Button(id='thumbs-up-button', children='👍', n_clicks=0),
            html.Button(id='thumbs-down-button', children='👎', n_clicks=0),
        ], style={'display': 'flex', 'justifyContent': 'center', 'marginTop': '10px'}),
    ]),
    html.Div(id='button-output', style={'textAlign': 'center', 'marginTop': '20px'}),
    html.Img(src='..\\assets\\animation.gif', alt="Project Photo", style={'width': '50%', 'margin': 'auto', 'display': 'block'})

])


@app.callback(
    Output('random-recommendation', 'children'),
    [Input('random-recommendation', 'id')]
)
def update_random_recommendation(_):
    random_recommendation = random.choice(material_types)
    return random.choice(material_types)
# callback for thumbs-up button
@app.callback(
    Output('button-output', 'children'),
    [Input('thumbs-up-button', 'n_clicks')]
)
def update_output_thumbs_up(n_clicks):
    if n_clicks:
        return "Thank you for your feedback!"

# callback for thumbs-down button
@app.callback(
    Output('button-output', 'children'),
    [Input('thumbs-down-button', 'n_clicks')]
)
def update_output_thumbs_down(n_clicks):
    if n_clicks:
        return "Thank you for your feedback!"

if __name__ == '__main__':
    app.run_server(debug=True)

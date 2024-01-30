import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import urllib.parse
from sqlalchemy import create_engine, text

# Loading Data from DB
params = urllib.parse.quote_plus(r'Driver={ODBC Driver 18 for SQL Server};Server=tcp:adaptive-learning-server.database.windows.net,1433;Database=adaptive_learning_db;Uid=superadmin;Pwd=Poorpassword@2024;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
engine_azure = create_engine(conn_str, echo=True)

# Connect to the database
connection = engine_azure.connect()

# Define the stored procedure query
query = text("EXEC convert_user_input_to_integer;")

# Print a success message if the connection is successful
print("Connection successful !!!!")

# Create the Dash application
app = dash.Dash(__name__)

# Define the layout of the Dash application
database_data = "RECOMM."
layout = html.Div([
    html.H2("Here is your recommendation:", style={'textAlign': 'center', 'fontSize': '1.5em'}),
    html.Div(" ", style={'marginTop': '20px'}),
    dcc.Textarea(id='feedback-input', value=database_data, style={'width': '100%', 'height': '100px'}),
    html.Div(style={'textAlign': 'center'}, children=[
        html.Div("Does it make sense for you?", style={'marginTop': '20px'}),
        html.Div([
            html.Button(id='thumbs-up-button', children='👍', n_clicks=0),
            html.Button(id='thumbs-down-button', children='👎', n_clicks=0),
        ], style={'display': 'flex', 'justifyContent': 'center', 'marginTop': '10px'}),
    ]),
    html.Div(id='button-output', style={'textAlign': 'center', 'marginTop': '20px'})
])

# Define the callback function for the thumbs-up button
@app.callback(
    Output('button-output', 'children'),
    [Input('thumbs-up-button', 'n_clicks')]
)
def update_output_thumbs_up(n_clicks):
    # Execute the stored procedure
    results = connection.execute(query)
    return f'Thumbs Up Clicked: {n_clicks} times'

# Define the callback function for the thumbs-down button
@app.callback(
    Output('button-output', 'children'),
    [Input('thumbs-down-button', 'n_clicks')]
)
def update_output_thumbs_down(n_clicks):
    # Execute the stored procedure
    results = connection.execute(query)
    return f'Thumbs Down Clicked: {n_clicks} times'

# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True)

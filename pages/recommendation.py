import pandas as pd
import dash_mantine_components as dmc
import dash_core_components as dcc
from dash import Input, Output, State, html, ctx
from dash_iconify import DashIconify
from app import app
from dash_core_components import Dropdown
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy import text

# def create_dropdown(id,label, options_list):
#     return dmc.Select(
#         id = id,
#         label = label,
#         data = [{'value':i, 'label': i} for i in options_list],
#         value = options_list[0]
#     )

def create_dropdown(id, label, options_list):
    # Filter out null values from the options list
    filtered_options = [{'value': i, 'label': i} for i in options_list if i is not None]
    
    return html.Div([
        html.Label(label, htmlFor=id),  # Add label for the dropdown
        dcc.Dropdown(
            id=id,
            options=filtered_options,
            value=filtered_options[0]['value'] if filtered_options else None
        )
    ])
    

# Load dataset from Azure SQL DB
params = urllib.parse.quote_plus(r'Driver={ODBC Driver 18 for SQL Server};Server=tcp:adaptive-learning-server.database.windows.net,1433;Database=adaptive_learning_db;Uid=superadmin;Pwd=Poorpassword@2024;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
engine_azure = create_engine(conn_str,echo=True)

connection = engine_azure.connect()
print("Connection successful !!!!")

# Perform a query to fetch effectivness
query = text(
    "SELECT * "
    "FROM import_survey;"
)

result = connection.execute(query)

# Fetch all the rows and convert them to a Pandas DataFrame
df = pd.DataFrame(result.fetchall(), columns=result.keys())

print("!!! df retrieved values:", df)
#df = pd.read_csv(r'/Users/mohamedatef/Dev/LA--AdaptiveLearning/data/Survey_data.csv')
#custs = pd.read_csv(r'/Users/mohamedatef/Dev/LA--AdaptiveLearning/data/Survey_data.csv')
layout = html.Div(
    children=[
        dmc.Title(children = 'Recommending a Personalized Education System', order = 3, style = {'font-family':'IntegralCF-ExtraBold', 'text-align':'center', 'color' :'slategray'}),
        dmc.Modal(
            id = 'info-ml',
            size = '70%',
            overflow="inside",
            title = [dmc.Title('Info', order = 3)],
            children = [
                dmc.Divider(label = 'Performance', labelPosition = 'center'),
                dmc.SimpleGrid(
                    cols = 2,
                    children = [
                        dmc.Title('Content-based Recommendation', order = 4, style = {'text-align':'center'}),
                        dmc.Title('Accurancy', order = 4, style = {'text-align':'center'}),
                        html.Img(
                            src = app.get_asset_url('ml images/CB-Info.jpg'),
                            style = {'width':'25vw','justify-self':'center'}, 
                        ),
                        html.Img(
                            src = app.get_asset_url('ml images/Acc-Info.png'),
                            style = {'width':'25vw','justify-self':'center'}
                        ),
                        dmc.Text('A content-based recommender system suggests items to users based on their preferences and the features of items. It analyzes the content of items and matches them with user profiles.', style= {'justify-self':'center'}),
                        dmc.Text('What is accuracy in recommender system? Accuracy means that the system is working as it is supposed to or as expected to, however it does not imply that recommendations are relevant to a user. Usefulness is one of the factors which contributes to user satisfaction.', style= {'justify-self':'center'}),
                    ]
                ),

            ]
        ),
        dmc.Paper(
            m = 'sm',
            pb = 'sm',
            shadow = 'md',
            withBorder = True,
            radius = 'md',
            children = [
                dmc.Stack(
                    align = 'center',
                    children = [

                        dmc.Divider(label = 'By using the data collected through your answers, you get you Recommend  ', labelPosition='center'),
                        dmc.Title('Please answer these questions and submit', order = 4, style = {'text-align':'center'}),                     
                        dmc.SimpleGrid(
                            cols = 4,
                            children = [
                                dmc.NumberInput(id = 'input-age', label = 'Age', value = 18),
                                create_dropdown('select-gender', 'Gender', df.gender.unique()),
                                create_dropdown('select-study-field', 'Study Field', df.study_field.unique()),
                                create_dropdown('select-edu-level', 'Educational level', df.education_level.unique()),
                                create_dropdown('select-employment', 'Employment Status', df.employment.unique()),
                                create_dropdown('select-studying-people', 'preferred study type', df.learning_style.unique()),
                                create_dropdown('select-studying-place', 'Study Place', df.study_place.unique()),
                                create_dropdown('select-studying-sound', 'Study Sound', df.loudness.unique()),
                                create_dropdown('select-studying-time', 'studying time', df.sessions.unique()),
                                create_dropdown('select-studying-classes', 'Studying Classes', df.on_in.unique()),
                                create_dropdown('select-studying-help', 'Support by study difficulty', df.support.unique()),
                                create_dropdown('select-likert-platforms-effectiveness', 'likert_platforms_effectiveness', df.effectiveness.unique()),
                                create_dropdown('select-trust-ai', 'Trustworthy of AI', df.trust.unique()),
                                create_dropdown('select-relying-recomm-path', 'Relying on recommendation paths', df.openness.unique()),
                                #create_dropdown('select-openness-recomm', 'Openness to recommendation Sys.', df.likert_open_edurecsys.unique()),

                            ]
                        ),
                        dmc.Button(id = 'submit-recomm', children = 'Submit'),

                        dmc.Group(spacing = 'sm', children = [dmc.Title('Accurancy of your recommendetion', order = 3),dmc.ActionIcon(id = 'more-info', color = 'blue', size = 'lg', children = [DashIconify(icon = 'material-symbols:info', width = 24)])]),
                        dmc.Text(size = 'xs', color = 'dimmed', children = 'We want high % of accurancy!'),
                        dmc.Progress(id = 'accurancy', value=83, class_name = 'progressbar', color = 'green', label = '83%', size = 'xl'),
                        
                        
                    ]
                )
            ]
        )
    ]
)
@app.callback(Output('info-ml', 'opened'),
                Input('more-info', 'n_clicks'),
                State('info-ml', 'opened'))
def open_modal(n, opened):
    if ctx.triggered_id is not None:
        return not opened
    else:
        return False
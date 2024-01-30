import dash
import pandas as pd
import dash_mantine_components as dmc
import dash_core_components as dcc
import pages
from dash import Input, Output, State, html, ctx
from dash_iconify import DashIconify
from app import app
from dash_core_components import Dropdown
import urllib.parse
from sqlalchemy import create_engine, text

def create_dropdown(id, label, options_list):
    filtered_options = [{'value': i, 'label': i} for i in options_list if i is not None]
    return html.Div([
        html.Label(label, htmlFor=id),  
        dcc.Dropdown(
            id=id,
            options=filtered_options,
            value=filtered_options[0]['value'] if filtered_options else None
        )
    ])

params = urllib.parse.quote_plus(r'Driver={ODBC Driver 18 for SQL Server};Server=tcp:adaptive-learning-server.database.windows.net,1433;Database=adaptive_learning_db;Uid=superadmin;Pwd=Poorpassword@2024;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
engine_azure = create_engine(conn_str, echo=True)

connection = engine_azure.connect()
print("Connection successful !!!!")

query = text(
    "SELECT * "
    "FROM import_survey;"
)

result = connection.execute(query)
df = pd.DataFrame(result.fetchall(), columns=result.keys())

print("!!! df retrieved values:", df)

layout = html.Div(
    children=[
        dmc.Title(children='Recommending a Personalized Education System', order=3, style={'font-family': 'IntegralCF-ExtraBold', 'text-align': 'center', 'color': 'slategray'}),
        dmc.Modal(
            id='info-ml',
            size='70%',
            overflow="inside",
            title=[dmc.Title('Info', order=3)],
            children=[
                dmc.Divider(label='Performance', labelPosition='center'),
                dmc.SimpleGrid(
                    cols=2,
                    children=[
                        dmc.Title('Content-based Recommendation', order=4, style={'text-align': 'center'}),
                        dmc.Title('Accuracy', order=4, style={'text-align': 'center'}),
                        html.Img(
                            src=app.get_asset_url('ml images/CB-Info.jpg'),
                            style={'width': '25vw', 'justify-self': 'center'},
                        ),
                        html.Img(
                            src=app.get_asset_url('ml images/Acc-Info.png'),
                            style={'width': '25vw', 'justify-self': 'center'}
                        ),
                        dmc.Text('A content-based recommender system suggests items to users based on their preferences and the features of items. It analyzes the content of items and matches them with user profiles.', style={'justify-self': 'center'}),
                        dmc.Text('What is accuracy in recommender system? Accuracy means that the system is working as it is supposed to or as expected to, however it does not imply that recommendations are relevant to a user. Usefulness is one of the factors which contributes to user satisfaction.', style={'justify-self': 'center'}),
                    ]
                ),

            ]
        ),
        dmc.Paper(
            m='sm',
            pb='sm',
            shadow='md',
            withBorder=True,
            radius='md',
            children=[
                dmc.Stack(
                    align='center',
                    children=[
                        dmc.Divider(label='By using the data collected through your answers, you get you Recommend  ', labelPosition='center'),
                        dmc.Title('Please answer these questions and submit', order=4, style={'text-align': 'center'}),
                        dmc.SimpleGrid(
                            cols=4,
                            children=[
                                dmc.NumberInput(id='input-age', label='Age', value=18),
                                create_dropdown('select-gender', 'Gender', df.gender.unique()),
                                create_dropdown('select-study-field', 'Study Field', df.study_field.unique()),
                                create_dropdown('select-edu-level', 'Educational level', df.education_level.unique()),
                                create_dropdown('select-employment', 'Employment Status', df.employment.unique()),
                                create_dropdown('select-studying-people', 'Preferred study type', df.learning_style.unique()),
                                create_dropdown('select-studying-place', 'Study Place', df.study_place.unique()),
                                create_dropdown('select-studying-sound', 'Study Sound', df.loudness.unique()),
                                create_dropdown('select-studying-time', 'Studying Time', df.sessions.unique()),
                                create_dropdown('select-studying-classes', 'Studying Classes', df.on_in.unique()),
                                create_dropdown('select-studying-help', 'Support by study difficulty', df.support.unique()),
                                create_dropdown('select-likert-platforms-effectiveness', 'Likert Platforms Effectiveness', df.effectiveness.unique()),
                                create_dropdown('select-trust-ai', 'Trustworthy of AI', df.trust.unique()),
                                create_dropdown('select-relying-recomm-path', 'Relying on recommendation paths', df.openness.unique()),
                            ]
                        ),
                        dmc.Button(id='submit-recomm', children='Submit'),
                        dmc.Group(spacing='sm', children=[dmc.Title('Accuracy of your recommendation', order=3), dmc.ActionIcon(id='more-info', color='blue', size='lg', children=[DashIconify(icon='material-symbols:info', width=24)])]),
                        dmc.Text(size='xs', color='dimmed', children='We want high % of accuracy!'),
                        dmc.Progress(id='accuracy', value=83, class_name='progressbar', color='green', label='83%', size='xl'),
                    ]
                )
            ]
        )
    ]
)

@app.callback(
    [Output('accuracy', 'value'), Output('url', 'pathname')],
    [Input('submit-recomm', 'n_clicks')],
    [State('input-age', 'value'),
     State('select-gender', 'value'),
     State('select-study-field', 'value'),
     State('select-edu-level', 'value'),
     State('select-employment', 'value'),
     State('select-studying-people', 'value'),
     State('select-studying-place', 'value'),
     State('select-studying-sound', 'value'),
     State('select-studying-time', 'value'),
     State('select-studying-classes', 'value'),
     State('select-studying-help', 'value'),
     State('select-likert-platforms-effectiveness', 'value'),
     State('select-trust-ai', 'value'),
     State('select-relying-recomm-path', 'value')],
    prevent_initial_call=True
)
def insert_into_database(n_clicks, age, gender, study_field, edu_level, employment, studying_people, studying_place,
                         studying_sound, studying_time, studying_classes, studying_help, likert_effectiveness,
                         trust_ai, relying_recomm_path):
    

    if n_clicks:
        print(f"Age: {age}")
        print(f"Gender: {gender}")
        print(f"Study Field: {study_field}")
        print(f"Educational Level: {edu_level}")
        print(f"Employment Status: {employment}")
        print(f"Preferred Study Type: {studying_people}")
        print(f"Study Place: {studying_place}")
        print(f"Study Sound: {studying_sound}")
        print(f"Studying Time: {studying_time}")
        print(f"Studying Classes: {studying_classes}")
        print(f"Support by Study Difficulty: {studying_help}")
        print(f"Likert Platforms Effectiveness: {likert_effectiveness}")
        print(f"Trustworthy of AI: {trust_ai}")
        print(f"Relying on Recommendation Paths: {relying_recomm_path}")

        user_data = pd.DataFrame({
            'Age': [age],
            'Gender': [gender],
            'Study_Field': [study_field],
            'Educational_Level': [edu_level],
            'Employment_Status': [employment],
            'Preferred_Study_Type': [studying_people],
            'Study_Place': [studying_place],
            'Study_Sound': [studying_sound],
            'Studying_Time': [studying_time],
            'Studying_Classes': [studying_classes],
            'Support_by_Study_Difficulty': [studying_help],
            'Likert_Platforms_Effectiveness': [likert_effectiveness],
            'Trustworthy_of_AI': [trust_ai],
            'Relying_on_Recommendation_Paths': [relying_recomm_path]
        })

        user_data.to_sql('user_input_data', con=engine_azure, index=False, if_exists='append')
        
        return 83, "/finalRecom"
    else:
        return dash.no_update, dash.no_update


@app.callback(Output('info-ml', 'opened'),
              Input('more-info', 'n_clicks'),
              State('info-ml', 'opened'))
def open_modal(n, opened):
    if ctx.triggered_id is not None:
        return not opened
    else:
        return False

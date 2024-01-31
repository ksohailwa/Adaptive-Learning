import pandas as pd
import urllib.parse
import plotly.express as px
import dash_mantine_components as dmc
from dash import Input, Output, State, html, dcc, dash_table, ctx
from dash_iconify import DashIconify
from sqlalchemy import create_engine
from sqlalchemy import text
from dash import callback_context
from app import app

params = urllib.parse.quote_plus(r'Driver={ODBC Driver 18 for SQL Server};Server=tcp:adaptive-learning-server.database.windows.net,1433;Database=adaptive_learning_db;Uid=superadmin;Pwd=Poorpassword@2024;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
engine_azure = create_engine(conn_str, echo=True)

connection = engine_azure.connect()
print("Connection successful !!!!")


# Perform a query to fetch table names
table_query = text(
    "SELECT * "
    "FROM main_data_web; "
)
result = connection.execute(table_query)

# Fetch all the rows and convert them to a Pandas DataFrame
df = pd.DataFrame(result.fetchall(), columns=result.keys())
# Fetch the results

print("!!! df retrieved values:", df)

############################
layout = html.Div(
    style={'overflow-x': 'hidden'},
    children=[
        dmc.Modal(
            id='cat-table',
            size='xl',
            title=[dmc.Title('Support Method Choice in Relation to Gender', order=2)],
            children=[

            ]
        ),
        dmc.Modal(
            id='num-table',
            title=[dmc.Title('Employment status in relation to Education level', order=2)],
            children=[

            ]
        ),
        dmc.Group(
            direction='column',
            grow=True,
            position='center',
            spacing='sm',
            children=[
                dmc.Title(children='Visualizations ', order=3,
                          style={'font-family': 'IntegralCF-ExtraBold', 'text-align': 'center', 'color': 'slategray'}),
                dmc.Paper(
                    shadow='md',
                    m='sm',
                    p='md',
                    withBorder=True,
                    children=[
                        dmc.Stack(
                            children=[
                                dmc.Group(
                                    position='apart',
                                    children=[
                                        dmc.Title('Total Age Range vs Support Difficulty', order=4),
                                        dmc.ActionIcon(id='categorical-table',
                                                        children=[DashIconify(icon='material-symbols:backup-table',
                                                                             width=24)], color='blue',
                                                        variant='filled', size='lg')
                                    ]
                                ),
                                dmc.Stack(
                                    children=[
                                        dmc.Select(
                                            id='column_name',
                                            label='Select Column To Investigate (Categorical)',
                                            style={'width': '50%', 'margin': 'auto'},
                                            data=[
                                                {'label': i, 'value': i} for i in
                                                df[['age', 'gender', 'study_field', 'employment', 'learning_style',
                                                    'study_place']].columns

                                            ],
                                            value='gender'
                                        ),
                                        dmc.Group(
                                            position='center',
                                            children=[

                                            ]
                                        ),
                                    ]
                                ),
                                dcc.Graph(id='compare_graph'),
                            ]
                        )
                    ]
                ),
            ]  # Closing the list of children for dmc.Group
        ),  # Closing the dmc.Group component
        dmc.Group(
            direction='column',
            grow=True,
            position='center',
            spacing='sm',
            children=[
                dmc.Title(children='Visualizations ', order=3,
                          style={'font-family': 'IntegralCF-ExtraBold', 'text-align': 'center', 'color': 'slategray'}),
                dmc.Paper(
                    shadow='md',
                    m='sm',
                    p='md',
                    withBorder=True,
                    children=[
                        dmc.Stack(
                            children=[
                                dmc.Group(
                                    position='apart',
                                    children=[
                                        dmc.Title('Total Ranking for Opinion on Effectiveness of Learning Platforms ', order=4),
                                        dmc.ActionIcon(id='categorical-table',
                                                        children=[DashIconify(icon='material-symbols:backup-table',
                                                                             width=24)], color='blue',
                                                        variant='filled', size='lg')
                                    ]
                                ),
                                dmc.Stack(
                                    children=[
                                        dmc.Select(
                                            id='column_name',
                                            label='Select Column To Investigate (Categorical)',
                                            style={'width': '50%', 'margin': 'auto'},
                                            data=[
                                                {'label': i, 'value': i} for i in
                                                df[['age', 'gender', 'study_field', 'employment', 'learning_style',
                                                    'study_place']].columns

                                            ],
                                            value='gender'
                                        ),
                                        dmc.Group(
                                            position='center',
                                            children=[

                                            ]
                                        ),
                                    ]
                                ),
                                dcc.Graph(id='compare_graph1'),
                            ]
                        )
                    ]
                ),
                dmc.Paper(
                    shadow='md',
                    m='sm',
                    p='md',
                    withBorder=True,
                    children=[
                        dmc.Stack(
                            children=[
                                dmc.Group(
                                    position='apart',
                                    children=[
                                        dmc.Title('Pie Chart: Participant Information', order=4),
                                        dmc.ActionIcon(id='table-nums',
                                                        children=[DashIconify(icon='material-symbols:backup-table',
                                                                             width=24)], color='blue',
                                                        variant='filled', size='lg')
                                    ]
                                ),
                                dmc.Select(
                                    id='column_name_num',
                                    label='Select Column To Investigate ',
                                    style={'width': '50%', 'margin': 'auto'},
                                    data=[
                                        {'label': i, 'value': i} for i in
                                        df[['gender', 'education_level', 'study_field']].columns
                                    ],
                                    value='gender'
                                ),
                                dmc.Group(
                                    # direction = 'row',
                                    position='center',
                                    children=[

                                    ]
                                ),
                                dcc.Graph(id='pie_graph'),
                            ]
                        ),
                    ]
                ),
            ]  # Closing the list of children for dmc.Group
        ),  # Closing the dmc.Group component
    ]
)
##############################################

@app.callback(Output('pie_graph', 'figure'),
              Input('column_name_num', 'value'))
def update_graph(value):

    df2 = df[value].value_counts().reset_index()
    df2.columns = ['value', 'count']
    unique_values = df2['value'].unique()
    color_map = {value: px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)] for i, value in
                 enumerate(unique_values)}
    fig = px.pie(df2, names='value', values='count', title=f'Distribution of {value}', color='value',
                 color_discrete_map=color_map)
    fig.update_layout(plot_bgcolor='#fff', paper_bgcolor='#fff')

    return fig


##########################################################
labels = ['15-20', '21-25', '26-30', '31-35', '36-40', '41-45']
df['AgeRange'] = pd.cut(df['age'], bins=[15, 20, 25, 30, 35, 40, 45], labels=labels, right=False)


@app.callback(Output('compare_graph', 'figure'),
              Input('column_name', 'value'))
def update_graph(value):

    triggered_id = [p['prop_id'] for p in callback_context.triggered][0]
    is_age_dropdown = 'column_name' in triggered_id and callback_context.inputs_list[0]['value'] == 'age'

    if is_age_dropdown:
        value_counts = df[['study_help', 'AgeRange']].groupby(['study_help', 'AgeRange']).size().to_frame().reset_index()
        value_counts.columns = ['study_help', 'value', 'count']
    else:

        value_counts = df[['study_help', value]].groupby(['study_help', value]).size().to_frame().reset_index()
        value_counts.columns = ['study_help', 'value', 'count']

    unique_values = value_counts['value'].unique()
    color_map = {val: px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)] for i, val in
                 enumerate(unique_values)}

    fig = px.bar(value_counts, x='value', y='count', title=f'Distribution of {value}', color='study_help',
                 color_discrete_map=color_map, barmode='group')

    fig.update_layout(plot_bgcolor='#fff', paper_bgcolor='#fff')

    return fig


##########################################################

@app.callback(Output('compare_graph1', 'figure'),
              Input('column_name', 'value'))
def update_graph(value):

    triggered_id = [p['prop_id'] for p in callback_context.triggered][0]
    is_age_dropdown = 'column_name' in triggered_id and callback_context.inputs_list[0]['value'] == 'age'

    if is_age_dropdown:
        value_counts = df[['effectiveness', 'AgeRange']].groupby(['effectiveness', 'AgeRange']).size().to_frame().reset_index()
        value_counts.columns = ['effectiveness', 'value', 'count']
    else:

        value_counts = df[['effectiveness', value]].groupby(['effectiveness', value]).size().to_frame().reset_index()
        value_counts.columns = ['effectiveness', 'value', 'count']

    unique_values = value_counts['value'].unique()
    color_map = {val: px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)] for i, val in
                 enumerate(unique_values)}

    fig = px.bar(value_counts, x='value', y='count', title=f'Distribution of {value}', color='effectiveness',
                 color_discrete_map=color_map, barmode='group')

    fig.update_layout(plot_bgcolor='#fff', paper_bgcolor='#fff')

    return fig


############################################################
@app.callback(Output('cat-table', 'children'),
              Output('cat-table', 'opened'),
              Input('categorical-table', 'n_clicks'),
              State('cat-table', 'opened'),
              prevent_initial_call=True)
def update_modal_cat(n, opened):

    if ctx.triggered_id is None:
        return [], False

    dft = df[['gender', 'study_place']]

    final_df = pd.DataFrame()

    for i in dft.columns.tolist():
        if i == 'study_place':
            pass
        else:
            dft = dft[['study_place', i]].groupby(['study_place', i]).size().to_frame().reset_index()
            dft.columns = ['study_place', 'value', 'count']
            final_df = pd.concat([final_df, dft[['study_place', 'value', 'count']]], ignore_index=True)

    print(final_df)
    return dash_table.DataTable(
        data=final_df.to_dict('records'),
        columns=[{'name': i, 'id': j} for i, j in zip(['study_place', 'value', 'count'], final_df.columns.tolist())],
        style_as_list_view=True,
        style_cell={'textAlign': 'left'},
    ), not opened


######################################

@app.callback(Output('num-table', 'children'),
              Output('num-table', 'opened'),
              Input('table-nums', 'n_clicks'),
              State('table-nums', 'opened'),
              prevent_initial_call=True)
def update_modal_num(n, opened):

    if ctx.triggered_id is None:
        return [], False
    dft = df[['employment', 'education_level']]
    final_df = pd.DataFrame()
    for i in dft.columns.tolist():
        if i == 'education_level':
            pass
        else:

            dft = dft[['education_level', i]].groupby(['education_level', i]).size().to_frame().reset_index()
            dft.columns = ['education_level', 'value', 'count']
            final_df = pd.concat([final_df, dft[['education_level', 'value', 'count']]], ignore_index=True)

    print(final_df)

    return dash_table.DataTable(
        data=final_df.to_dict('records'),
        columns=[{'name': i, 'id': j} for i, j in
                 zip(['education_level', 'value', 'count'], final_df.columns.tolist())],
        style_as_list_view=True,
        style_cell={'textAlign': 'left'},
    ), not opened

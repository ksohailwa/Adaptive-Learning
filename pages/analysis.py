
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc
from sqlalchemy import create_engine
from dash import Input, Output, State, html, dcc, dash_table, ctx
from dash_iconify import DashIconify

from dash import callback_context
from app import app

db_engine = create_engine('Driver=ODBC Driver 18 for SQL Server;Server=tcp:adaptive-learning-server.database.windows.net,1433;Database=adaptive_learning_db;Uid=superadmin;Pwd=Poorpassword@2024;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')

try:

    # Establish a connection
    connection = db_engine.connect()

    # Perform a simple test query
    result = connection.execute("SELECT 1")

    # Fetch the result
    row = result.fetchone()
    print("Connection successful. Result:", row[0])

    # Close the connection
    connection.close()

except Exception as e:
    print("Error:", str(e))

############################
df2 = pd.read_csv(r'/Users/mohamedatef/Dev/LA--AdaptiveLearning/data/Survey_data.csv')
layout = html.Div(
    style = {'overflow-x':'hidden'},
    children=[
        dmc.Modal(
            id = 'cat-table',
            size = 'xl',
            title = [dmc.Title('Support Method Choice in Relation to Gender', order = 2)],
            children = [

            ]
        ),
        dmc.Modal(
            id = 'num-table',
            title = [dmc.Title('Employment status in relation to Education level', order = 2)],
            children = [
                
            ]
        ),
        dmc.Group(
            #direction = 'column',
            grow = True,
            position = 'center',
            spacing = 'sm',
            children = [
                dmc.Title(children = 'Visualizations ', order = 3, style = {'font-family':'IntegralCF-ExtraBold','text-align':'center', 'color' :'slategray'}),
                dmc.Paper(
                    shadow = 'md',
                    m = 'sm',
                    p = 'md',
                    withBorder = True,
                    children = [
                        dmc.Stack(
                            children = [
                                dmc.Group(
                                    position = 'apart',
                                    children = [
                                        dmc.Title('Total Age range vs Support difficulty', order = 4),
                                        dmc.ActionIcon(id = 'categorical-table', children = [DashIconify(icon = 'material-symbols:backup-table', width=24)], color = 'blue', variant = 'filled', size = 'lg')
                                    ]
                                ),
                                dmc.Stack(
                                    children = [
                                        dmc.Select(
                                            id = 'column_name',
                                            label = 'Select Column To Investigate (Categorical)',
                                            style= {'width':'50%','margin':'auto'},
                                            data = [
                                                {'label':i, 'value':i} for i in df2[['age','gender','study_field','employment','studying_people','studying_place']].columns 
                                                
                                            ],
                                            value = 'gender'
                                        ),
                                        dmc.Group(
                                            position = 'center',
                                            children = [

                                            ]
                                        ),                                        
                                    ]
                                ),
                                dcc.Graph(id = 'compare_graph'),                                
                            ]
                        )
                    ]
                ),

                dmc.Paper(
                    shadow = 'md',
                    m = 'sm',
                    p = 'md',
                    withBorder = True,
                    children = [
                        dmc.Stack(
                            children = [
                                dmc.Group(
                                    position = 'apart', 
                                    children = [
                                        dmc.Title('PieChart participants information', order = 4),
                                        dmc.ActionIcon(id = 'table-nums', children = [DashIconify(icon = 'material-symbols:backup-table', width=24)], color = 'blue', variant = 'filled', size = 'lg')
                                    ]
                                ),
                                dmc.Select(
                                    id = 'column_name_num',
                                    label = 'Select Column To Investigate ',
                                    style= {'width':'50%','margin':'auto'},
                                    data = [
                                        {'label':i, 'value':i} for i in df2[['gender','edu_level', 'study_field']].columns
                                    ],
                                    value = 'gender'
                                ),
                                dmc.Group(
                                    #direction = 'row',
                                    position = 'center',
                                    children = [

                                    ]
                                ),
                                dcc.Graph(id = 'pie_graph'),
                            ]
                        ),
                    ]
                ),
            ]
        )
        
    ]
)
##############################################

@app.callback(Output('pie_graph', 'figure'),
                Input('column_name_num','value'))
def update_graph(value):
    df2 = pd.read_csv(r'/Users/mohamedatef/Dev/LA--AdaptiveLearning/data/Survey_data.csv')
    df2 = df2[value].value_counts().reset_index()
    df2.columns = ['value', 'count']
    unique_values = df2['value'].unique()
    color_map = {value: px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)] for i, value in enumerate(unique_values)}
    fig = px.pie(df2, names='value', values='count', title=f'Distribution of {value}', color='value', color_discrete_map=color_map)
    fig.update_layout(plot_bgcolor='#fff', paper_bgcolor='#fff')

    return fig

##########################################################
labels = ['15-20', '21-25', '26-30', '31-35', '36-40', '41-45']
df2['AgeRange'] = pd.cut(df2['age'], bins=[15, 20, 25, 30, 35, 40, 45], labels=labels, right=False)

@app.callback(Output('compare_graph', 'figure'),
              Input('column_name', 'value'))
def update_graph(value):

    triggered_id = [p['prop_id'] for p in callback_context.triggered][0]
    is_age_dropdown = 'column_name' in triggered_id and callback_context.inputs_list[0]['value'] == 'age'

    if is_age_dropdown:
        value_counts = df2[['studying_help', 'AgeRange']].groupby(['studying_help', 'AgeRange']).size().to_frame().reset_index()
        value_counts.columns = ['studying_help', 'value', 'count']
    else:

        value_counts = df2[['studying_help', value]].groupby(['studying_help', value]).size().to_frame().reset_index()
        value_counts.columns = ['studying_help', 'value', 'count']

 
    unique_values = value_counts['value'].unique()
    color_map = {val: px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)] for i, val in enumerate(unique_values)}

    fig = px.bar(value_counts, x='value', y='count', title=f'Distribution of {value}', color='studying_help',
                 color_discrete_map=color_map, barmode='group')


    fig.update_layout(plot_bgcolor='#fff', paper_bgcolor='#fff')

    return fig
##########################################################
@app.callback(Output('cat-table', 'children'),
                Output('cat-table', 'opened'),
                Input('categorical-table', 'n_clicks'),
                State('cat-table', 'opened'),
                prevent_inital_call = True)
def update_modal_cat(n, opened):

    if ctx.triggered_id is None:
        return [], False

    dft=df2[['gender', 'studying_help']]

    final_df = pd.DataFrame()

    for i in dft.columns.tolist():
        if i == 'studying_help':
            pass
        else:
            dft = dft[['studying_help',i]].groupby(['studying_help', i]).size().to_frame().reset_index()
            dft.columns = ['studying_help', 'value', 'count']
            final_df = pd.concat([final_df, dft[[ 'studying_help','value', 'count']]], ignore_index = True)

    print(final_df)
    return dash_table.DataTable(
        data = final_df.to_dict('records'),
        columns = [{'name':i, 'id':j} for i,j in zip([ 'studying_help','value', 'count'], final_df.columns.tolist())],
        style_as_list_view=True,
        style_cell={'textAlign': 'left'}, 
    ), not opened
    
######################################

@app.callback(Output('num-table', 'children'),
                Output('num-table', 'opened'),
                Input('table-nums', 'n_clicks'),
                State('table-nums', 'opened'),
                prevent_inital_call = True)
def update_modal_cat(n, opened):

    if ctx.triggered_id is None:
        return [], False
    dft= df2[['employment', 'edu_level']]
    final_df = pd.DataFrame()
    for i in dft.columns.tolist():
        if i == 'edu_level':
            pass
        else:
            
            dft = dft[['edu_level',i]].groupby(['edu_level', i]).size().to_frame().reset_index()
            dft.columns = ['edu_level', 'value', 'count']
            final_df = pd.concat([final_df, dft[['edu_level', 'value', 'count']]], ignore_index = True)


    print(final_df)

    return dash_table.DataTable(
        data = final_df.to_dict('records'),
        columns = [{'name':i, 'id':j} for i,j in zip(['edu_level', 'value', 'count'], final_df.columns.tolist())],
        style_as_list_view=True,
        style_cell={'textAlign': 'left'},
    ), not opened




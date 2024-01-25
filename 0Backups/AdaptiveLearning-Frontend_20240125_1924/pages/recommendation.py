import pandas as pd
import dash_mantine_components as dmc
from dash import Input, Output, State, html, ctx
from dash_iconify import DashIconify
from app import app

def create_dropdown(id,label, options_list):
    return dmc.Select(
        id = id,
        label = label,
        data = [{'value':i, 'label': i} for i in options_list],
        value = options_list[0]
    )

df = pd.read_csv(r'C:\Users\Mary\Desktop\AdaptiveLearning-Frontend\data\Survey_data.csv')
custs = pd.read_csv(r'C:\Users\Mary\Desktop\AdaptiveLearning-Frontend\data\Survey_data.csv')

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
                        dmc.Title('Collaborative-Model Based Filtering Recommendation', order = 4, style = {'text-align':'center'}),
                        dmc.Title('Accurancy', order = 4, style = {'text-align':'center'}),
                        html.Img(
                            src = app.get_asset_url('ml images/Coll.png'),
                            style = {'width':'25vw','justify-self':'center'}, 
                        ),
                        html.Img(
                            src = app.get_asset_url('ml images/Acc-Info.png'),
                            style = {'width':'25vw','justify-self':'center'}
                        ),
                        dmc.Text(' OUR EXplanation', style= {'justify-self':'center'}),
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
                                create_dropdown('select-edu-level', 'Educational level', df.edu_level.unique()),
                                create_dropdown('select-employment', 'Employment Status', df.employment.unique()),
                                create_dropdown('select-studying-people', 'preferred study type', df.studying_people.unique()),
                                create_dropdown('select-studying-place', 'Study Place', df.studying_place.unique()),
                                create_dropdown('select-studying-sound', 'Study Sound', df.studying_sound.unique()),
                                create_dropdown('select-studying-time', 'studying time', df.studying_time.unique()),
                                create_dropdown('select-studying-classes', 'Studying Classes', df.studying_classes.unique()),
                                create_dropdown('select-studying-help', 'Support by study difficulty', df.studying_help.unique()),
                                create_dropdown('select-likert-platforms-effectiveness', 'likert_platforms_effectiveness', df.likert_platforms_effectiveness.unique()),
                                create_dropdown('select-studying-help', 'Support by study difficulty', df.studying_help.unique()),
                                create_dropdown('select-trust-ai', 'Trustworthy of AI', df.likert_trust_ai_materials.unique()),
                                create_dropdown('select-relying-recomm-path', 'Relying on recommendation paths', df.likert_open_AI_studyplan.unique()),
                                create_dropdown('select-openness-recomm', 'Openness to recommendation Sys.', df.likert_open_edurecsys.unique()),

                            ]
                        ),
                        dmc.Button(id = 'submit-recomm', children = 'Submit'),

                        dmc.Group(spacing = 'sm', children = [dmc.Title('Accuracy of the Recommendation', order = 3),dmc.ActionIcon(id = 'more-info', color = 'blue', size = 'lg', children = [DashIconify(icon = 'material-symbols:info', width = 24)])]),
                        dmc.Text(size = 'xs', color = 'dimmed', children = 'We want high % of accuracy!'),
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
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import dash_html_components as html
import pandas as pd
import urllib.parse
from caserec.recommenders.item_recommendation.itemknn import ItemKNN
from sqlalchemy import create_engine, text
import dash_bootstrap_components as dbc
from sklearn.metrics.pairwise import cosine_similarity
from backend import retrieve_data
from machinelearning import get_cluster_members, get_similar_users_ratings, get_rating_diff_from_one, get_best_item_id, get_best_material_name




app = dash.Dash(__name__)


params = urllib.parse.quote_plus(r'Driver={ODBC Driver 18 for SQL Server};Server=tcp:adaptive-learning-server.database.windows.net,1433;Database=adaptive_learning_db;Uid=superadmin;Pwd=Poorpassword@2024;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
engine_azure = create_engine(conn_str, echo=True)
connection = engine_azure.connect()


########## BACKEND ML CLUSTERING PART ###############

students_query = text(
    "SELECT id, age, gender, study_field, education_level, employment, study_place "
    "FROM import_student;"
)
students_df = retrieve_data(students_query)


ratings_query = text(
    "SELECT user_id, item_id, rating "
    "FROM rating_materials;"
)
ratings_df = retrieve_data(ratings_query)


merged_df = pd.merge(ratings_df, students_df, how='inner', left_on='user_id', right_on='id')
print("merged_df : !!!!! ", merged_df)

features_for_clustering = ['id','age', 'gender', 'study_field', 'education_level', 'employment', 'study_place']
user_item_matrix = merged_df.pivot_table(index='user_id', columns='item_id', values='rating', fill_value=0)

demographic_data = students_df[features_for_clustering].drop_duplicates().set_index('id')


# Perform a query to fetch effectivness
new_user_query = text(
    "SELECT top 1 * "
    "FROM user_input_data_integer order by New_user_id desc;"
)

new_user_df = retrieve_data(new_user_query)


new_user_demographics = {
    'age': new_user_df.loc[0].Age,
    'gender': str(new_user_df.loc[0].Gender),
    'study_field': str(new_user_df.loc[0].Study_Field),
    'education_level': str(new_user_df.loc[0].Educational_Level),
    'employment': str(new_user_df.loc[0].Employment_Status),
    'study_place': str(new_user_df.loc[0].Study_Place)
}

print("new_user_demo : !!!!! :",new_user_demographics)



cluster_members = get_cluster_members(demographic_data, new_user_demographics)



train_file = 'train_file.dat'  # File to store training data in CaseRecommender format
with open(train_file, 'w') as file:
    for user in cluster_members:
        items_rated = merged_df[merged_df['id'] == user][['item_id', 'rating']].values
        for item, rating in items_rated:
            user_features = merged_df[merged_df['id'] == user][features_for_clustering].drop_duplicates().set_index('id')
            user_demographics_df = pd.DataFrame([new_user_demographics])
            similarity =  int(  cosine_similarity(user_demographics_df , user_demographics_df)[0][0] )
            #file.write(f"{user}::{item}::{rating}\n")
            file.write(f"{user}::{(item)}::{7 -rating}::{similarity}\n")

train = ItemKNN(train_file, similarity_metric='cosine', sep='::')
train.compute()



######## Recommendation Part ###############################

train_file_path = train_file

similar_users_ratings = get_similar_users_ratings(train_file)

rating_diff_from_one = get_rating_diff_from_one(similar_users_ratings)

best_item_id = get_best_item_id(rating_diff_from_one)
#best_rating = rating_diff_from_one[best_item_id]

best_material_name = get_best_material_name(best_item_id)

layout = html.Div([
    html.H2("Here is your recommendation:", style={'textAlign': 'center', 'fontSize': '1.5em'}),
    html.H3("Based on your responses, our recommendation for you is:", style={'textAlign': 'center'}),   
    html.H4(best_material_name, style={'textAlign': 'center', 'color': 'red'}),   
    html.Div(" ", style={'marginTop': '20px'}),
    html.Div(style={'textAlign': 'center'}, children=[
        html.Div("Give us a thumbs up if you find it helpful or not?", style={'marginTop': '20px'}),
    html.Div([
    html.Button('Like👍', id='show-secret'),
    html.Button('Dislike👎', id='show-secret1'),
    html.Div(id='body-div')
]),]),
    html.Div(id='button-output', style={'textAlign': 'center', 'marginTop': '20px'}),
    html.Img(src='..\\assets\\animation.gif', alt="Project Photo", style={'width': '50%', 'margin': 'auto', 'display': 'block'})

])


@callback(
    Output('body-div', 'children'),
    Input('show-secret', 'n_clicks'),
    Input('show-secret1', 'n_clicks')
)
def update_output(clicks1, clicks2):
    if clicks1 :       
        user_id = str(new_user_df.loc[0].New_user_id)
        liked = 1
        user_data = pd.DataFrame({
             'New_user_id': [user_id],
            'Feedback': [liked]})
        user_data.to_sql('Feedback', con=engine_azure, index=False, if_exists='append')
        return "Thank you for your feedback!"
    if clicks2:       
        user_id = str(new_user_df.loc[0].New_user_id)
        liked = 0
        user_data = pd.DataFrame({
             'New_user_id': [user_id],
            'Feedback': [liked]})
        user_data.to_sql('Feedback', con=engine_azure, index=False, if_exists='append')
        return "Thank you for your feedback!"
    else:
        return ""

if __name__ == '__main__':
    app.run(debug=True)

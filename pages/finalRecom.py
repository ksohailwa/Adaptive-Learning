import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_html_components as html
import pandas as pd
import urllib.parse
from sklearn.cluster import KMeans
from caserec.recommenders.item_recommendation.userknn import UserKNN
from caserec.recommenders.item_recommendation.itemknn import ItemKNN
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

########## BACKEND ML CLUSTERING PART ###############

students_query = text(
    "SELECT id, age, gender, study_field, education_level, employment, study_place "
    "FROM import_student;"
)

students_result = connection.execute(students_query)

# Fetch all the rows and convert them to a Pandas DataFrame
students_df = pd.DataFrame(students_result.fetchall(), columns=students_result.keys())
print("students_df : !!!!! ", students_df)

ratings_query = text(
    "SELECT user_id, item_id, rating "
    "FROM rating_materials;"
)

ratings_result = connection.execute(ratings_query)

# Fetch all the rows and convert them to a Pandas DataFrame
ratings_df = pd.DataFrame(ratings_result.fetchall(), columns=ratings_result.keys())
print("ratings_df : !!!!! ", ratings_df)

merged_df = pd.merge(ratings_df, students_df, how='inner', left_on='user_id', right_on='id')
print("merged_df : !!!!! ", merged_df)

features_for_clustering = ['id','age', 'gender', 'study_field', 'education_level', 'employment', 'study_place']
user_item_matrix = merged_df.pivot_table(index='user_id', columns='item_id', values='rating', fill_value=0)

demographic_data = students_df[features_for_clustering].drop_duplicates().set_index('id')
num_clusters = 15  # Adjust the number of clusters as needed
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
user_clusters = kmeans.fit_predict(demographic_data)

# new_user_demographics = {
#     'age': 40,
#     'gender': '2',
#     'study_field': '2',
#     'education_level': '2',
#     'employment': '2',
#     'study_place': '2'
# }

new_user_demographics = {
    'age': random.randint(18, 100),
    'gender': str(random.randint(1, 3)),
    'study_field': str(random.randint(1, 7)),
    'education_level': str(random.randint(1, 3)),
    'employment': str(random.randint(1, 2)),
    'study_place': str(random.randint(1, 2))
}

print("new_user_demo : !!!!! :",new_user_demographics)



num_clusters = 15
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
user_clusters = kmeans.fit_predict(demographic_data)

# Assign the new user to a demographic cluster
new_user_cluster = kmeans.predict([list(new_user_demographics.values())])[0]

cluster_members = demographic_data.index[user_clusters == new_user_cluster]

train_file = 'train_file.dat'  # File to store training data in CaseRecommender format
with open(train_file, 'w') as file:
    for user in cluster_members:
        items_rated = merged_df[merged_df['id'] == user][['item_id', 'rating']].values
        for item, rating in items_rated:
            file.write(f"{user}::{item}::{rating}\n")

train = ItemKNN(train_file, similarity_metric='cosine', sep='::')
train.compute()

######## Reommendation Part ###############################
train_file_path = 'train_file.dat'

similar_users_ratings = {}
with open(train_file_path, 'r') as file:
    for line in file:
        user_id, item_id, rating = map(int, line.strip().split('::'))
        if item_id not in similar_users_ratings:
            similar_users_ratings[item_id] = []
        similar_users_ratings[item_id].append(rating)

# Calculate the absolute difference of each item's average rating from 1
rating_diff_from_one = {}
for item_id, ratings in similar_users_ratings.items():
    average_rating = sum(ratings) / len(ratings)
    diff_from_one = abs(average_rating - 1)
    rating_diff_from_one[item_id] = diff_from_one

# Find the item with the minimum absolute difference from 1

best_item_id = min(rating_diff_from_one, key=rating_diff_from_one.get)
best_rating = rating_diff_from_one[best_item_id]


material_types_map = {
    "Visual Materials": 1,
    "Interactive Materials": 2,
    "Written-Based Materials": 3,
    "Hands-on Materials": 4,
    "Collaborative Materials": 5,
    "Auditory Materials": 6
}

def find_key_by_value(value):
    for key, val in material_types_map.items():
        if val == value:
            return key
    return None



best_material_name = find_key_by_value(best_item_id)
# Print or use the best item and its adjusted average rating
print(f"Best Recommended Item: {best_item_id}")


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
    #html.H4(random_recommendation, style={'textAlign': 'center', 'color': 'red'}),
    html.H4(best_material_name, style={'textAlign': 'center', 'color': 'red'}),
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

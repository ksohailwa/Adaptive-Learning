import urllib.parse
import pandas as pd
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html


from sklearn.cluster import KMeans
from caserec.recommenders.item_recommendation.userknn import UserKNN
from caserec.recommenders.item_recommendation.itemknn import ItemKNN


# Clustering and Classicifation of New User to Cluster
# returns cluter members of new user's cluster

def get_cluster_members(demographic_data, new_user_demographics):
    num_clusters = 15
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    user_clusters = kmeans.fit_predict(demographic_data)
    # Assign the new user to a demographic cluster
    new_user_cluster = kmeans.predict([list(new_user_demographics.values())])[0]
    cluster_members = demographic_data.index[user_clusters == new_user_cluster]
    return cluster_members


def get_similar_users_ratings(train_file_path):
    similar_users_ratings = {}
    with open(train_file_path, 'r') as file:
        for line in file:
            user_id, item_id, rating, similarity = map(int, line.strip().split('::'))
            if item_id not in similar_users_ratings:
                similar_users_ratings[item_id] = []
            similar_users_ratings[item_id].append(rating * similarity) # for weighted sum (not adjusted bc participants were required to assign each rating value)
    return similar_users_ratings


def get_rating_diff_from_one(similar_users_ratings):
    # Calculate the absolute difference of each item's average rating from 1
    rating_diff_from_one = {}
    for item_id, ratings in similar_users_ratings.items():
        average_rating = sum(ratings) / len(ratings)
        diff_from_one = abs(average_rating - 1)
        rating_diff_from_one[item_id] = diff_from_one
    return rating_diff_from_one

def get_best_item_id(rating_diff_from_one):
    # Find the item with the minimum absolute difference from 1
    best_item_id = min(rating_diff_from_one, key=rating_diff_from_one.get)
    return best_item_id



material_types_map = {
    "Visual Materials":         1,
    "Interactive Materials":    2,
    "Written-Based Materials":  3,
    "Hands-on Materials":       4,
    "Collaborative Materials":  5,
    "Auditory Materials":       6
}

def find_key_by_value(value):
    for key, val in material_types_map.items():
        if val == value:
            return key
    return None



#best_material_name = find_key_by_value(best_item_id)
## Print or use the best item and its adjusted average rating
#print(f"Best Recommended Item: {best_item_id}")

def get_best_material_name(best_item_id):
    best_material_name = "best_material_name :" + find_key_by_value(best_item_id)
    return best_material_name


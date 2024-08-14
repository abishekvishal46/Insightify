import pandas as pd
import re
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
# Load datasets
data = pd.read_csv("./course datasets/cleaned_udemy.csv")
data_coursera = pd.read_csv("./course datasets/cleaned_coursera.csv")
data_edx = pd.read_csv("./course datasets/cleaned_edx.csv")

# Load preprocessed data and vectorizers
with open('tfidf_matrix_udemy.pkl', 'rb') as f:
    tfidf_matrix_udemy, tfidf_vectorizer_udemy = pickle.load(f)

with open('feature_matrix_coursera.pkl', 'rb') as f:
    feature_matrix_coursera, vectorizer_coursera = pickle.load(f)

with open('feature_matrix_edx.pkl', 'rb') as f:
    feature_matrix_edx, vectorizer_edx = pickle.load(f)

# You can now use these loaded objects in your recommendation functions


def get_udemy_recommendations(title, min_rating=0):
    # Use the loaded tfidf_matrix_udemy and tfidf_vectorizer_udemy
    matches = data[data['title'].str.contains(title, case=False)]
    if not matches.empty:
        idx1 = matches.index[0]
        sim_scores = list(enumerate(cosine_similarity(tfidf_matrix_udemy[idx1], tfidf_matrix_udemy)[0]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
        course_indices = [score[0] for score in sim_scores]
        recommended_courses = data.iloc[course_indices]

        if 'description' in recommended_courses.columns:
            recommended_courses = recommended_courses[
                recommended_courses['description'].notna() &
                recommended_courses['description'].str.contains(title, case=False)
            ]

        if 'rating' in recommended_courses.columns:
            recommended_courses = recommended_courses[recommended_courses['rating'] >= min_rating]
    else:
        recommended_courses = None

    return recommended_courses


def get_coursera_recommendations(title, min_rating=0, top_n=10):
    input_features_vector = vectorizer_coursera.transform([title])
    similarity_scores = cosine_similarity(feature_matrix_coursera, input_features_vector)
    similar_indices = similarity_scores.argsort(axis=0)[-top_n - 1:-1][::-1]
    top_recommendations = data_coursera.iloc[similar_indices.flatten()]

    if 'rating' in top_recommendations.columns:
        top_recommendations = top_recommendations[top_recommendations['rating'].notna()]
        top_recommendations['rating'] = pd.to_numeric(top_recommendations['rating'], errors='coerce')
        top_recommendations = top_recommendations[top_recommendations['rating'] >= min_rating]
        top_recommendations = top_recommendations.sort_values(by='rating', ascending=False)

    return top_recommendations


def get_edx_recommendations(title, top_n=10):
    input_features_edx_vector = vectorizer_edx.transform([title])
    similarity_scores_edx = cosine_similarity(feature_matrix_edx, input_features_edx_vector)
    similar_indices_edx = similarity_scores_edx.argsort(axis=0)[-top_n - 1:-1][::-1]
    top_edx = data_edx.iloc[similar_indices_edx.flatten()]

    return top_edx

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re


data = pd.read_csv("./course datasets/cleaned_udemy.csv")
data_coursera = pd.read_csv("./course datasets/cleaned_coursera.csv")
data_edx = pd.read_csv("./course datasets/cleaned_edx.csv")

def clean_numeric_strings(value):
    if isinstance(value, str):
        cleaned_value = re.sub(r'[^\d.]', '', value)
    else:
        cleaned_value = str(value)
    return cleaned_value if cleaned_value else '0'



# Preprocess edX data


# Process Udemy recommendations



def get_udemy_recommendations(title, min_rating=0):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    data['description'] = data['description'].fillna('')
    tfidf_matrix = tfidf_vectorizer.fit_transform(data['description'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    matches = data[data['title'].str.contains(title, case=False)]
    if not matches.empty:
        idx1 = matches.index[0]
        sim_scores = list(enumerate(cosine_sim[idx1]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
        course_indices = [score[0] for score in sim_scores]
        recommended_courses = data.iloc[course_indices]

        # Check if the 'description' column exists and has non-NaN values
        if 'description' in recommended_courses.columns:
            recommended_courses = recommended_courses[
                recommended_courses['description'].notna() &
                recommended_courses['description'].str.contains(title, case=False)
                ]

        # Filter based on rating
        if 'rating' in recommended_courses.columns:
            recommended_courses = recommended_courses[
                recommended_courses['rating'] >= min_rating
                ]
    else:
        recommended_courses = None

    return recommended_courses


def get_coursera_recommendations(title, min_rating=0, top_n=10):
    data_coursera['features'] = data_coursera['features'].fillna('')
    vectorizer_coursera = TfidfVectorizer(stop_words='english')
    feature_matrix_coursera = vectorizer_coursera.fit_transform(data_coursera['features'])
    # Convert the input title into a feature vector
    input_features_vector = vectorizer_coursera.transform([title])

    # Compute cosine similarity between the input feature vector and the feature matrix
    similarity_scores = cosine_similarity(feature_matrix_coursera, input_features_vector)

    # Get indices of the top similar courses
    similar_indices = similarity_scores.argsort(axis=0)[-top_n - 1:-1][::-1]

    # Fetch the top recommendations from the data_coursera DataFrame
    top_recommendations = data_coursera.iloc[similar_indices.flatten()]

    # Check if the 'rating' column exists and has non-NaN values
    if 'rating' in top_recommendations.columns:
        top_recommendations = top_recommendations[top_recommendations['rating'].notna()]
        top_recommendations['rating'] = pd.to_numeric(top_recommendations['rating'], errors='coerce')
        top_recommendations = top_recommendations[top_recommendations['rating'] >= min_rating]

    # Sort by rating in descending order
    top_recommendations = top_recommendations.sort_values(by='rating', ascending=False)

    return top_recommendations


# Process edX recommendations

def get_edx_recommendations(title, top_n=10):
    text_features = ['title', 'summary', 'instructors', 'Level', 'price', 'course_url']
    data_edx['combined_text'] = data_edx[text_features].astype(str).apply(lambda x: ' '.join(x), axis=1)
    vectorizer_edx = TfidfVectorizer(stop_words='english')
    feature_matrix_edx = vectorizer_edx.fit_transform(data_edx['combined_text'])
    # Convert the input title into a feature vector
    input_features_edx_vector = vectorizer_edx.transform([title])

    # Compute cosine similarity between the input feature vector and the feature matrix
    similarity_scores_edx = cosine_similarity(feature_matrix_edx, input_features_edx_vector)

    # Get indices of the top similar courses
    similar_indices_edx = similarity_scores_edx.argsort(axis=0)[-top_n - 1:-1][::-1]

    # Fetch the top recommendations from the data_edx DataFrame
    top_edx = data_edx.iloc[similar_indices_edx.flatten()]

    return top_edx
a =get_udemy_recommendations('python')
print(a)

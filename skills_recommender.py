import pandas as pd
import re
import numpy as np
import faiss
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load datasets
data = pd.read_csv("./course datasets/cleaned_udemy.csv")
data_coursera = pd.read_csv("./course datasets/cleaned_coursera.csv")
data_edx = pd.read_csv("./course datasets/cleaned_edx.csv")

def clean_numeric_strings(value):
    if isinstance(value, str):
        cleaned_value = re.sub(r'[^\d.]', '', value)
    else:
        cleaned_value = str(value)
    return cleaned_value if cleaned_value else '0'

# Preprocess data
data['description'] = data['description'].fillna('')
data_coursera['features'] = data_coursera['features'].fillna('')
text_features = ['title', 'summary', 'instructors', 'Level', 'price', 'course_url']
data_edx['combined_text'] = data_edx[text_features].astype(str).apply(lambda x: ' '.join(x), axis=1)

# TF-IDF Vectorization
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix_udemy = tfidf_vectorizer.fit_transform(data['description'])
tfidf_matrix_coursera = tfidf_vectorizer.fit_transform(data_coursera['features'])
tfidf_matrix_edx = tfidf_vectorizer.fit_transform(data_edx['combined_text'])

# FAISS Index Creation
def create_faiss_index(tfidf_matrix):
    index = faiss.IndexFlatL2(tfidf_matrix.shape[1])
    faiss_index = faiss.IndexIDMap(index)
    faiss_index.add_with_ids(tfidf_matrix.toarray(), np.array(range(0, tfidf_matrix.shape[0])))
    return faiss_index

faiss_index_udemy = create_faiss_index(tfidf_matrix_udemy)
faiss_index_coursera = create_faiss_index(tfidf_matrix_coursera)
faiss_index_edx = create_faiss_index(tfidf_matrix_edx)

# Recommendation Functions
def get_faiss_recommendations(title, faiss_index, tfidf_matrix, data, top_n=10, min_rating=0):
    matches = data[data['title'].str.contains(title, case=False)]
    if not matches.empty:
        idx1 = matches.index[0]
        D, I = faiss_index.search(tfidf_matrix[idx1:idx1+1].toarray(), top_n)
        recommended_courses = data.iloc[I.flatten()]

        if 'rating' in recommended_courses.columns:
            recommended_courses = recommended_courses[recommended_courses['rating'].notna()]
            recommended_courses['rating'] = pd.to_numeric(recommended_courses['rating'], errors='coerce')
            recommended_courses = recommended_courses[recommended_courses['rating'] >= min_rating]

        return recommended_courses
    else:
        return None

def get_udemy_recommendations(title, min_rating=0, top_n=10):
    return get_faiss_recommendations(title, faiss_index_udemy, tfidf_matrix_udemy, data, top_n, min_rating)

def get_coursera_recommendations(title, min_rating=0, top_n=10):
    return get_faiss_recommendations(title, faiss_index_coursera, tfidf_matrix_coursera, data_coursera, top_n, min_rating)

def get_edx_recommendations(title, top_n=10):
    return get_faiss_recommendations(title, faiss_index_edx, tfidf_matrix_edx, data_edx, top_n)

# Example Usage
title = "C#"
print("Udemy Recommendations:")
print(get_udemy_recommendations(title))

print("Coursera Recommendations:")
print(get_coursera_recommendations(title))

print("edX Recommendations:")
print(get_edx_recommendations(title))

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

'''input text should be (text=[resume,job_description])
where resume,job_description are strings

'''


def calculate_match_percentage(texts):
    if len(texts) != 2:
        raise ValueError("Input list must contain exactly two text documents.")

    cv = CountVectorizer()
    count_matrix = cv.fit_transform(texts)
    similarity_matrix = cosine_similarity(count_matrix)
    match_percentage = similarity_matrix[0][1] * 100

    return round(match_percentage, 2)
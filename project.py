import pandas as pd
from fuzzywuzzy import process

# Load the dataset from CSV
def load_project_data(filename):
    try:
        return pd.read_csv(filename)
    except pd.errors.ParserError as e:
        print(f"Error loading CSV file: {e}")
        return None

# Function to find the closest domain match using fuzzy matching
def find_closest_domain(input_domain, available_domains, threshold=80):
    closest_match, score = process.extractOne(input_domain, available_domains)
    if score >= threshold:
        return closest_match
    else:
        return None

# Function to get project ideas by domain and difficulty level
def get_project_ideas(domain, difficulty_level, filename="projects.csv"):
    project_df = load_project_data(filename)
    if project_df is not None:
        available_domains = project_df['domain'].unique()
        matched_domain = find_closest_domain(domain, available_domains)

        if matched_domain:
            filtered_projects = project_df[
                (project_df['domain'] == matched_domain) &
                (project_df['difficulty_level'].str.lower() == difficulty_level.lower())
            ]
            return filtered_projects.to_dict(orient="records")
        else:
            print(f"No close match found for the domain '{domain}'")
            return []
    else:
        return []

# Function to print and save each project idea
def print_and_save_projects(project_df, output_filename):
    if not project_df.empty:
        for index, row in project_df.iterrows():
            print(f"Project Idea: {row['project_idea']}")
            print(f"Description: {row['description']}")
            print(f"Difficulty Level: {row['difficulty_level']}")
            print(f"Estimated Time: {row['estimated_time']}")
            print(f"Prerequisites: {row['prerequisites']}")
            print(f"Tools/Technologies: {row['tools_technologies']}")
            print(f"Learning Outcomes: {row['learning_outcomes']}")
            print("-" * 40)  # Separator between projects

        project_df.to_csv(output_filename, index=False)
        print(f"Filtered project ideas saved to {output_filename}")
    else:
        print("No project ideas found for the specified domain and difficulty level.")

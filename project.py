import pandas as pd


# Load the dataset from CSV
def load_project_data(filename):
    try:
        # Read CSV with proper handling of special characters
        return pd.read_csv(filename)
    except pd.errors.ParserError as e:
        print(f"Error loading CSV file: {e}")
        return None


# Function to get project ideas by domain and difficulty level
def get_project_ideas( domain, difficulty_level):
    project_df = pd.read_csv("projects.csv")
    if project_df is not None:
        # Filter project ideas by domain and difficulty level
        filtered_projects = project_df[
            (project_df['domain'] == domain) & (project_df['difficulty_level'].str.lower() == difficulty_level.lower())
            ]
        dict_of_ideas = filtered_projects.to_dict(orient="records")
        return dict_of_ideas
    else:
        return pd.DataFrame()  # Return an empty DataFrame in case of error


# Function to print and save each project idea
def print_and_save_projects(project_df, output_filename):
    if not project_df.empty:
        # Print each project's details
        for index, row in project_df.iterrows():
            print(f"Project Idea: {row['project_idea']}")
            print(f"Description: {row['description']}")
            print(f"Difficulty Level: {row['difficulty_level']}")
            print(f"Estimated Time: {row['estimated_time']}")
            print(f"Prerequisites: {row['prerequisites']}")
            print(f"Tools/Technologies: {row['tools_technologies']}")
            print(f"Learning Outcomes: {row['learning_outcomes']}")
            print("-" * 40)  # Separator between projects

        # Save the filtered projects to a new CSV file
        project_df.to_csv(output_filename, index=False)
        print(f"Filtered project ideas saved to {output_filename}")
    else:
        print("No project ideas found for the specified domain and difficulty level.")

df = load_project_data("projects.csv")
ideas = get_project_ideas(domain="5G and Beyond",difficulty_level="Easy")
print(ideas)
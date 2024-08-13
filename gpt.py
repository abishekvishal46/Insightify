import openai
import json
import os
#Set up your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')
def GPT(domain):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"""
Generate a JSON roadmap for the domain of {domain} with five levels: Beginner, Intermediate, Advanced, Expert, and Specialized. Each level should include a description and at least 6 curated resources with titles and URLs. Use the exact keys: Beginner, Intermediate, Advanced, Expert, Specialized, and structure as shown:

{{
    "Beginner": {{
        "description": "Description of beginner content.",
        "resources": [
            {{"Title 1": "URL 1"}},
            {{"Title 2": "URL 2"}},
            ...
        ]
    }},
    "Intermediate": {{
        "description": "Description of intermediate content.",
        "resources": [
            {{"Title 1": "URL 1"}},
            
            ...
        ]
    }},
    "Advanced": {{
        "description": "Description of advanced content.",
        "resources": [
            {{"Title 1": "URL 1"}},
            
            ...
        ]
    }},
    "Expert": {{
        "description": "Description of expert content.",
        "resources": [
            {{"Title 1": "URL 1"}},
            
            ...
        ]
    }},
    "Specialized": {{
        "description": "Description of specialized content.",
        "resources": [
            {{"Title 1": "URL 1"}},
            
            ...
        ]
    }}
}} Ensure  5 resources per level.
""" }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1024,  # adjust token limit as needed
        n=1,
        temperature=0.6,  # adjust temperature for creativity
    )

    # Extract the summary from the response
    road_map = response.choices[0].message['content'].strip()


    # Parse the JSON response


    # Get token usage information
    prompt_tokens = response['usage']['prompt_tokens']
    completion_tokens = response['usage']['completion_tokens']
    total_tokens = response['usage']['total_tokens']

    # Calculate the cost
    cost_input = (prompt_tokens / 1000) * 0.0015
    cost_output = (completion_tokens / 1000) * 0.002
    total_cost = cost_input + cost_output


    return road_map
def resume_GPT(resume_text):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"""
Analyze the following resume and provide a dictionary with 'pros' and 'cons'. 
'pros' should list 5 points that make the resume attractive. 
'cons' should list 5 areas for improvement.
'jobs' should list 5 jobs that they can apply based on the resume.

Resume Text:
{resume_text}
Response Format:
{{
    "pros": [list of pros],
    "cons": [list of cons],
     "jobs"
}}
"""}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1024,  # adjust token limit as needed
        n=1,
        temperature=0.6,  # adjust temperature for creativity
    )

    # Extract the summary from the response
    road_map = response.choices[0].message['content'].strip()


    # Parse the JSON response

    # Get token usage information
    prompt_tokens = response['usage']['prompt_tokens']
    completion_tokens = response['usage']['completion_tokens']
    total_tokens = response['usage']['total_tokens']

    # Calculate the cost
    cost_input = (prompt_tokens / 1000) * 0.0015
    cost_output = (completion_tokens / 1000) * 0.002
    total_cost = cost_input + cost_output


    return road_map

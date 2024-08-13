from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import random
from gpt import GPT, resume_GPT
import json
from resume import calculate_match_percentage

app = Flask(__name__)
app.secret_key = "sdfsdhoguhuoshgouhsoughoaiwsejiqwhr"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/roadmap", methods=["GET", "POST"])
def roadmap():
    if request.method == "POST":
        domain_text = request.form.get('domain')

        road_map_str = GPT(domain_text)
        road_map_dict = json.loads(road_map_str)
        temp = ["m1.html", "m2.html"]
        chosen_template = random.choice(temp)
        return render_template(chosen_template, roadmap=road_map_dict)
    return render_template("input.html")


@app.route("/skill_recommendation", methods=["GET", "POST"])
def skill_recommendation():
    if request.method =="POST":
        from skills_recommender import get_udemy_recommendations, get_coursera_recommendations, get_edx_recommendations

        domain_text = request.form.get('domain')
        with open("output.txt", "w") as f:
            f.write(domain_text)

        recs = get_coursera_recommendations(domain_text)
        recs1 = get_udemy_recommendations(domain_text)
        rec2 = get_edx_recommendations(domain_text)
        recs_dic = recs.to_dict(orient='records')
        rec1_dic = recs1.to_dict(orient='records')
        rec2_dic = rec2.to_dict(orient='records')
        return render_template("skills_rec.html", skills = rec1_dic,courses=recs_dic,edx_courses=rec2_dic)
    return render_template("skills_input.html")


@app.route("/resume_extractor", methods=["GET", "POST"])
def resume_extractor():
    if request.method == "POST":
            data = request.get_json()
            job_description = data.get('job_description', '')
            pdf_text = data.get('pdf_text', '')

            response = {
                'success': True,
                'message': 'Text processed successfully',
                'job_description': job_description, # Pass the combined text back in the response
                'pdf_text':pdf_text
            }

            return jsonify(response), 200
    return render_template("resume.html")


@app.route('/points', methods=["POST", "GET"])
def success_page():
    # Get the text value from the query parameter
    text = request.args.get('pdf_text', '')
    job = request.args.get('job_description', '')

    resume_str = resume_GPT(resume_text=text)
    resume_dict = json.loads(resume_str)
    score = calculate_match_percentage([text,job])
    # Render the success template and pass the text value to it
    return render_template('points.html', pros=resume_dict["pros"], cons=resume_dict["cons"],score=score,jobs=resume_dict["jobs"])


@app.route("/project_recommendation", methods=["GET", "POST"])
def project_recommendation():
    if request.method =="POST":
        from project import get_project_ideas
        search_query = request.form.get('search', '')
        difficulty = request.form.get('difficulty', '')
        # Example response data
        response_data = {
            'status': 'success',
            'redirect_url': f'/success_project?search={search_query}&difficulty={difficulty}'  # Include query params
        }
        return jsonify(response_data)
    return render_template("project_input.html")
@app.route("/success_project", methods=["GET", "POST"])
def success_project():
    from project import get_project_ideas
    search_query = request.args.get('search', '')
    difficulty = request.args.get('difficulty', '')
    ideas = get_project_ideas(domain=search_query,difficulty_level=difficulty)
    return render_template("project.html",projects=ideas)

if __name__ == "__main__":
    app.run(debug=True)

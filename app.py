from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

file_path = os.path.join(os.getcwd(), 'data.csv')

# Load the CSV data
df = pd.read_csv(file_path)

# Convert the 'skills' column from a comma-separated string to a list
df['skills'] = df['skills'].apply(lambda x: [skill.strip() for skill in x.split(',')])

# Get all unique skills from the CSV
all_skills = sorted(set(skill for sublist in df['skills'] for skill in sublist))

def find_all_companies(input_skills):
    matches = []
    input_skills = [skill.strip() for skill in input_skills]
    
    for index, row in df.iterrows():
        matched_skills = set(row['skills']).intersection(set(input_skills))
        match_score = len(matched_skills)
        remaining_skills = list(set(row['skills']) - matched_skills)
        
        if match_score > 0:
            matches.append({
                'company_name': row['company_name'],
                'salary': row['salary'],
                'matched_skills': list(matched_skills),
                'remaining_skills': remaining_skills,
                'match_score': match_score
            })

    matches.sort(key=lambda x: (-x['match_score'], x['salary']))
    return matches

@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        input_skills = request.json['skills']
        matched_companies = find_all_companies(input_skills)
        return jsonify({'companies': matched_companies})

@app.route('/skills', methods=['GET'])
def get_skills():
    return jsonify({'skills': all_skills})

if __name__ == '__main__':
    app.run(debug=True)







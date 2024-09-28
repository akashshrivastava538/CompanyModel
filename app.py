from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the CSV data
df = pd.read_csv('data.csv')

# Check if the data is loaded correctly
print("Data loaded:")
print(df)

# Convert the 'skills' column from a comma-separated string to a list
# Here we ensure to strip any extra spaces
df['skills'] = df['skills'].apply(lambda x: [skill.strip() for skill in x.split(',')])  # Split skills by comma and strip spaces

def find_top_companies(input_skills):
    matches = []
    
    # Normalize input skills (remove extra spaces)
    input_skills = [skill.strip() for skill in input_skills]
    
    for index, row in df.iterrows():
        matched_skills = set(row['skills']).intersection(set(input_skills))
        match_score = len(matched_skills)
        
        if match_score > 0:
            matches.append({
                'company_name': row['company_name'],
                'salary': row['salary'],
                'matched_skills': list(matched_skills),
                'match_score': match_score
            })

    # Sort by match score and salary
    matches.sort(key=lambda x: (-x['match_score'], x['salary']))
    return matches[:5]  # Return top 5 matches

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        skills = request.form.get('skills').split(',')
        input_skills = [skill.strip() for skill in skills]  # Normalize input skills
        print(f"Input Skills: {input_skills}")  # Debugging statement
        top_companies = find_top_companies(input_skills)
        print("Top Companies Found:")
        print(top_companies)  # Debugging statement
        return render_template('index.html', companies=top_companies)
    return render_template('index.html', companies=[])

if __name__ == '__main__':
    app.run(debug=True)

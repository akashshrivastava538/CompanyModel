import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

file_path = 'akashshrivastava538/CompanyModel/companies.csv'

# Step 1: Load your CSV data
def load_data(file_path):
    # Assuming the CSV has columns 'Company', 'Skills', and 'CTC'
    data = pd.read_csv(file_path)
    return data

# Step 2: Preprocess the skills and create a mapping of companies to skills
def preprocess_skills(data):
    # Convert skills to lowercase and remove spaces
    data['Skills'] = data['Skills'].str.lower().str.replace(', ', ',')
    return data

# Step 3: Use a simple text vectorizer to convert skills into numerical format
def vectorize_skills(data):
    vectorizer = CountVectorizer(tokenizer=lambda x: x.split(','))
    skill_vectors = vectorizer.fit_transform(data['Skills']).toarray()
    return skill_vectors, vectorizer

# Step 4: Get user skills and match with company skills
def recommend_companies(user_skills, skill_vectors, vectorizer, data, top_n=5):
    # Convert user skills into vector format
    user_vector = vectorizer.transform([user_skills.lower().replace(', ', ',')]).toarray()
    
    # Calculate cosine similarity between user skills and each company's skills
    similarities = cosine_similarity(user_vector, skill_vectors)[0]
    
    # Get top n companies with the highest similarity scores
    indices = similarities.argsort()[-top_n:][::-1]
    
    # Show recommendations
    recommendations = data.iloc[indices][['Company', 'CTC']]
    return recommendations

# Step 5: Main function to load data, preprocess, and recommend companies
def main():
    # Path to your CSV file
    file_path = 'companies_skills_ctc.csv'
    
    # Load data
    data = load_data(file_path)
    
    # Preprocess skills
    data = preprocess_skills(data)
    
    # Vectorize skills
    skill_vectors, vectorizer = vectorize_skills(data)
    
    # Get user input (you can take this as input from the user)
    user_skills = input("Enter your skills separated by commas (e.g., python, java, sql): ")
    
    # Recommend companies based on user skills
    recommendations = recommend_companies(user_skills, skill_vectors, vectorizer, data)
    
    # Print recommended companies and their expected CTC
    print("\nTop Company Recommendations Based on Your Skills:")
    print(recommendations)

# Run the main function
if __name__ == "__main__":
    main()

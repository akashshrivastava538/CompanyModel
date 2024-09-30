from fastapi import FastAPI, Query
from typing import List
import csv

app = FastAPI()

# Load the skills from a CSV file
skills = []

with open('skills.csv', newline='', encoding='utf-8') as csvfile:
    skillreader = csv.reader(csvfile)
    for row in skillreader:
        skills.extend(row)

# Remove duplicates and sort skills for better UX
skills = sorted(set(skills))

@app.get("/autocomplete", response_model=List[str])
def autocomplete(query: str = Query(None, min_length=1)):
    if not query:
        return []
    # Filter skills based on the query (case-insensitive)
    results = [skill for skill in skills if query.lower() in skill.lower()]
    return results[:10]  # Limit the result to top 10 matches

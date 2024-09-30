import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Select from 'react-select'; // Import the react-select component
import './styles.css';  // Import the CSS file

const App = () => {
    const [skills, setSkills] = useState([]);
    const [selectedSkills, setSelectedSkills] = useState([]);
    const [companies, setCompanies] = useState(() => {
        const savedCompanies = localStorage.getItem('companies');
        return savedCompanies ? JSON.parse(savedCompanies) : [];
    });
    const [sortOrder, setSortOrder] = useState('asc');
    const [availableSkills, setAvailableSkills] = useState([]);

    useEffect(() => {
        if (companies.length > 0) {
            localStorage.setItem('companies', JSON.stringify(companies));
        }
    }, [companies]);

    // Fetch available skills from the backend
    useEffect(() => {
        const fetchSkills = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5000/skills'); // New route to get all skills
                setAvailableSkills(response.data.skills.map(skill => ({ label: skill, value: skill })));
            } catch (error) {
                console.error("Error fetching skills:", error);
            }
        };
        fetchSkills();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:5000/', { skills: selectedSkills.map(skill => skill.value) });
            setCompanies(response.data.companies);
        } catch (error) {
            console.error("There was an error fetching the data!", error);
        }
    };

    const handleSort = () => {
        const sortedCompanies = [...companies].sort((a, b) => {
            return sortOrder === 'asc' ? a.salary - b.salary : b.salary - a.salary; 
        });
        setCompanies(sortedCompanies);
        setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    };

    return (
        <div className="container">
            <h1>Find Top Companies Based on Your Skills</h1>
            <form onSubmit={handleSubmit}>
                <label htmlFor="skills">Select Skills:</label>
                <Select
                    isMulti
                    options={availableSkills}
                    value={selectedSkills}
                    onChange={setSelectedSkills}
                    placeholder="Start typing to search for skills"
                    className="skills-select"
                />
                <button type="submit">Submit</button>
            </form>

            {companies.length > 0 ? (
                <>
                    <div className="sorting-controls">
                        <button onClick={handleSort}>
                            Sort by CTC ({sortOrder === 'asc' ? 'High to Low' : 'Low to High'})
                        </button>
                    </div>

                    <h2>Company Matches:</h2>
                    <ul>
                        {companies.map((company, index) => (
                            <li key={index}>
                                <strong>{company.company_name}</strong> - Expected Salary: Rs {company.salary} LPA
                                <br />Matched Skills: {company.matched_skills.join(', ')}
                                <br />Other Required Skills: {company.remaining_skills && company.remaining_skills.length > 0 ? company.remaining_skills.join(', ') : "None"}
                                <br />Match Score: {company.match_score}
                                <br /><a href={`https://www.${company.company_name.toLowerCase()}.com`} className="read-more-link" target="_blank" rel="noopener noreferrer">Apply Now</a>
                            </li>
                        ))}
                    </ul>
                </>
      ) : (
                <p>No matches found. Try different Skills.</p>
            )}
        </div>
    );
};

export default App;












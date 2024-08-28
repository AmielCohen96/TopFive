import React, { useEffect, useState, useContext } from 'react';
import './Matches.css';
import axios from 'axios';
import AuthContext from '../context/AuthContext.js';

const Matches = () => {
    const [matches, setMatches] = useState([]);
    const [filteredMatches, setFilteredMatches] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const { authTokens } = useContext(AuthContext);

    // Function to fetch matches
    const fetchMatches = async () => {
        try {
            const response = await axios.get('http://localhost:8000/matches/', {
                headers: {
                    'Authorization': `Bearer ${authTokens.access}`
                }
            });
            // Sort matches by date (ascending)
            const sortedMatches = response.data.sort((a, b) => new Date(a.match_date) - new Date(b.match_date));
            setMatches(sortedMatches);
            setFilteredMatches(sortedMatches);
            setLoading(false);
        } catch (err) {
            setError(err.message);
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchMatches();
    }, [authTokens]);

    // Filter matches based on date
    const handleFilter = () => {
        const filtered = matches.filter(match => {
            const matchDate = new Date(match.match_date);
            return (!startDate || matchDate >= new Date(startDate)) &&
                   (!endDate || matchDate <= new Date(endDate));
        });
        // Ensure filtered results are also sorted
        setFilteredMatches(filtered.sort((a, b) => new Date(a.match_date) - new Date(b.match_date)));
    };

    if (loading) return <p>Loading...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div className="matches-container">
            <div className="filter-container">
                <input
                    type="date"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                    placeholder="Start Date"
                />
                <input
                    type="date"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                    placeholder="End Date"
                />
                <button onClick={handleFilter}>Filter</button>
            </div>
            <table className="matches-table">
                <thead>
                    <tr>
                        <th>Home Team</th>
                        <th>Away Team</th>
                        <th>League</th>
                        <th>Score</th>
                        <th>Result</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    {filteredMatches.map((match, index) => (
                        <tr key={index} className={match.completed ? 'completed-match' : ''}>
                            <td>{match.home_team.name}</td>
                            <td>{match.away_team.name}</td>
                            <td>{match.league ? match.league.name : 'Unknown League'}</td>
                            <td>{match.completed ? `${match.home_team_score} - ${match.away_team_score}` : "Not Played"}</td>
                            <td>{match.result}</td>
                            <td>{new Date(match.match_date).toLocaleDateString()}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default Matches;

import React, { useEffect, useState, useContext } from 'react';
import './Matches.css';
import axios from 'axios';
import AuthContext from '../context/AuthContext.js';

const Matches = () => {
    const [matches, setMatches] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const { authTokens } = useContext(AuthContext);

    useEffect(() => {
        const fetchMatches = async () => {
            try {
                const response = await axios.get('http://localhost:8000/matches/', {
                    headers: {
                        'Authorization': `Bearer ${authTokens.access}`
                    }
                });
                setMatches(response.data);
                setLoading(false);
            } catch (err) {
                setError(err.message);
                setLoading(false);
            }
        };

        fetchMatches();
    }, [authTokens]);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>{error}</p>;

    return (
        <table className="matches-table">
            <thead>
                <tr>
                    <th>Home Team</th>
                    <th>Away Team</th>
                    <th>Score</th>
                    <th>Date</th>
                </tr>
            </thead>
            <tbody>
                {matches.map((match, index) => (
                    <tr key={index} className={match.completed ? 'completed-match' : ''}>
                        <td>{match.home_team.name}</td>
                        <td>{match.away_team.name}</td>
                        <td>{match.completed ? `${match.home_team_score} - ${match.away_team_score}` : "Not Played"}</td>
                        <td>{new Date(match.match_date).toLocaleDateString()}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default Matches;

// frontend/src/components/LeagueTable.js
import React, { useEffect, useState, useContext } from 'react';
import './LeagueTable.css';
import axios from 'axios';
import AuthContext from '../context/AuthContext.js';

const LeagueTable = () => {
    const [teams, setTeams] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const { authTokens } = useContext(AuthContext);

    useEffect(() => {
        const fetchLeagueTeams = async () => {
            try {
                const response = await axios.get('http://localhost:8000/league-teams/', {
                    headers: {
                        'Authorization': `Bearer ${authTokens.access}`
                    }
                });
                setTeams(response.data);
                setLoading(false);
            } catch (err) {
                setError(err.message);
                setLoading(false);
            }
        };

        fetchLeagueTeams();
    }, [authTokens]);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>{error}</p>;

    return (
        <table className="league-table">
            <thead>
                <tr>
                    <th>Position</th>
                    <th>Team Name</th>
                    <th>Manager Name</th>
                    <th>Points</th>
                </tr>
            </thead>
            <tbody>
                {teams.map((team, index) => (
                    <tr key={index} className={
                        index >= teams.length - 2 ? 'bottom-two' :
                        (index === 3 || index === 7) ? 'border-row' : ''
                    }>
                        <td>{team.position}</td>
                        <td>{team.name}</td>
                        <td>{team.manager_name}</td>
                        <td>{team.points}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default LeagueTable
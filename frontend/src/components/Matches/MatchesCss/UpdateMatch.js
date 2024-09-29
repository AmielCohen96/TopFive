import React, { useState, useContext } from 'react';
import './UpdateMatch.css';
import axios from 'axios';
import AuthContext from '../../../context/AuthContext.js';

const UpdateMatch = ({ matchId }) => {
    const [homeScore, setHomeScore] = useState(0);
    const [awayScore, setAwayScore] = useState(0);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const { authTokens } = useContext(AuthContext);

    const handleSubmit = async () => {
        setLoading(true);
        try {
            await axios.patch(`http://localhost:8000/matches/${matchId}/`, {
                home_team_score: homeScore,
                away_team_score: awayScore,
                completed: true,
            }, {
                headers: {
                    'Authorization': `Bearer ${authTokens.access}`
                }
            });
            alert('Match updated successfully');
        } catch (err) {
            setError(err.message);
            alert('Failed to update match');
        }
        setLoading(false);
    };

    if (loading) return <p>Updating...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div className="update-match">
            <h3>Update Match</h3>
            <input
                type="number"
                value={homeScore}
                onChange={e => setHomeScore(parseInt(e.target.value))}
                placeholder="Home Team Score"
                min="0"
            />
            <input
                type="number"
                value={awayScore}
                onChange={e => setAwayScore(parseInt(e.target.value))}
                placeholder="Away Team Score"
                min="0"
            />
            <button onClick={handleSubmit}>Update Match</button>
        </div>
    );
};

export default UpdateMatch;

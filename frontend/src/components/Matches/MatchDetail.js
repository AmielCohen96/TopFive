import React, { useEffect, useState, useContext } from 'react';
import axios from 'axios';
import AuthContext from '../../context/AuthContext.js';
import { useParams } from 'react-router-dom';
import './MatchesCss/MatchDetail.css'; // Create appropriate CSS for styling

const MatchDetail = () => {
    const { id } = useParams(); // Get the match ID from the URL
    const [match, setMatch] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const { authTokens } = useContext(AuthContext);

    useEffect(() => {
        const fetchMatchDetail = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/matches/${id}/`, {
                    headers: {
                        'Authorization': `Bearer ${authTokens.access}`
                    }
                });
                setMatch(response.data);
                setLoading(false);
            } catch (err) {
                setError(err.message);
                setLoading(false);
            }
        };

        fetchMatchDetail();
    }, [id, authTokens]);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div className="match-detail">
            <h2>Match Details</h2>
            <p><strong>Home Team:</strong> {match.home_team?.name || 'N/A'}</p>
            <p><strong>Away Team:</strong> {match.away_team?.name || 'N/A'}</p>
            <p><strong>League:</strong> {match.league?.name || 'N/A'}</p>
            <p><strong>Score:</strong> {match.completed ? `${match.home_team_score} - ${match.away_team_score}` : "Not Played"}</p>
            <p><strong>Result:</strong> {match.result || 'N/A'}</p>
            <p><strong>Date:</strong> {new Date(match.match_date).toLocaleDateString()}</p>
            <p><strong>Time:</strong> {new Date(match.match_date).toLocaleTimeString()}</p>
            {/* Add more details as needed */}
        </div>
    );
};

export default MatchDetail;

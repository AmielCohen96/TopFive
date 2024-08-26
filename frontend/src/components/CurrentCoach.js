import React, { useEffect, useState, useContext } from 'react';
import axios from 'axios';
import AuthContext from '../context/AuthContext.js';
import './TransferTable.css'; // Use the same CSS as TransferTable for consistent styling

const CurrentCoach = () => {
    const [coach, setCoach] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const { authTokens } = useContext(AuthContext);

    useEffect(() => {
        const fetchCoach = async () => {
            try {
                const response = await axios.get('http://localhost:8000/my-coach/', {
                    headers: {
                        'Authorization': `Bearer ${authTokens.access}`
                    }
                });
                setCoach(response.data);
                setLoading(false);
            } catch (err) {
                setError(err.message);
                setLoading(false);
            }
        };

        fetchCoach();
    }, [authTokens]);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div className="transfers-table-container"> {/* Adds scrollable area with consistent styling */}
            <table className="transfers-table">
                <thead>
                <tr>
                    <th>Role</th>
                    <th>Name</th>
                    <th>Defense</th>
                    <th>Offense</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>Coach</td>
                    <td>{coach.name}</td>
                    <td>{coach.defense}</td>
                    <td>{coach.offense}</td>
                </tr>
                </tbody>
            </table>
        </div>
    );
};

export default CurrentCoach;

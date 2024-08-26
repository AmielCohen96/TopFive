// TransferTable.js
import React, { useEffect, useState, useContext } from 'react';
import axios from 'axios';
import AuthContext from '../context/AuthContext.js';
import './TransferTable.css';

const TransferTable = ({ onBuy }) => {
    const [players, setPlayers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const { authTokens } = useContext(AuthContext);

    useEffect(() => {
        const fetchPlayers = async () => {
            try {
                const response = await axios.get('http://localhost:8000/transfer-players/', {
                    headers: {
                        'Authorization': `Bearer ${authTokens.access}`
                    }
                });
                setPlayers(response.data);
                setLoading(false);
            } catch (err) {
                setError(err.message);
                setLoading(false);
            }
        };

        fetchPlayers();
    }, [authTokens]);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>{error}</p>;

    return (
        <table className="transfers-table">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Age</th>
                    <th>Height</th>
                    <th>Position</th>
                    <th>Team</th>
                    <th>Rating</th>
                    <th>Price</th>
                    <th>Buy</th>
                </tr>
            </thead>
            <tbody>
                {players.map((player) => (
                    <tr key={player.id}>
                        <td>{player.name}</td>
                        <td>{player.age}</td>
                        <td>{player.height}</td>
                        <td>{player.position_name}</td>
                        <td>{player.team ? player.team.name : 'Free Agent'}</td>
                        <td>{player.rating}</td>
                        <td>${player.price}</td>
                        <td><button className="buy-button" onClick={() => onBuy(player)}>Buy</button></td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default TransferTable;

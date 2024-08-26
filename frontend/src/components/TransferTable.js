import React, { useEffect, useState, useContext } from 'react';
import axios from 'axios';
import AuthContext from '../context/AuthContext.js';
import './TransferTable.css';

const TransferTable = ({ onBuy }) => {
    const [players, setPlayers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [sortConfig, setSortConfig] = useState({ key: null, direction: 'ascending' });
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

    const sortedPlayers = [...players].sort((a, b) => {
        if (sortConfig.key) {
            let aValue = a[sortConfig.key];
            let bValue = b[sortConfig.key];

            if (sortConfig.key === 'team') {
                aValue = a.team ? a.team.name : '';
                bValue = b.team ? b.team.name : '';
            }

            if (sortConfig.direction === 'ascending') {
                return aValue > bValue ? 1 : -1;
            } else {
                return aValue < bValue ? 1 : -1;
            }
        }
        return 0;
    });

    const requestSort = (key) => {
        let direction = 'ascending';
        if (sortConfig.key === key && sortConfig.direction === 'ascending') {
            direction = 'descending';
        }
        setSortConfig({ key, direction });
    };

    if (loading) return <p>Loading...</p>;
    if (error) return <p>{error}</p>;

    return (
        <table className="transfers-table">
            <thead>
                <tr>
                    <th onClick={() => requestSort('name')}>Name</th>
                    <th onClick={() => requestSort('age')}>Age</th>
                    <th onClick={() => requestSort('height')}>Height</th>
                    <th onClick={() => requestSort('position_name')}>Position</th>
                    <th onClick={() => requestSort('team')}>Team</th>
                    <th onClick={() => requestSort('rating')}>Rating</th>
                    <th onClick={() => requestSort('price')}>Price</th>
                    <th>Buy</th>
                </tr>
            </thead>
            <tbody>
                {sortedPlayers.map((player) => (
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

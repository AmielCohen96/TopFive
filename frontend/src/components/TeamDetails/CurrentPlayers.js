import React, { useEffect, useState, useContext } from 'react';
import axios from 'axios';
import AuthContext from '../../context/AuthContext.js';
import '../Transfer/TransferCss/TransferTable.css'; // Use the same CSS as TransferTable for consistent styling

const CurrentPlayers = () => {
    const [players, setPlayers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [sortConfig, setSortConfig] = useState({ key: null, direction: 'ascending' });
    const { authTokens } = useContext(AuthContext);

    useEffect(() => {
        const fetchPlayers = async () => {
            try {
                const response = await axios.get('http://localhost:8000/my-players/', {
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
        <div className="transfers-table-container"> {/* Adds scrollable area with consistent styling */}
            <table className="transfers-table">
                <thead>
                    <tr>
                        <th onClick={() => requestSort('name')}>Name</th>
                        <th onClick={() => requestSort('age')}>Age</th>
                        <th onClick={() => requestSort('height')}>Height</th>
                        <th onClick={() => requestSort('position')}>Position</th>
                        <th onClick={() => requestSort('speed')}>Speed</th>
                        <th onClick={() => requestSort('strength')}>Strength</th>
                        <th onClick={() => requestSort('stamina')}>Stamina</th>
                        <th onClick={() => requestSort('shooting3')}>3 Point Shot</th>
                        <th onClick={() => requestSort('shooting2')}>2 Point Shot</th>
                        <th onClick={() => requestSort('jumping')}>Jumping</th>
                        <th onClick={() => requestSort('defense')}>Defense</th>
                        <th onClick={() => requestSort('rating')}>Rating</th>
                        <th onClick={() => requestSort('price')}>Price</th>
                        <th>Status</th> {/* Transfer list status column */}
                        <th>Options</th> {/* Placeholder for options button */}
                    </tr>
                </thead>
                <tbody>
                    {sortedPlayers.map((player) => (
                        <tr key={player.id}>
                            <td>{player.name}</td>
                            <td>{player.age}</td>
                            <td>{player.height}</td>
                            <td>{player.position}</td>
                            <td>{player.speed}</td>
                            <td>{player.strength}</td>
                            <td>{player.stamina}</td>
                            <td>{player.shooting3}</td>
                            <td>{player.shooting2}</td>
                            <td>{player.jumping}</td>
                            <td>{player.defense}</td>
                            <td>{player.rating}</td>
                            <td>${player.price}</td>
                            <td>{player.transfer_list ? "On Transfer List" : "Not for Sale"}</td>
                            <td><button className="options-button">Option</button></td> {/* Options button placeholder */}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default CurrentPlayers;

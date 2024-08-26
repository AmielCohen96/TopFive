import React, { useEffect, useState, useContext } from 'react';
import './Transfers.css';
import axios from 'axios';
import AuthContext from '../context/AuthContext.js';
import { confirmAlert } from 'react-confirm-alert'; // Import confirmAlert
import 'react-confirm-alert/src/react-confirm-alert.css'; // Import confirmAlert styles

const Transfers = () => {
    const [players, setPlayers] = useState([]);
    const [balance, setBalance] = useState(0);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const { authTokens } = useContext(AuthContext);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [playersResponse, balanceResponse] = await Promise.all([
                    axios.get('http://localhost:8000/transfer-players/', {
                        headers: {
                            'Authorization': `Bearer ${authTokens.access}`
                        }
                    }),
                    axios.get('http://localhost:8000/current-balance/', {
                        headers: {
                            'Authorization': `Bearer ${authTokens.access}`
                        }
                    })
                ]);

                setPlayers(playersResponse.data);
                setBalance(balanceResponse.data.balance);
                setLoading(false);
            } catch (err) {
                setError(err.message);
                setLoading(false);
            }
        };

        fetchData();
    }, [authTokens]);

    const handleBuy = (player) => {
        confirmAlert({
            title: 'Confirm Purchase',
            message: `Do you want to buy ${player.name} for $${player.price}?`,
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => handleConfirmBuy(player)
                },
                {
                    label: 'No',
                    onClick: () => console.log('Purchase cancelled')
                }
            ]
        });
    };

    const handleConfirmBuy = async (player) => {
        try {
            const response = await axios.post('http://localhost:8000/buy-player/',
                { player_id: player.id },
                {
                    headers: {
                        'Authorization': `Bearer ${authTokens.access}`
                    }
                }
            );
            alert(response.data.message);
            // Update balance and players after successful purchase
            setBalance(response.data.new_balance);
            setPlayers(players.filter(p => p.id !== player.id));
        } catch (err) {
            alert(err.response?.data?.error || 'An error occurred');
        }
    };

    if (loading) return <p>Loading...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div className="transfers-container">
            <h2 className="transfers-title">Transfers</h2>
            <div className="balance-container">
                <p className="balance-text">Current Balance: ${balance}</p>
            </div>
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
                            <td><button className="buy-button" onClick={() => handleBuy(player)}>Buy</button></td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default Transfers;

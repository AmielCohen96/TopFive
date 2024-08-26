// frontend/src/components/CurrentBalance.js
import React, { useEffect, useState, useContext } from 'react';
import axios from 'axios';
import AuthContext from '../context/AuthContext.js';
import './CurrentBalance.css';

const CurrentBalance = ({ balance, setBalance }) => {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const { authTokens } = useContext(AuthContext);

    useEffect(() => {
        const fetchBalance = async () => {
            try {
                const response = await axios.get('http://localhost:8000/current-balance/', {
                    headers: {
                        'Authorization': `Bearer ${authTokens.access}`
                    }
                });
                setBalance(response.data.balance); // עדכון ה-balance עם הערך החדש
                setLoading(false);
            } catch (err) {
                setError(err.message);
                setLoading(false);
            }
        };

        fetchBalance();
    }, [authTokens, setBalance]);

    if (loading) return <p>Loading balance...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div className="balance-container">
            <p className="balance-text">Current Balance: ${balance}</p>
        </div>
    );
};

export default CurrentBalance;

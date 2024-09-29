// frontend/src/components/Transfers.js
import React, { useState, useContext } from 'react';
import './TransferCss/Transfers.css';
import TransferTable from './TransferTable.js';
import CurrentBalance from './CurrentBalance.js';
import { confirmAlert } from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';
import AuthContext from '../../context/AuthContext.js';
import axios from 'axios';

const Transfers = () => {
    const { authTokens } = useContext(AuthContext);
    const [balance, setBalance] = useState(0);

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
        const response = await axios.post('http://localhost:8000/buy-player/', {
            player_id: player.id
        }, {
            headers: {
                'Authorization': `Bearer ${authTokens.access}`
            }
        });

        if (response.status === 200) {
            // עדכון ה-balance עם הערך החדש מהשרת
            setBalance(response.data.new_balance);

            confirmAlert({
                title: 'Purchase Successful',
                message: `You have successfully purchased ${player.name} for $${player.price}.`,
                buttons: [
                    {
                        label: 'OK',
                        onClick: () => {} // פעולה לסגירת החלון
                    }
                ]
            });
        } else {
            // הודעת שגיאה במקרה של שגיאה מהשרת
            confirmAlert({
                title: 'Purchase Failed',
                message: response.data.error || 'Failed to purchase player. Please try again.',
                buttons: [
                    {
                        label: 'OK',
                        onClick: () => {} // פעולה לסגירת החלון
                    }
                ]
            });
        }

    } catch (error) {
        console.error('Error purchasing player:', error);
        confirmAlert({
            title: 'Error',
            message: 'An error occurred. Please try again later.',
            buttons: [
                {
                    label: 'OK',
                    onClick: () => {} // פעולה לסגירת החלון
                }
            ]
        });
    }
};



    return (
        <div className="transfers-container">
            <div className="header-container">
                <CurrentBalance balance={balance} setBalance={setBalance} />
                <h2 className="transfers-title">Transfers</h2>
            </div>
            <div className="transfers-table-container">
                <TransferTable onBuy={handleBuy} />
            </div>
        </div>
    );
};

export default Transfers;

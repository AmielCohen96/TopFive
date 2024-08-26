import React from 'react';
import './Transfers.css';
import TransferTable from './TransferTable.js';
import CurrentBalance from './CurrentBalance.js';
import { confirmAlert } from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';

const Transfers = () => {
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
        // Logic for confirming the purchase
    };

    return (
        <div className="transfers-container">
            <div className="header-container">
                <CurrentBalance />
                <h2 className="transfers-title">Transfers</h2>
            </div>
            <div className="transfers-table-container">
                <TransferTable onBuy={handleBuy} />
            </div>
        </div>
    );
};

export default Transfers;

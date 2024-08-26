// frontend/src/components/League.js
import React from 'react';
import './League.css';
import LeagueTable from './LeagueTable.js';

const League = () => {
    return (
        <div className="league-container">
            <h2>League Standings</h2>
            <LeagueTable />
        </div>
    );
};

export default League;

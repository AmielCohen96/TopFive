// frontend/src/components/League.js
import React from 'react';
import './League.css';
import LeagueTable from './LeagueTable.js';
import {Link} from "react-router-dom";

const League = () => {
    return (
        <div className="league-container">
            <h2>League Standings</h2>
            <Link to="/matches" className="matches-link">View Matches</Link>
            <LeagueTable />
        </div>
    );
};

export default League;

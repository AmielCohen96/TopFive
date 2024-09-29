import React from 'react';
import './TeamDetailsCss/MyTeam.css';
import CurrentPlayers from './CurrentPlayers.js';
import CurrentCoach from './CurrentCoach.js';

const MyTeam = () => {
    return (
        <div className="my-team-container">
            <h2 className="my-team-title">My Team</h2>
            <CurrentCoach />
            <CurrentPlayers />
        </div>
    );
};

export default MyTeam;

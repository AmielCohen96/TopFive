// import React, { useEffect, useState, useContext } from 'react';
// import './Matches.css';
// import axios from 'axios';
// import AuthContext from '../context/AuthContext.js';
// import { Link } from 'react-router-dom';
//
// const Matches = () => {
//     const [matches, setMatches] = useState([]);
//     const [filteredMatches, setFilteredMatches] = useState([]);
//     const [loading, setLoading] = useState(true);
//     const [error, setError] = useState(null);
//     const [startDate, setStartDate] = useState('');
//     const [endDate, setEndDate] = useState('');
//     const { authTokens } = useContext(AuthContext);
//
//     // Function to fetch matches
//     const fetchMatches = async () => {
//         try {
//             const response = await axios.get('http://localhost:8000/matches/', {
//                 headers: {
//                     'Authorization': `Bearer ${authTokens.access}`
//                 }
//             });
//
//             console.log(response.data);  // Log API response to ensure fields are present
//
//             // Sort matches by date (ascending)
//             const sortedMatches = response.data.sort((a, b) => new Date(a.match_date) - new Date(b.match_date));
//             setMatches(sortedMatches);
//             setFilteredMatches(sortedMatches);
//             setLoading(false);
//         } catch (err) {
//             setError(err.message);
//             setLoading(false);
//         }
//     };
//
//     // Fetch matches on mount and set up polling
//     useEffect(() => {
//         fetchMatches(); // Fetch initially
//
//         const intervalId = setInterval(() => {
//             fetchMatches();
//         }, 30000); // Fetch every 30 seconds
//
//         return () => clearInterval(intervalId); // Cleanup on unmount
//     }, [authTokens]);
//
//     // Filter matches based on date
//     const handleFilter = () => {
//         const filtered = matches.filter(match => {
//             const matchDate = new Date(match.match_date);
//             return (!startDate || matchDate >= new Date(startDate)) &&
//                    (!endDate || matchDate <= new Date(endDate));
//         });
//         // Ensure filtered results are also sorted
//         setFilteredMatches(filtered.sort((a, b) => new Date(a.match_date) - new Date(b.match_date)));
//     };
//
//     if (loading) return <p>Loading...</p>;
//     if (error) return <p>{error}</p>;
//
//     return (
//         <div className="matches-page">
//             <div className="header-container">
//                 <Link to="/league" className="back-link">Back to League Table</Link>
//                 <div className="filter-container">
//                     <input
//                         type="date"
//                         value={startDate}
//                         onChange={(e) => setStartDate(e.target.value)}
//                     />
//                     <input
//                         type="date"
//                         value={endDate}
//                         onChange={(e) => setEndDate(e.target.value)}
//                     />
//                     <button onClick={handleFilter}>Filter</button>
//                 </div>
//             </div>
//             <div className="matches-table-container">
//                 <table className="matches-table">
//                     <thead>
//                         <tr>
//                             <th>Home Team</th>
//                             <th>Away Team</th>
//                             <th>League</th>
//                             <th>Score</th>
//                             <th>Result</th>
//                             <th>Date</th>
//                             <th>Time</th>
//                         </tr>
//                     </thead>
//                     <tbody>
//                         {filteredMatches.map((match, index) => (
//                             <tr key={index} className={match.completed ? 'completed-match' : ''}>
//                                 <td>{match.home_team?.name || 'N/A'}</td>
//                                 <td>{match.away_team?.name || 'N/A'}</td>
//                                 <td>{match.league?.name || 'N/A'}</td>
//                                 <td>{match.completed ? `${match.home_team_score} - ${match.away_team_score}` : "Not Played"}</td>
//                                 <td>{match.result || 'N/A'}</td>
//                                 <td>{new Date(match.match_date).toLocaleDateString()}</td>
//                                 <td>{new Date(match.match_date).toLocaleTimeString()}</td>
//                             </tr>
//                         ))}
//                     </tbody>
//                 </table>
//             </div>
//         </div>
//     );
// };
//
// export default Matches;
//

import React, { useEffect, useState, useContext } from 'react';
import './MatchesCss/Matches.css';
import axios from 'axios';
import AuthContext from '../../context/AuthContext.js';
import { Link } from 'react-router-dom';

const Matches = () => {
    const [matches, setMatches] = useState([]);
    const [filteredMatches, setFilteredMatches] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const { authTokens } = useContext(AuthContext);

    // Function to fetch matches
    const fetchMatches = async () => {
        try {
            const response = await axios.get('http://localhost:8000/matches/', {
                headers: {
                    'Authorization': `Bearer ${authTokens.access}`
                }
            });

            console.log(response.data);  // Log API response to ensure fields are present

            // Sort matches by date (ascending)
            const sortedMatches = response.data.sort((a, b) => new Date(a.match_date) - new Date(b.match_date));
            setMatches(sortedMatches);
            setFilteredMatches(sortedMatches);
            setLoading(false);
        } catch (err) {
            setError(err.message);
            setLoading(false);
        }
    };

    // Fetch matches on mount and set up polling
    useEffect(() => {
        fetchMatches(); // Fetch initially

        const intervalId = setInterval(() => {
            fetchMatches();
        }, 30000); // Fetch every 30 seconds

        return () => clearInterval(intervalId); // Cleanup on unmount
    }, [authTokens]);

    // Filter matches based on date
    const handleFilter = () => {
        const filtered = matches.filter(match => {
            const matchDate = new Date(match.match_date);
            return (!startDate || matchDate >= new Date(startDate)) &&
                (!endDate || matchDate <= new Date(endDate));
        });
        // Ensure filtered results are also sorted
        setFilteredMatches(filtered.sort((a, b) => new Date(a.match_date) - new Date(b.match_date)));
    };

    if (loading) return <p>Loading...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div className="matches-page">
            <div className="header-container">
                <Link to="/league" className="back-link">Back to League Table</Link>
                <div className="filter-container">
                    <input
                        type="date"
                        value={startDate}
                        onChange={(e) => setStartDate(e.target.value)}
                        className="date-picker"
                    />
                    <input
                        type="date"
                        value={endDate}
                        onChange={(e) => setEndDate(e.target.value)}
                        className="date-picker"
                    />
                    <button onClick={handleFilter} className="filter-button">Filter</button>
                </div>
            </div>
            <div className="matches-table-container">
                <table className="matches-table">
                    <thead>
                    <tr>
                        <th>#</th>
                        <th>Home Team</th>
                        <th>Away Team</th>
                        <th>League</th>
                        <th>Score</th>
                        <th>Result</th>
                        <th>Date</th>
                        <th>Time</th>
                        <th>Details</th>
                    </tr>
                    </thead>
                    <tbody>
                    {filteredMatches.map((match, index) => (
                        <tr key={index} className={match.completed ? 'completed-match' : ''}>
                            <td>{index + 1}</td>
                            <td>{match.home_team?.name || 'N/A'}</td>
                            <td>{match.away_team?.name || 'N/A'}</td>
                            <td>{match.league?.name || 'N/A'}</td>
                            <td>{match.completed ? `${match.home_team_score} - ${match.away_team_score}` : "Not Played"}</td>
                            <td>{match.result || 'N/A'}</td>
                            <td>{new Date(match.match_date).toLocaleDateString()}</td>
                            <td>{new Date(match.match_date).toLocaleTimeString()}</td>
                            <td><Link to={`/matches/${match.id}`} className="details-link">View Details</Link></td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default Matches;

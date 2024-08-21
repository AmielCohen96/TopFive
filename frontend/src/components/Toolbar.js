// import React from 'react';
// import {Link, useNavigate} from 'react-router-dom';
// import axios from 'axios';
//
//
// const Toolbar = ({ isLoggedIn, setIsLoggedIn }) => {
//     const navigate = useNavigate();
//
//     const handleLogout = async () => {
//         try {
//             const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
//
//             // Proceed with logout even if CSRF token is not found
//             if (csrfToken) {
//                 await axios.post('http://localhost:8000/logout/', {}, {
//                     headers: {
//                         'X-CSRFToken': csrfToken,
//                     },
//                 });
//             } else {
//                 console.warn('CSRF token not found. Attempting to log out without it.');
//             }
//
//             setIsLoggedIn(false);
//             navigate('/', { state: { message: 'You have been logged out successfully.' } });
//         } catch (error) {
//             console.error('Logout failed:', error);
//         }
//     };
//
//     return (
//         <div className="toolbar">
//             <nav className="toolbar">
//                 <ul className="toolbar-nav">
//                     <li className="nav-item"><a href="/home">Home</a></li>
//                     <li className={`nav-item ${!isLoggedIn && 'disabled'}`}><a href="/my-team">My Team</a></li>
//                     <li className={`nav-item ${!isLoggedIn && 'disabled'}`}><a href="/league">League</a></li>
//                     <li className={`nav-item ${!isLoggedIn && 'disabled'}`}><a href="/statistics">Statistics</a></li>
//                     <li className="nav-item">
//                         {isLoggedIn ? (
//                             <button onClick={handleLogout} className="auth-button">Logout</button>
//                         ) : (
//                             <button onClick={() => window.location.href = '/login'}
//                                     className="auth-button">Login</button>
//
//
//                         )}
//                     </li>
//                 </ul>
//             </nav>
//
//         </div>
//     );
// };
//
// export default Toolbar;


// Toolbar.js

import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Toolbar.css';

const Toolbar = ({ isLoggedIn, setIsLoggedIn }) => {
    const navigate = useNavigate();

    const handleLogout = async () => {
        try {
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

            if (csrfToken) {
                await axios.post('http://localhost:8000/logout/', {}, {
                    headers: { 'X-CSRFToken': csrfToken },
                });
            } else {
                console.warn('CSRF token not found. Attempting to log out without it.');
            }

            setIsLoggedIn(false);
            navigate('/',{ state: { message: 'You have been logged out successfully.' } });
        } catch (error) {
            console.error('Logout failed:', error);
        }
    };

    return (
        <div className="toolbar">
            <nav className="toolbar">
                <ul className="toolbar-nav">
                    <li className="nav-item"><Link to="/">Home</Link></li>
                    {isLoggedIn && (
                        <>
                            <li className="nav-item"><Link to="/my-team">My Team</Link></li>
                            <li className="nav-item"><Link to="/league">League</Link></li>
                            <li className="nav-item"><Link to="/statistics">Statistics</Link></li>
                        </>
                    )}
                    <li className="nav-item">
                        {isLoggedIn ? (
                            <button onClick={handleLogout} className="auth-button">Logout</button>
                        ) : (
                            <>
                                <button onClick={() => navigate('/login')} className="auth-button">Login</button>
                                <button onClick={() => navigate('/signup')} className="auth-button">Sign Up</button>
                            </>

                        )}
                    </li>
                </ul>
            </nav>
        </div>
    );
};

export default Toolbar;




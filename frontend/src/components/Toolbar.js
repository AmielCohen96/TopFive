import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import AuthContext from '../context/AuthContext.js';
import './Toolbar.css';

const Toolbar = () => {
    const { isLoggedIn, logoutUser } = useContext(AuthContext);
    const navigate = useNavigate();

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
                            <button onClick={logoutUser} className="auth-button">Logout</button>
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

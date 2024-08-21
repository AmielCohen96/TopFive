import React, { useState } from 'react';
import './Login.css';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';

const Login = ({ setIsLoggedIn }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const location = useLocation();
    const { message } = location.state || {};

    const handleUsernameChange = (event) => {
        setUsername(event.target.value);
    };

    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const response = await axios.post('http://localhost:8000/login/', {
                username,
                password,
            });

            if (response.data.success) {
                setIsLoggedIn(true);
                navigate('/home');
            } else {
                setError('Invalid username or password');
            }
        } catch (error) {
            console.error('Login failed:', error);
            setError('Login failed. Please try again.');
        }
    };

    const handleSignUp = () => {
        navigate('/signup');
    };

    return (
        <div className="login-container">
            <h2>Login</h2>
            {message && <p className="success-message">{message}</p>}
            <div className="input-container">
                <span>Username </span>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={handleUsernameChange}
                />
            </div>
            <div className="input-container">
                <span>Password </span>
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={handlePasswordChange}
                />
            </div>
            <div className="button-container">
                <button onClick={handleSubmit}>Sign In</button>
                <button onClick={handleSignUp}>Sign Up</button>
            </div>
            {error && <p className="error-message">{error}</p>}
        </div>
    );
};

export default Login;


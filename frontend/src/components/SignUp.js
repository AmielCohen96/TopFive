import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {Link, Navigate, useNavigate} from 'react-router-dom';
import './SignUp.css';

const SignUp = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [password2, setPassword2] = useState('');
    const [email, setEmail] = useState('');
    const [firstName, setName] = useState('');
    const [lastName, setLastName] = useState('');
    const [teamName, setTeamName] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);
    const [signingUp, setSigningUp] = useState(false);
    const [csrfToken, setCsrfToken] = useState('');
    const navigate = useNavigate(); // Add this line

    const handleUsernameChange = (event) => setUsername(event.target.value);
    const handlePasswordChange = (event) => setPassword(event.target.value);
    const handlePassword2Change = (event) => setPassword2(event.target.value);
    const handleEmailChange = (event) => setEmail(event.target.value);
    const handleNameChange = (event) => setName(event.target.value);
    const handleLastNameChange = (event) => setLastName(event.target.value);
    const handleTeamNameChange = (event) => setTeamName(event.target.value);

    const validateForm = () => {
        if (!username) {
            setError('Please enter a username');
            return false;
        }
        if (!password || password.length < 6 || !/\d/.test(password) || !/[a-zA-Z]/.test(password)) {
            setError('Password must be at least 6 characters long and include both letters and numbers');
            return false;
        }
        if (password2 !== password) {
            setError('Password must be same');
            return false;
        }
        if (!email || !/\S+@\S+\.\S+/.test(email)) {
            setError('Please enter a valid email address');
            return false;
        }
        if (!firstName) {
            setError('Please enter your name');
            return false;
        }
        if (!lastName) {
            setError('Please enter your last name');
            return false;
        }
        if (!teamName) {
            setError('Please enter your team name');
            return false;
        }
        return true;
    };

    useEffect(() => {
        axios.get('http://localhost:8000/get-csrf-token/')
            .then(response => {
                setCsrfToken(response.data.csrfToken);
            })
            .catch(error => {
                console.error('Error fetching CSRF token:', error);
            });
    }, []);
const handleSubmit = async (event) => {
    event.preventDefault();
    if (validateForm()) {
        setError('');
        setSigningUp(true);
        try {
            const response = await axios.post('http://localhost:8000/signup/', {
                username,
                password,
                password2,
                email,
                first_name: firstName,
                last_name: lastName,
                team_name: teamName
            }, {
                headers: {
                    'X-CSRFToken': csrfToken
                }
            });

            console.log('Signup successful:', response.data);
            setSuccess(true);
            navigate('/login');
        } catch (error) {
            console.error('Signup failed:', error);
            if (error.response && error.response.data) {
                const errorMessages = error.response.data;
                // Extract error messages from backend response and format them
                setError(Object.values(errorMessages).join(' '));
            } else {
                setError('Signup failed. Please try again.');
            }
        } finally {
            setSigningUp(false);
        }
    }
};

    return (
        <div className="signup-container">
            {success ? (
                <div className="success-message">
                    <p>Signup successful! You can now proceed to login.</p>
                    <button><Link to="/login">Back to Login</Link></button>
                </div>
            ) : (
                <>
                    <h2>Sign Up</h2>
                    <form onSubmit={handleSubmit}>
                        <div className="input-container">
                            <span>Username:</span>
                            <input
                                type="text"
                                placeholder="Username"
                                value={username}
                                onChange={handleUsernameChange}
                            />
                        </div>
                        <div className="input-container">
                            <span>Password:</span>
                            <input
                                type="password"
                                placeholder="Password"
                                value={password}
                                onChange={handlePasswordChange}
                            />
                        </div>
                        <div className="input-container">
                            <span>Password Check:</span>
                            <input
                                type="password"
                                placeholder="Password"
                                value={password2}
                                onChange={handlePassword2Change}
                            />
                        </div>
                        <div className="input-container">
                            <span>Email:</span>
                            <input
                                type="email"
                                placeholder="Email"
                                value={email}
                                onChange={handleEmailChange}
                            />
                        </div>
                        <div className="input-container">
                            <span>First Name:</span>
                            <input
                                type="text"
                                placeholder="Name"
                                value={firstName}
                                onChange={handleNameChange}
                            />
                        </div>
                        <div className="input-container">
                            <span>Last Name:</span>
                            <input
                                type="text"
                                placeholder="Last Name"
                                value={lastName}
                                onChange={handleLastNameChange}
                            />
                        </div>
                        <div className="input-container">
                            <span>Team Name:</span>
                            <input
                                type="text"
                                placeholder="Team Name"
                                value={teamName}
                                onChange={handleTeamNameChange}
                            />
                        </div>
                        {error && <p className="error-message">{error}</p>}
                        <button type="submit" disabled={signingUp}>{signingUp ? 'Signing up...' : 'Sign Up'}</button>
                        <button><Link to="/login">Back to Login</Link></button>
                    </form>
                </>
            )}
        </div>
    );
};

export default SignUp;


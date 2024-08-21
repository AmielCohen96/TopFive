import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './SignUp.css';

const SignUp = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [name, setName] = useState(''); // New field
    const [lastName, setLastName] = useState(''); // New field
    const [teamName, setTeamName] = useState(''); // New field
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);
    const [signingUp, setSigningUp] = useState(false);

    const handleUsernameChange = (event) => setUsername(event.target.value);
    const handlePasswordChange = (event) => setPassword(event.target.value);
    const handleEmailChange = (event) => setEmail(event.target.value);
    const handleNameChange = (event) => setName(event.target.value); // New handler
    const handleLastNameChange = (event) => setLastName(event.target.value); // New handler
    const handleTeamNameChange = (event) => setTeamName(event.target.value); // New handler

    const validateForm = () => {
        if (!username) {
            setError('Please enter a username');
            return false;
        }
        if (!password || password.length < 6 || !/\d/.test(password) || !/[a-zA-Z]/.test(password)) {
            setError('Password must be at least 6 characters long and include both letters and numbers');
            return false;
        }
        if (!email || !/\S+@\S+\.\S+/.test(email)) {
            setError('Please enter a valid email address');
            return false;
        }
        if (!name) {
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

    const handleSubmit = async (event) => {
    event.preventDefault();
    if (validateForm()) {
        setError('');
        setSigningUp(true);
        try {
            const response = await axios.post('http://localhost:8000/signup/', {
                username,
                password: password, // Change from password1 and password2 to password
                email,
                first_name: name,   // Map name to first_name
                last_name: lastName, // Map lastName to last_name
                team_name: teamName  // Map teamName to team_name
            });
            console.log('Signup successful:', response.data);
            setSuccess(true);
        } catch (error) {
            console.error('Signup failed:', error);
            setError('Signup failed. Please try again.');
        } finally {
            setSigningUp(false);
        }
    }
};


//     const handleSubmit = async (event) => {
//     event.preventDefault();
//     if (validateForm()) {
//         setError('');
//         setSigningUp(true);
//         try {
//             const response = await axios.post('http://localhost:8000/signup/', {
//                 username,
//                 password1: password,
//                 password2: password,
//                 email,
//                 name,
//                 lastName,
//                 teamName
//             });
//             console.log('Signup successful:', response.data);
//             setSuccess(true);
//         } catch (error) {
//             console.error('Signup failed:', error);
//             setError('Signup failed. Please try again.');
//         } finally {
//             setSigningUp(false);
//         }
//     }
// };
//


    return (
        <div className="signup-container">
            {success ? (
                <div className="success-message">
                    <p>Signup successful! You can now proceed to login.</p>
                    <button><Link to="/">Back to Login</Link></button>
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
                            <span>Email:</span>
                            <input
                                type="email"
                                placeholder="Email"
                                value={email}
                                onChange={handleEmailChange}
                            />
                        </div>
                        <div className="input-container">
                            <span>Name:</span>
                            <input
                                type="text"
                                placeholder="Name"
                                value={name}
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

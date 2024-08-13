// App.js

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/Login.js';
import SignUp from './components/SignUp.js';
import BackgroundWrapper from './BackgroundWrapper.js';
import './App.css'; // Import your CSS file


const App = () => {
    return (
        <BackgroundWrapper> {/* Wrap the entire App component with the BackgroundWrapper */}
            <Router>
                <div className="app-container">
                    <Routes>
                        <Route path="/" element={<Login />} />
                        <Route path="/signup" element={<SignUp />} />
                    </Routes>
                </div>
            </Router>
        </BackgroundWrapper>
    );
};

export default App;

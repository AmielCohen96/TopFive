// App.js

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import signUp from './components/signUp';
import './App.css'; // Import your CSS file
import BackgroundWrapper from './BackgroundWrapper'; // Import the BackgroundWrapper component


const App = () => {
    return (
        <BackgroundWrapper> {/* Wrap the entire App component with the BackgroundWrapper */}
            <Router>
                <div className="app-container">
                    <Routes>
                        <Route path="/" element={<Login />} />
                        <Route path="/signup" element={<signUp />} />

                    </Routes>
                </div>
            </Router>
        </BackgroundWrapper>
    );
};

export default App;

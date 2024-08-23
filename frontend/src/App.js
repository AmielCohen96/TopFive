import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import PrivateRoute from './utils/PrivateRouthe.js';
import { AuthProvider } from "./context/AuthContext.js";

import Login from './components/Login.js';
import SignUp from './components/SignUp.js';
import BackgroundWrapper from './BackgroundWrapper.js';
import './App.css';
import Toolbar from './components/Toolbar.js';
import HomePage from './components/HomePage.js';

const App = () => {
    return (
        <Router>
            <BackgroundWrapper>
                <AuthProvider>
                    <div className="app-container">
                        <Toolbar />
                        <Routes>
                            <Route path="/home" element={<HomePage />} />
                            <Route path="/login" element={<Login />} />
                            <Route path="/signup" element={<SignUp />} />
                            <Route
                                path="/home"
                                element={<PrivateRoute element={<HomePage />} />}
                            />
                            {/* Other private routes can be added here */}
                        </Routes>
                    </div>
                </AuthProvider>
            </BackgroundWrapper>
        </Router>
    );
};

export default App;

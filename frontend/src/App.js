// frontend/src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from "./context/AuthContext.js";
import League from "./components/League/League.js";
import Login from './components/Home/Login.js';
import SignUp from './components/Home/SignUp.js';
import BackgroundWrapper from './BackgroundWrapper.js';
import './App.css';
import Toolbar from './components/Home/Toolbar.js';
import HomePage from './components/Home/HomePage.js';
import Transfers from './components/Transfer/Transfers.js'; // ייבוא הקומפוננטה החדשה
import MyTeam from './components/TeamDetails/MyTeam.js';
import Matches from "./components/Matches/Matches.js";
import UpdateMatch from "./components/Matches/MatchesCss/UpdateMatch.js";
import MatchDetail from "./components/Matches/MatchDetail.js";

const App = () => {
    return (
        <Router>
            <BackgroundWrapper>
                <AuthProvider>
                    <div className="app-container">
                        <Toolbar />
                        <Routes>
                            <Route path="/" element={<HomePage />} />
                            <Route path="/login" element={<Login />} />
                            <Route path="/signup" element={<SignUp />} />
                            <Route path="/league" element={<League />} />
                            <Route path="/transfers" element={<Transfers />} />
                            <Route path="/my-team" element={<MyTeam />} />
                            <Route path="/matches" element={<Matches />} />
                            <Route path="/matches/:id" element={<MatchDetail />} />
                            <Route path="/update-match" element={<UpdateMatch />} />

                        </Routes>
                    </div>
                </AuthProvider>
            </BackgroundWrapper>
        </Router>
    );
};

export default App;

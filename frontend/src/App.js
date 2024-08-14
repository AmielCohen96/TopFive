// // App.js
//
// import React, {useState} from 'react';
// import {BrowserRouter as Router, Route, Routes, Navigate} from 'react-router-dom';
// import Login from './components/Login.js';
// import SignUp from './components/SignUp.js';
// import BackgroundWrapper from './BackgroundWrapper.js';
// import './App.css';
// import Toolbar from './components/Toolbar.js';
// import HomePage from "./components/HomePage.js";
//
// const App = () => {
//     const [isLoggedIn, setIsLoggedIn] = useState(false);
//
//     return (
//         <BackgroundWrapper>
//
//             <Router>
//                 <Toolbar isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn}/>
//                 <div className="app-container">
//                     <meta name="csrf-token" content="{{ csrf_token }}"/>
//                     <Routes>
//                         <Route path="/" element={<HomePage />} />
//                         <Route path="/login" element={<Login setIsLoggedIn={setIsLoggedIn} />} />
//                         <Route path="/signup" element={<SignUp />} />
//                         <Route path="*" element={<Navigate to="/" />} />
//                     </Routes>
//                 </div>
//             </Router>
//         </BackgroundWrapper>
//     );
// };
//
// export default App;
//
//
//
//
//
//
//

// App.js

import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './components/Login.js';
import SignUp from './components/SignUp.js';
import BackgroundWrapper from './BackgroundWrapper.js';
import './App.css';
import Toolbar from './components/Toolbar.js';
import HomePage from './components/HomePage.js';

const App = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    return (
        <BackgroundWrapper>
            <Router>
                <div className="app-container">
                    <meta name="csrf-token" content="{{ csrf_token }}" />
                    <Toolbar isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} />
                    <Routes>
                        <Route path="/" element={<HomePage />} />
                        <Route path="/login" element={<Login setIsLoggedIn={setIsLoggedIn} />} />
                        <Route path="/signup" element={<SignUp />} />
                        <Route path="*" element={<Navigate to="/" />} />
                    </Routes>
                </div>
            </Router>
        </BackgroundWrapper>
    );
};

export default App;


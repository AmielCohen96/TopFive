import { createContext, useEffect, useState } from 'react';
import {jwtDecode} from 'jwt-decode';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext();
export default AuthContext;

export const AuthProvider = ({ children }) => {
    const [authTokens, setAuthTokens] = useState(() =>
        localStorage.getItem("authTokens")
            ? JSON.parse(localStorage.getItem("authTokens"))
            : null
    );

    const [user, setUser] = useState(() =>
        localStorage.getItem("authTokens")
            ? jwtDecode(localStorage.getItem("authTokens"))
            : null
    );

    const navigate = useNavigate();

    const loginUser = async (username, password) => {
        const response = await fetch("http://127.0.0.1:8000/token/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username : username,
                password : password,
            }),
        });

        const data = await response.json();

        if (response.status === 200) {
            setAuthTokens(data);
            setUser(jwtDecode(data.access));
            localStorage.setItem("authTokens", JSON.stringify(data));
            console.log("Login successfully")
            navigate("/home");
        } else {
            if (password !== data.password || user !== data.user) {
                console.log("Wrong password or username");
            }
        }
    };

 const registerUser = async (username, password, password2, email, first_name, last_name, team_name) => {
    try {
        const response = await fetch("http://127.0.0.1:8000/signup/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password, password2, email, first_name, last_name, team_name }),
        });

        if (response.status === 201) {
            return null; // No error
        } else {
            const errorData = await response.json();
            // Handle error response from backend
            console.log("Error:", errorData);
            return errorData.detail;
        }
    } catch (error) {
        console.error("Signup error:", error.message);
        // Return the error message for displaying
        return "An unexpected error occurred. Please try again.";
    }
};


    const logoutUser = () => {
        setAuthTokens(null);
        setUser(null);
        localStorage.removeItem("authTokens");
        console.log("You have logged out");

        navigate("/login");


    };

    const isLoggedIn = !!user;  // Use this to determine if the user is logged in

    const ContextData = {
        user,
        setUser,
        authTokens,
        setAuthTokens,
        registerUser,
        loginUser,
        logoutUser,
        isLoggedIn,
    };

    useEffect(() => {
        if (authTokens) {
            setUser(jwtDecode(authTokens.access));
        }
    }, [authTokens]);

    return (
        <AuthContext.Provider value={ContextData}>
            {children}
        </AuthContext.Provider>
    );
};

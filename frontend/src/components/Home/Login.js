import React, {useContext} from 'react';
import './HomeCss/Login.css';
import AuthContext from "../../context/AuthContext.js";

const Login = () => {

const {loginUser} = useContext(AuthContext);
const handleSubmit = e => {
    e.preventDefault();
    const username = e.target.elements.username.value;
    const password = e.target.elements.password.value;

    if (username.length > 0) {
        loginUser(username, password);
    }

}


    return (
        <div className="login-container">
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <div className="input-container">
                    <span>Username </span>
                    <input type="text" name="username" placeholder="Username" />
                </div>
                <div className="input-container">
                    <span>Password </span>
                    <input type="password" name="password" placeholder="Password" />
                </div>
                <div className="button-container">
                    <button type="submit">Sign In</button>
                </div>
            </form>
        </div>
    );
};

export default Login;
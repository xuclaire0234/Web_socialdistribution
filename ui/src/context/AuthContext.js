/*
2023-02-24
context/AuthContext.js

This code is modified from a tutorial video about Authentication & Refreshing Tokens from Dennis Ivy on 2022-06-02, retrieved on 2023-02-19, to youtube.com
tutorial video here:
https://www.youtube.com/watch?v=2k8NleFjG7I
*/

import { createContext, useState, useEffect } from "react";
import jwt_decode from 'jwt-decode'
import { useNavigate } from "react-router-dom";

const AuthContext = createContext();
export default AuthContext;

export const AuthProvider = ({children}) => {
    //  variable declarations -------------------------------------
    const API_URL = process.env.REACT_APP_API_URL;
    const [ authTokens, setAuthTokens ] = useState(() => localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null);
    const [ user, setUser ] = useState(() => localStorage.getItem('authTokens') ? jwt_decode(localStorage.getItem('authTokens')) : null);
    const [ loading, setLoading ] = useState(true);
    const navigate = useNavigate();

    //  event listners --------------------------------------------
    useEffect(() => {
        if (loading) {
            updateToken();
        }
        // Refresh access token every 59 minutes
        const oneHour = 59 * 60 * 1000;
        let interval = setInterval(() => {
            if (authTokens) {
                updateToken()
            }
        }, oneHour);
        return () => clearInterval(interval);
    }, [authTokens, loading])

    //  async functions -------------------------------------------
    const loginUser = async (e) =>  {
        e.preventDefault();
        let response = null;
        try {
            response = await fetch(`${API_URL}/api/token/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({'username': e.target.username.value, 'password': e.target.password.value})
            });
        } catch (error) {
            console.error('Failed to call authentication. e ');
            console.error(error);
        }
        let data = response ? await response.json() : null;
        if (response && response.status && response.status === 200) {
            setAuthTokens(data);
            setUser(jwt_decode(data.access));
            localStorage.setItem('authTokens', JSON.stringify(data));
            navigate('/');
        } else {
            alert('Opps! Login failed.');
        }
    }

    const logoutUser = () => {
        setAuthTokens(null);
        setUser(null);
        localStorage.removeItem('authTokens');
        navigate('/login');
    }

    const updateToken = async () => {
        let response = null;
        try {
            response = await fetch(`${API_URL}/api/token/refresh/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({'refresh': authTokens?.refresh})
            });
        } catch (error) {
            console.error('Failed to call authentication. e ');
            console.error(error);
        }
        let data = response ? await response.json() : null;
        if (response && response.status && response.status === 200) {
            setAuthTokens(data);
            setUser(jwt_decode(data.access));
            localStorage.setItem('authTokens', JSON.stringify(data));
        } else {
            logoutUser();
        }
        if (loading) {
            setLoading(false);
        }
    }

    //  context ---------------------------------------------------
    let contextData = {
        authTokens: authTokens,
        loginUser: loginUser,
        logoutUser: logoutUser,
        user: user
    };

    // RENDER APP =================================================
    return (
        <AuthContext.Provider value={contextData}>
            {loading ? null : children}
        </AuthContext.Provider>
    );
}

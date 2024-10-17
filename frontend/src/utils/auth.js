// src/auth.js

import axios from '../axios';

const TOKEN_KEY = 'token';

export const AuthService = {
    login(email, password) {
        return axios.post('/login/', { email, password })
        .then(response => {
            const token = response.data.access_token;
            this.setToken(token);
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
            return response.data;
        });
    },

    register(email, password) {
        return axios.post('/register/', { email, password })
        .then(response => {
            const token = response.data.access_token;
            this.setToken(token);
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
            return response.data;
        });
    },

    setToken(token) {
        localStorage.setItem(TOKEN_KEY, token);
    },

    getToken() {
        return localStorage.getItem(TOKEN_KEY);
    },

    removeToken() {
        localStorage.removeItem(TOKEN_KEY);
        delete axios.defaults.headers.common['Authorization'];
    },

    isAuthenticated() {
        const token = this.getToken();
        if (!token) return false;

        try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const currentTime = Date.now() / 1000;
        return payload.exp > currentTime;
        } catch (error) {
        console.error("Invalid token format", error);
        return false;
        }
    },

    logout() {
        localStorage.removeItem('token');
        delete axios.defaults.headers.common['Authorization'];
    }
};

// export function logout() {
//     localStorage.removeItem('token');
//     delete axios.defaults.headers.common['Authorization'];
// }
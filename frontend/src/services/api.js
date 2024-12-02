import axios from 'axios'

const api = axios.create({
    baseURL: process.env.REACT_APP_API_URL,
});

export const login = async (email, password) => {
    return await api.post('/accounts/login', {email, password});
};

export const register = async (username, email, password) => {
    return await api.post('/accounts/register', {email, password});
};

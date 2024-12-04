import axios from 'axios';
import config from '../utils/config';

const api = axios.create({
  baseURL: `${config.backendURL}`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const login = async (email, password) => {
  return await api.post('/accounts/login', { email, password });
};

export const register = async (username, email, password) => {
  return await api.post('/accounts/register', { email, password });
};

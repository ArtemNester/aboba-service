import axios from 'axios';
import config from '../utils/config';
import { setCredentials, logout, setTokens } from '../store/authSlice';
import store from '../store';

const api = axios.create({
  baseURL: `${config.backendURL}`,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const accessToken = store.getState().auth.accessToken;
    if (accessToken) {
      config.headers['Authorization'] = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response && error.response.status === 401) {
      const refreshToken = store.getState().auth.refreshToken;

      if (refreshToken) {
        try {
          const response = await axios.post(`${config.backendURL}/accounts/refresh`, {
            refresh_token: refreshToken,
          });

          const { access, refresh } = response.data;

          store.dispatch(setTokens({ access, refresh }));

          originalRequest.headers['Authorization'] = `Bearer ${access}`;
          return axios(originalRequest);
        } catch (err) {
          store.dispatch(logout());
          window.location.href = '/login';
        }
      }
    }

    return Promise.reject(error);
  },
);

export const login = async (email, password) => {
  const response = await api.post('/accounts/login', { email, password });
  const { access, refresh } = response.data;

  store.dispatch(setCredentials({ access, refresh }));

  return response;
};

export const register = async (username, email, password1, password2) => {
  const response = await api.post('/accounts/register', {
    username,
    email,
    password1,
    password2,
  });
  const { access, refresh } = response.data;

  store.dispatch(setCredentials({ access, refresh }));

  return response;
};

export const logoutUser = async () => {
  try {
    const refreshToken = store.getState().auth.refreshToken;

    if (!refreshToken) {
      throw new Error('No refresh token available.');
    }

    const response = await api.post('/accounts/logout', {
      refresh: refreshToken,
    });

    if (response.status === 205) {
      store.dispatch(logout());
    }

    return response;
  } catch (err) {
    console.error('Logout failed:', err);
    throw err;
  }
};

export default api;

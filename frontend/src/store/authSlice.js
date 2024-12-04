import { createSlice } from '@reduxjs/toolkit';
import { removeToken, getAccessToken, getRefreshToken } from '../utils/tokenManager';

const initialState = {
  accessToken: getAccessToken() || null,
  refreshToken: getRefreshToken() || null,
  isAuthenticated: !!getAccessToken(),
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setCredentials: (state, action) => {
      state.accessToken = action.payload.access;
      state.refreshToken = action.payload.refresh;
      state.isAuthenticated = true;
    },
    logout: (state) => {
      state.accessToken = null;
      state.refreshToken = null;
      state.isAuthenticated = false;
      removeToken();
    },
    setTokens: (state, action) => {
      state.accessToken = action.payload.access;
      state.refreshToken = action.payload.refresh;
    },
  },
});

export const { setCredentials, logout, setTokens } = authSlice.actions;
export default authSlice.reducer;

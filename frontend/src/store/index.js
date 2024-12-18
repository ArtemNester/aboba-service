import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';
import passwordReducer from './passwordSlice';
import videReducer from './videoSlice';

const store = configureStore({
  reducer: {
    auth: authReducer,
    password: passwordReducer,
    video: videReducer,
  },
});

export default store;

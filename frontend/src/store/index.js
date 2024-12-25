import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';
import passwordReducer from './passwordSlice';
import videReducer from './videoSlice';
import commentsReducer from './commentsSlice';

const store = configureStore({
  reducer: {
    auth: authReducer,
    password: passwordReducer,
    video: videReducer,
    comments: commentsReducer,
  },
});

export default store;

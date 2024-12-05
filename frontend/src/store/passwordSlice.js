import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  isPasswordVisible: false,
};

const passwordSlice = createSlice({
  name: 'password',
  initialState,
  reducers: {
    togglePasswordVisibility: (state) => {
      state.isPasswordVisible = !state.isPasswordVisible;
    },
  },
});

export const { togglePasswordVisibility } = passwordSlice.actions;
export default passwordSlice.reducer;

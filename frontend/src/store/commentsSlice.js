import { createSlice } from '@reduxjs/toolkit';

const commentsSlice = createSlice({
  name: 'comments',
  initialState: {
    count: {},
  },
  reducers: {
    addComment: (state, action) => {
      const { postId, comment } = action.payload;
      if (!state.count[postId]) {
        state.count[postId] = 1;
      } else {
        state.count[postId] += 1;
      }
    },
  },
});

export const { addComment } = commentsSlice.actions;
export default commentsSlice.reducer;

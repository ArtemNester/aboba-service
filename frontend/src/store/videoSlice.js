import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

export const fetchVideo = createAsyncThunk('video/fetchVideo', async (_, { rejectWithValue }) => {
  try {
    const response = await axios.get('/memes/rik-roll.mp4', {
      responseType: 'blob',
    });
    return URL.createObjectURL(response.data);
  } catch (error) {
    return rejectWithValue(error.response?.data || 'Ошибка загрузки видео');
  }
});

const videoSlice = createSlice({
  name: 'video',
  initialState: {
    videoUrl: null,
    isLoading: false,
    error: null,
  },
  reducers: {
    clearVideo: (state) => {
      state.videoUrl = null;
      state.isLoading = false;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchVideo.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchVideo.fulfilled, (state, action) => {
        state.videoUrl = action.payload;
        state.isLoading = false;
      })
      .addCase(fetchVideo.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload || 'Ошибка загрузки видео';
      });
  },
});

export const { clearVideo } = videoSlice.actions;
export default videoSlice.reducer;

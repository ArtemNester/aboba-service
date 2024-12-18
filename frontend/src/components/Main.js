import React from 'react';
import { useSelector } from 'react-redux';
import VideoPlayer from './VideoPlayer';
import { Box, Typography } from '@mui/material';
import MemesGallery from './MemesGallery';

const Main = () => {
  const { isAuthenticated } = useSelector((state) => state.auth);

  return (
    <Box
      sx={{
        padding: 4,
        textAlign: 'center',
        height: '100vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
      }}
    >
      {isAuthenticated ? (
        <Box>
          <Typography variant="h4" color="primary">
            Добро пожаловать!
          </Typography>
          <MemesGallery />
        </Box>
      ) : (
        <VideoPlayer />
      )}
    </Box>
  );
};

export default Main;

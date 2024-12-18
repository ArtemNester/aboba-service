import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Button, CircularProgress, Box, Typography } from '@mui/material';
import { fetchVideo, clearVideo } from '../store/videoSlice';
import { Link } from 'react-router-dom';

const VideoPlayer = () => {
  const dispatch = useDispatch();
  const { videoUrl, isLoading, error } = useSelector((state) => state.video);

  const handleFetchVideo = () => {
    dispatch(fetchVideo());
  };

  const handleClearVideo = () => {
    dispatch(clearVideo());
  };

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 2,
        marginTop: 4,
        height: '100vh',
      }}
    >
      {!videoUrl && !isLoading && (
        <Button
          variant="contained"
          color="warning"
          onClick={handleFetchVideo}
          disabled={isLoading}
          sx={{
            fontSize: '1.5rem',
            padding: '20px 40px',
            width: '300px',
          }}
        >
          {isLoading ? <CircularProgress size={24} color="inherit" /> : 'Не нажимай на кнопку'}
        </Button>
      )}

      {videoUrl && (
        <>
          <Typography
            variant="h6"
            sx={{
              color: 'white',
              backgroundColor: 'rgba(0, 0, 0, 0.5)',
              padding: '8px',
              borderRadius: '4px',
              fontSize: { xs: '1rem', sm: '1.25rem', md: '1.5rem' },
              textAlign: 'center',
              width: '100%',
              maxWidth: '600px',
              marginBottom: '16px',
            }}
          >
            Вы зарикролены! Чтобы дальше пользоваться сервисом, вам необходимо
            авторизоваться/зарегистрироваться!
          </Typography>

          <Box
            sx={{
              position: 'relative',
              width: '100%',
              maxWidth: '600px',
            }}
          >
            <video
              src={videoUrl}
              controls
              autoPlay
              style={{ width: '100%', borderRadius: '8px' }}
            />
            <Button variant="outlined" color="secondary" onClick={handleClearVideo}>
              Убрать видео
            </Button>
            <Box sx={{ marginTop: 2 }}>
              <Button
                component={Link}
                to="/login"
                variant="contained"
                color="primary"
                sx={{ marginRight: 2 }}
              >
                Войти
              </Button>
              <Button component={Link} to="/register" variant="contained" color="secondary">
                Зарегистрироваться
              </Button>
            </Box>
          </Box>
        </>
      )}

      {error && <Box sx={{ color: 'red' }}>Ошибка: {error}</Box>}
    </Box>
  );
};

export default VideoPlayer;

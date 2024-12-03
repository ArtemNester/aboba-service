import React, { useState } from 'react';
import { TextField, Button, Box, Typography, Container, CircularProgress } from '@mui/material';
import { toast } from 'react-toastify';
import { login } from '../services/api';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    setLoading(true);
    try {
      const response = await login(email, password);
      if (response.status === 200) toast.success('Вы успешно вошли!');
    } catch (err) {
      if (err.response && err.response.status >= 400)
        toast.error('Неправильный логин или пароль. Попробуйте ещё раз.');
      else toast.error('Что-то пошло не так. Попробуйте ещё раз.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="xs">
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100vh',
        }}
      >
        <Box
          sx={{
            animation: 'frame-animation 3s ease infinite',
            border: '2px solid #9c27b0',
            padding: 4,
            borderRadius: 2,
            width: '100%',
            maxWidth: 400,
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            '&:hover': {
              boxShadow: '0 4px 10px rgba(0, 0, 0, 0.2)',
            },
          }}
        >
          <Typography variant="h4" sx={{ marginBottom: 2, textAlign: 'center' }}>
            Вход
          </Typography>
          <TextField
            label="Email"
            fullWidth
            variant="outlined"
            margin="normal"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={loading}
          />
          <TextField
            label="Пароль"
            type="password"
            fullWidth
            variant="outlined"
            margin="normal"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={loading}
          />
          <Button
            variant="contained"
            color="primary"
            onClick={handleLogin}
            disabled={loading}
            sx={{ marginTop: 2 }}
          >
            {loading ? <CircularProgress size={24} color="inherit" /> : 'Войти'}
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default LoginPage;

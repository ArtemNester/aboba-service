import React, { useState } from 'react';
import { TextField, Button, Box, Typography, Container } from '@mui/material';
import { register } from '../services/api';
import { toast } from 'react-toastify';
import { setToken } from '../utils/tokenManager';
import { useNavigate } from 'react-router-dom';
import PasswordInput from './Inputs/Password/PasswordInput';

const RegisterPage = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password1, setPassword1] = useState('');
  const [password2, setPassword2] = useState('');
  const navigate = useNavigate();

  const handlerRegister = async () => {
    try {
      const response = await register(username, email, password1, password2);
      if (response.status === 201) {
        setToken(response);
        toast.success('Вы успешно зарегистрировались!');
        navigate('/');
      }
    } catch (err) {
      if (err.response && err.response.status === 400) toast.error('Такой email уже существует!');
      else toast.error('Ошибка регистрации. Попробуйте ещё раз.');
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
            Регистрация
          </Typography>
          <TextField
            label="Имя пользователя"
            fullWidth
            variant="outlined"
            margin="normal"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <TextField
            label="Email"
            fullWidth
            variant="outlined"
            margin="normal"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <PasswordInput
            label="Пароль"
            value={password1}
            onChange={(e) => setPassword1(e.target.value)}
          />
          <PasswordInput
            label="Подтвердите пароль"
            value={password2}
            onChange={(e) => setPassword2(e.target.value)}
          />
          <Button variant="contained" color="primary" onClick={handlerRegister}>
            зарегистрироваться
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default RegisterPage;

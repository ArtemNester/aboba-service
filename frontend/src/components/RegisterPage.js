import React, { useState } from 'react';
import { TextField, Button, Box, Typography, Container } from '@mui/material';
import { register } from '../services/api';
import { toast } from 'react-toastify';

const RegisterPage = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    const handlerRegister = async () => {
        if (password !== confirmPassword) {
            toast.error('Пароли не совпадают.')
            return;
        }
        try {
            const response = await register(username, email, password);
            if (response.status === 201) toast.success("Вы успешно зарегистрировались!");
        } catch (err) {
            if (err.response && err.response.status >= 400) toast.error('Такой email уже существует!')
            else toast.error('Ошибка регистрации. Попробуйте ещё раз.')
        }
    };

    return (
        <Container maxWidth='xs'>
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
                    <Typography variant='h4' sx={{ marginBottom: 2, textAlign: 'center' }}>Регистрация</Typography>
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
                        variant='outlined'
                        margin='normal'
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                    <TextField
                        label="Пароль"
                        type="password"
                        fullWidth
                        variant='outlined'
                        margin='normal'
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <TextField
                        label="Подтвердите пароль"
                        type="password"
                        fullWidth
                        variant="outlined"
                        margin="normal"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
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
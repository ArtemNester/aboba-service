import React, {useState } from 'react';
import { TextField, Button, Box, Typography, Container} from '@mui/material';
import { register } from '../services/api';
import { toast } from 'react-toastify';


const RegisterPage = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    const handlerRegister = async () => {
        if (password !== confirmPassword) {
            toast.error('Пароль не совпадают.')
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
                    margin: 8,
                }}
            >
                <Typography variant='h4'>Регистрация</Typography>
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
        </Container>
    )
}

export default RegisterPage;
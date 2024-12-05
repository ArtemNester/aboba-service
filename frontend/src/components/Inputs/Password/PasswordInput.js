/* eslint-disable react/prop-types */
import React from 'react';
import { TextField, InputAdornment, IconButton } from '@mui/material';
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import { useDispatch, useSelector } from 'react-redux';
import { togglePasswordVisibility } from '../../../store/passwordSlice';

const PasswordInput = ({ label, value, onChange }) => {
  const dispatch = useDispatch();
  const isPasswordVisible = useSelector((state) => state.password.isPasswordVisible);

  return (
    <TextField
      label={label}
      type={isPasswordVisible ? 'text' : 'password'}
      fullWidth
      variant="outlined"
      margin="normal"
      value={value}
      onChange={onChange}
      InputProps={{
        endAdornment: (
          <InputAdornment position="end">
            <IconButton onClick={() => dispatch(togglePasswordVisibility())} edge="end">
              {isPasswordVisible ? <VisibilityOffIcon /> : <VisibilityIcon />}
            </IconButton>
          </InputAdornment>
        ),
      }}
    />
  );
};

export default PasswordInput;

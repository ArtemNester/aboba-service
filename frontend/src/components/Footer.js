import React from 'react';
import { Box, Typography, useMediaQuery, useTheme } from '@mui/material';

const Footer = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  return (
    <Box
      sx={{
        background: 'linear-gradient(to right, #2e6783, #607d8b)',
        padding: '20px 0',
        position: 'relative',
        bottom: 0,
        width: '100%',
        marginTop: 'auto',
        textAlign: 'center',
      }}
    >
      <Typography
        variant={isMobile ? 'body2' : 'h6'}
        color="inherit"
        sx={{
          background: 'linear-gradient(to right, #9b59b6, #8e44ad, #e74c3c)', 
          WebkitBackgroundClip: 'text', 
          color: 'transparent',
          fontWeight: 'bold',
          backgroundSize: '200% auto',
          animation: 'gradient-animation 3s ease infinite',
          display: 'inline',
        }}
      >
        by S4toRiX
      </Typography>
      <Typography variant="body2" color="inherit">
        © {new Date().getFullYear()} Aboba. Все права защищены.
      </Typography>
    </Box>
  );
};

export default Footer;

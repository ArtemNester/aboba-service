import React, { useState } from 'react';
import { AppBar, Toolbar, IconButton, Typography, Button, Drawer, List, ListItem, ListItemText, useMediaQuery, useTheme } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { Link } from 'react-router-dom';

const Header = () => {
  const [openDrawer, setOpenDrawer] = useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const toggleDrawer = (open) => () => {
    setOpenDrawer(open);
  };

  return (
    <AppBar position="sticky" sx={{ background: 'linear-gradient(to right, #2e6783, #607d8b)' }}>
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          Aboba
        </Typography>

        {isMobile ? (
          <IconButton edge="start" color="inherit" onClick={toggleDrawer(true)}>
            <MenuIcon />
          </IconButton>
        ) : (
          <div>
            <Button color="inherit" component={Link} to="/login">
              Войти
            </Button>
            <Button color="inherit" component={Link} to="/register">
              Регистрация
            </Button>
          </div>
        )}
      </Toolbar>

      {/* Mobile Drawer */}
      <Drawer anchor="left" open={openDrawer} onClose={toggleDrawer(false)}>
        <List>
          <ListItem button component={Link} to="/login">
            <ListItemText primary="Войти" />
          </ListItem>
          <ListItem button component={Link} to="/register">
            <ListItemText primary="Регистрация" />
          </ListItem>
        </List>
      </Drawer>
    </AppBar>
  );
};

export default Header;

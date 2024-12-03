import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  IconButton,
  Typography,
  Button,
  Drawer,
  List,
  ListItem,
  ListItemText,
  useMediaQuery,
  useTheme,
  Link,
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { Link as RouterLink } from 'react-router-dom';

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
          <Link
            component={RouterLink}
            to="/"
            sx={{
              textDecoration: 'none',
              color: 'white',
              fontWeight: 'bold',
              fontSize: { xs: '1.5rem', sm: '2rem' },
              position: 'relative',
            }}
          >
            Aboba
          </Link>
        </Typography>

        {isMobile ? (
          <IconButton edge="start" color="inherit" onClick={toggleDrawer(true)}>
            <MenuIcon />
          </IconButton>
        ) : (
          <div>
            <Button color="inherit" component={RouterLink} to="/login">
              Войти
            </Button>
            <Button color="inherit" component={RouterLink} to="/register">
              Регистрация
            </Button>
          </div>
        )}
      </Toolbar>

      {/* Mobile Drawer */}
      <Drawer anchor="left" open={openDrawer} onClose={toggleDrawer(false)}>
        <List>
          <ListItem button component={RouterLink} to="/login">
            <ListItemText primary="Войти" />
          </ListItem>
          <ListItem button component={RouterLink} to="/register">
            <ListItemText primary="Регистрация" />
          </ListItem>
        </List>
      </Drawer>
    </AppBar>
  );
};

export default Header;

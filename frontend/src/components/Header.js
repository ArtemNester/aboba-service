import React from 'react';
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
import { useDispatch, useSelector } from 'react-redux';
import { logoutUser } from '../services/api';
import { toast } from 'react-toastify';
import { logout as logoutAction } from '../store/authSlice';

const Header = () => {
  const dispatch = useDispatch();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const { isAuthenticated } = useSelector((state) => state.auth);

  const [openDrawer, setOpenDrawer] = React.useState(false);

  const toggleDrawer = (open) => () => {
    setOpenDrawer(open);
  };

  const handleLogout = async () => {
    try {
      await logoutUser();
      dispatch(logoutAction());
      toast.success('Вы успешно вышли из системы!');
    } catch (err) {
      toast.error('Ошибка при выходе.');
    }
  };

  return (
    <AppBar position="sticky" sx={{ background: 'linear-gradient(to right, #2e6783, #607d8b)' }}>
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          <Link
            component={RouterLink}
            to="/"
            sx={{ textDecoration: 'none', color: 'white', fontWeight: 'bold' }}
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
            {isAuthenticated ? (
              <Button color="inherit" onClick={handleLogout}>
                Выйти
              </Button>
            ) : (
              <>
                <Button color="inherit" component={RouterLink} to="/login">
                  Войти
                </Button>
                <Button color="inherit" component={RouterLink} to="/register">
                  Регистрация
                </Button>
              </>
            )}
          </div>
        )}
      </Toolbar>

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

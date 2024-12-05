import Cookies from 'js-cookie';

const removeToken = () => {
  Cookies.remove('access', { path: '/' });
  Cookies.remove('refresh', { path: '/' });
};

const getAccessToken = () => {
  return Cookies.get('access');
};

const getRefreshToken = () => {
  return Cookies.get('refresh');
};

const setToken = (access, refresh) => {
  Cookies.set('access', access, {
    path: '/',
    secure: true,
    sameSite: 'Strict',
    expires: 15 / 1440,
  });
  Cookies.set('refresh', refresh, { path: '/', secure: true, sameSite: 'Strict', expires: 1 });
};

export { setToken, getAccessToken, getRefreshToken, removeToken };

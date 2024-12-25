import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage';
import Header from './components/Header';
import Footer from './components/Footer';
import { Box } from '@mui/material';
import Main from './components/Main';
import UploadMeme from './components/UploadMeme';
import Comments from './components/Comments';

const App = () => {
  return (
    <Router>
      <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <Header />
        <Box sx={{ flex: 1 }}>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/" element={<Main />} />
            <Route path="/upload" element={<UploadMeme />} />
            <Route path="/posts/:postId" element={<Comments />} />
          </Routes>
        </Box>
        <Footer />
        <ToastContainer
          position="top-right"
          autoClose={5000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
        />
      </Box>
    </Router>
  );
};

export default App;

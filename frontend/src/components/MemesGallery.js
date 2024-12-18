import React, { useEffect, useState } from 'react';
import { Box, Card, CardMedia, CardContent, Typography } from '@mui/material';
import api from '../services/api';
import config from '../utils/config';

const MemesGallery = () => {
  const [memes, setMemes] = useState([]);
  const [hasError, setHasError] = useState(false);

  useEffect(() => {
    const fetchMemes = async () => {
      try {
        const response = await api.get('/posts/get/all/');
        if (response.data && Array.isArray(response.data.results)) {
          setMemes(response.data.results);
        } else {
          setHasError(true);
        }
      } catch (error) {
        console.error('Failed to fetch memes:', error);
        setHasError(true);
      }
    };

    fetchMemes();
  }, []);

  if (hasError || memes.length === 0) {
    console.warn('Memes null!');
    return null;
  }

  return (
    <Box
      sx={{
        height: '100vh',
        overflowY: 'auto',
        padding: 2,
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))',
        gap: 2,
        backgroundColor: '#f9f9f9',
      }}
    >
      {memes.map((meme) => (
        <Card key={meme.post_id} sx={{ boxShadow: 3 }}>
          {meme.file_type === 'video' ? (
            <CardMedia
              component="video"
              controls
              src={`${config.s3URL}/${meme.file_key}`}
              sx={{ height: 200 }}
            />
          ) : (
            <CardMedia
              component="img"
              image={`${config.s3URL}/${meme.file_key}`}
              alt={`Meme by ${meme.user.username}`}
              sx={{ height: 200, objectFit: 'cover' }}
            />
          )}
          <CardContent>
            <Typography variant="h6" noWrap>
              by {meme.user.username}
            </Typography>
          </CardContent>
        </Card>
      ))}
    </Box>
  );
};

export default MemesGallery;

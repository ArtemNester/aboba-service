import React, { useEffect, useState, useRef } from 'react';
import { Box, Card, CardMedia, CardContent, Typography, IconButton, Badge } from '@mui/material';
import { ChatBubbleOutline } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import api from '../services/api';
import config from '../utils/config';

const MemesGallery = () => {
  const [memes, setMemes] = useState([]);
  const [hasError, setHasError] = useState(false);
  const [page, setPage] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const containerRef = useRef(null);
  const navigate = useNavigate();

  const commentsCount = useSelector((state) => state.comments.count);

  const fetchMemes = async (page) => {
    setIsLoading(true);
    try {
      const response = await api.get(`/posts/?page=${page}`);
      if (response.data && Array.isArray(response.data.results)) {
        setMemes((prevMemes) => [...prevMemes, ...response.data.results]);
        if (!response.data.next) {
          setHasMore(false);
        }
      } else {
        setHasError(true);
      }
    } catch (error) {
      console.error('Failed to fetch memes:', error);
      setHasError(true);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (hasMore) {
      fetchMemes(page);
    }
  }, [page]);

  const handleScroll = (e) => {
    const { scrollTop, clientHeight, scrollHeight } = e.target;

    // Check if we are near the bottom of the scroll container
    if (scrollTop + clientHeight >= scrollHeight - 100 && !isLoading && hasMore) {
      setPage((prevPage) => prevPage + 1);
    }
  };

  if (hasError) {
    return <Typography align="center">Failed to load memes. Please try again later.</Typography>;
  }

  return (
    <Box
      ref={containerRef}
      onScroll={handleScroll}
      sx={{
        height: '100vh',
        overflowY: 'auto',
        scrollSnapType: 'y mandatory',
      }}
    >
      {memes.map((meme, index) => (
        <Box
          key={index}
          sx={{
            height: '100vh',
            scrollSnapAlign: 'start',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
          }}
        >
          <Card
            sx={{
              width: '90%',
              maxWidth: '600px',
              height: '80%',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'center',
              alignItems: 'center',
              boxShadow: 3,
            }}
          >
            {meme.file_type === 'video' ? (
              <CardMedia
                component="video"
                controls
                src={`${config.s3URL}/${meme.file_key}`}
                sx={{ height: '100%', width: '100%', objectFit: 'cover' }}
              />
            ) : (
              <CardMedia
                component="img"
                image={`${config.s3URL}/${meme.file_key}`}
                alt={`Meme by ${meme.user.username}`}
                sx={{ height: '100%', width: '100%', objectFit: 'cover' }}
              />
            )}
            <CardContent
              sx={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                width: '100%',
                padding: 2,
              }}
            >
              <Typography variant="h6" noWrap>
                by {meme.user.username}
              </Typography>
              <IconButton onClick={() => navigate(`/posts/${meme.post_id}`)}>
                <Badge badgeContent={commentsCount[meme.post_id] || 0} color="primary">
                  <ChatBubbleOutline />
                </Badge>
              </IconButton>
            </CardContent>
          </Card>
        </Box>
      ))}
      {isLoading && <Typography align="center">Loading more memes...</Typography>}
      {!hasMore && <Typography align="center">No more memes to show.</Typography>}
    </Box>
  );
};

export default MemesGallery;

import React, { useEffect, useState } from 'react';
import { Box, TextField, Button, Typography } from '@mui/material';
import { useDispatch } from 'react-redux';
import { addComment } from '../store/commentsSlice';
import api from '../services/api';
import { useParams } from 'react-router-dom';

const Comments = () => {
  const { postId } = useParams();
  const [comment, setComment] = useState('');
  const [commentsList, setCommentsList] = useState([]);
  const dispatch = useDispatch();

  useEffect(() => {
    const fetchComments = async () => {
      try {
        const response = await api.get(`/posts/?post_id=${postId}`);
        if (response.data && response.data.post_comments) {
          setCommentsList(response.data.post_comments);
          console.log('Received post_comments data: ', response.data.post_comments);
        }
      } catch (error) {
        console.error('Failed to fetch comments:', error);
      }
    };

    fetchComments();
  }, [postId]);
  const handleAddComment = async () => {
    if (comment.trim()) {
      const newComment = {
        content: comment,
        post_id: postId,
      };

      try {
        const response = await api.post('/posts/create/comment/', newComment);
        const addedComment = response.data;

        setCommentsList((prev) => [...prev, addedComment]);

        dispatch(addComment({ postId, comment: addedComment }));

        setComment('');
      } catch (error) {
        console.error('Failed to add comment:', error);
      }
    }
  };

  return (
    <Box
      sx={{
        padding: 2,
        display: 'flex',
        flexDirection: 'column',
        gap: 2,
        alignItems: 'center',
      }}
    >
      <Typography variant="h5">Comments for Post {postId}</Typography>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          gap: 1,
          width: '100%',
          maxWidth: '600px',
        }}
      >
        {commentsList.map((c) => (
          <Typography key={c.id} variant="body1">
            {c.content}
          </Typography>
        ))}
      </Box>
      <TextField
        label="Напишите ваше сообщение..."
        variant="outlined"
        fullWidth
        value={comment}
        onChange={(e) => setComment(e.target.value)}
      />
      <Button variant="contained" onClick={handleAddComment}>
        Добавить комментарий
      </Button>
    </Box>
  );
};

export default Comments;

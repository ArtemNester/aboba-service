import React, { useState } from 'react';
import { Button, Grid, Box } from '@mui/material';
import { toast } from 'react-toastify';
import api from '../services/api';

const UploadMeme = () => {
  const [file, setFile] = useState(null);
  const [fileType, setFileType] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      const mimeType = selectedFile.type;

      if (mimeType.startsWith('image/')) {
        setFileType('image');
      } else if (mimeType.startsWith('video/')) {
        setFileType('video');
      } else {
        toast.error('Ошибка типа файла. Пожалуйста, загрузите картинку или видео');
        setFile(null);
        setFileType('');
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file || !fileType) {
      toast.error('Файл и тип файла обязательны');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('file_type', fileType);

    try {
      const response = await api.post('/posts/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      toast.success(`File uploaded successfully: Post ID ${response.data.post_id}`);
    } catch (error) {
      toast.error('Failed to upload file');
    }
  };

  return (
    <Box sx={{ padding: 2, maxWidth: 500, margin: '0 auto' }}>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <input
              type="file"
              accept="image/*,video/*"
              onChange={handleFileChange}
              style={{ display: 'block', marginTop: '10px' }}
              required
            />
          </Grid>
          <Grid item xs={12}>
            <Button
              type="submit"
              variant="contained"
              color="primary"
              fullWidth
              sx={{ marginTop: 2 }}
            >
              Загрузить мемес
            </Button>
          </Grid>
        </Grid>
      </form>
    </Box>
  );
};

export default UploadMeme;

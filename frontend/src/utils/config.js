const config = {
  backendURL: process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000/api/v1',
  s3URL: process.env.REACT_APP_S3_URL || 'http://localhost:9000/memes',
};

export default config;

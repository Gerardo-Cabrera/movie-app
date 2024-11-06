import axios from 'axios';
import { API_CONFIG } from '@/config';

axios.defaults.baseURL = API_CONFIG.baseURL;

// Set Axios default headers to include the JWT token if it's available
// const token = localStorage.getItem('token');
// if (token) {
//   axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
// }

axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export default axios;

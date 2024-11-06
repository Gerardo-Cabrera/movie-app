import App from '@/App.vue';
import router from '@/router';
import axios from '@/axios';
import { createApp } from 'vue';
//import '@/assets/css/global.css';

// Set Axios default headers to include the JWT token if it's available
const token = localStorage.getItem('token');
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

const app = createApp(App);
app.use(router);
app.mount('#app');

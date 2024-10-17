<template>
    <div class="auth-container">
      <h2 class="auth-title">Login</h2>
      <form @submit.prevent="loginUser" class="auth-form">
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" v-model="email" placeholder="Enter your email" class="auth-input" required />
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" v-model="password" placeholder="Enter your password" class="auth-input" required />
        </div>
        <button type="submit" @click="login" class="auth-button">Login</button>
      </form>
      <p v-if="error" style="color:red;">{{ error }}</p>
      <p class="auth-switch">
        Don't have an account? 
        <router-link to="/register" class="auth-link">Register here</router-link>
      </p>
    </div>
  </template>
  
<script>
  import { AuthService } from '@/utils/auth';
  
  export default {
    data() {
      return {
        email: '',
        password: '',
        error: ''
      };
    },
    methods: {
      async login() {
        try {
          // const response = await axios.post('/login/', {
          //   email: this.email,
          //   password: this.password
          // });
          // localStorage.setItem('token', response.data.token);
          // axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
          await AuthService.login(this.email, this.password);
          this.$router.push({ name: 'MovieSearch' });
        } catch (err) {
          this.error = 'Login failed. Please check your credentials.';
        }
      }
    }
  };
</script>
  
<style scoped>
.auth-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 50px;
}

.auth-title {
  font-size: 28px;
  margin-bottom: 20px;
  color: #333;
}

.auth-form {
  width: 350px;
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

.auth-input {
  width: 100%;
  padding: 12px;
  margin-top: 5px;
  border-radius: 4px;
  border: 1px solid #ccc;
  font-size: 16px;
}

.auth-button {
  padding: 12px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 10px;
}

.auth-button:hover {
  background-color: #45a049;
}

.auth-switch {
  margin-top: 15px;
}

.auth-link {
  color: #2196F3;
  text-decoration: none;
}

.auth-link:hover {
  text-decoration: underline;
}
</style>
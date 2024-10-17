<template>
    <div>
      <h2>Your Favorite Movies</h2>
      <ul v-if="favorites.length">
        <li v-for="movie in favorites" :key="movie.imdb_id">
          <img :src="movie.poster" alt="Poster" width="100" />
          <p>{{ movie.title }} ({{ movie.year }})</p>
          <button @click="viewDetails(movie.imdb_id)">View Details</button>
        </li>
      </ul>
      <p v-else>No favorites added yet.</p>
    </div>
  </template>
  
<script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        favorites: []
      };
    },
    async created() {
      const response = await axios.get('http://localhost:8000/movies/favorites/', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      this.favorites = response.data;
    },
    methods: {
      viewDetails(imdbID) {
        this.$router.push({ name: 'MovieDetail', params: { imdbID } });
      }
    }
  };
</script>
  
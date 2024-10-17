<template>
  <div>
    <h2>Add a Review for {{ movie.Title }}</h2>
    <form @submit.prevent="submitReview">
      <textarea v-model="reviewContent" placeholder="Write your review" required></textarea>
      <label>Rating:</label>
      <input type="number" v-model="rating" min="1" max="10" required />
      <button type="submit">Submit Review</button>
    </form>
    <button @click="goBack">Cancel</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      movie: null,
      reviewContent: '',
      rating: null
    };
  },
  async created() {
    const { imdbID } = this.$route.params;
    const response = await axios.get(`http://localhost:8000/movies/detail/${imdbID}/`);
    this.movie = response.data;
  },
  methods: {
    async submitReview() {
      const { imdbID } = this.$route.params;
      await axios.post(`http://localhost:8000/movies/review/${imdbID}/`, {
        content: this.reviewContent,
        rating: this.rating
      }, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      alert('Review submitted!');
      this.$router.push({ name: 'MovieDetail', params: { imdbID } });
    },
    goBack() {
      this.$router.push({ name: 'MovieDetail', params: { imdbID: this.$route.params.imdbID } });
    }
  }
};
</script>

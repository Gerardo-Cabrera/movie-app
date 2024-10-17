<template>
    <div v-if="isLoading" class="loader">Loading...</div>
    <div v-else-if="movie">
        <h1>{{ movie.original_title }}</h1>
        <img :src="movie.poster_path" alt="Poster" />
        <p><strong>Director:</strong> {{ movie.Director }}</p>
        <p><strong>Year:</strong> {{ movie.Year }}</p>
        <p><strong>IMDB Rating:</strong> {{ movie.imdbRating }}</p>
        <p>{{ movie.Plot }}</p>

        <div v-if="isAuthenticated">
            <button v-if="!isFavorite" @click="addToFavorites">Add to Favorites</button>
            <button v-else @click="removeFromFavorites">Remove from Favorites</button>
        </div>

        <button @click="goBack">Back to Search</button>
    </div>
</template>
  
<script>
  import axios from '../axios';
  import { AuthService } from '@/utils/auth';
  
  export default {
    props: ['movie_id', 'slug'],
    data() {
      return {
        movie: null,
        isFavorite: false,
        isAuthenticated: AuthService.isAuthenticated(),
        isLoading: true
      };
    },
    async created() {
        //const { movie_id } = this.$route.params;
        const { movie_id, slug } = this.$route.params;
        try {
            //const response = await axios.get(`/movies/detail/${movie_id}/`);
            const response = await axios.get(`/movies/detail/${movie_id}/${slug}/`);
            this.movie = response.data;

            if (this.isAuthenticated) {
                await this.checkIfFavorite(movie_id);
            }
        } catch (error) {
            console.error('Error fetching movie details:', error);
        } finally {
            this.isLoading = false;
        }
    },
    methods: {
        async addToFavorites() {
            const { movie_id } = this.$route.params;
            try {
                await axios.post(`/movies/favorites/add/`, { imdb_id: movie_id }, {
                    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
                });
                alert('Added to favorites!');
                this.isFavorite = true;
            } catch (error) {
                console.error('Error adding to favorites:', error);
            }
        },
        async removeFromFavorites() {
            const { movie_id } = this.$route.params;
            try {
                await axios.delete(`/movies/favorites/remove/${movie_id}/`, {
                headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
                });
                alert('Removed from favorites!');
                this.isFavorite = false;
            } catch (error) {
                console.error('Error removing from favorites:', error);
            }
        },
        async checkIfFavorite(movie_id) {
            try {
                const response = await axios.get(`/movies/favorites/${movie_id}/`, {
                headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
                });
                this.isFavorite = response.data.is_favorite;
            } catch (error) {
                console.error('Error checking if favorite:', error);
            }
        },
        goBack() {
            this.$router.push({ name: 'MovieSearch' });
        }
    }
};
</script>

<style scoped>
.loader {
  margin: 20px 0;
  font-size: 18px;
  color: #333;
}
</style>
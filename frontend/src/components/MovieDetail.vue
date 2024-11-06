<template>
    <div v-if="isLoading" class="loader">Loading...</div>
    <div v-else-if="movie" class="movie-detail-container">
        <div class="movie-header">
            <img :src="movie.poster_url" alt="Poster" class="movie-poster" loading="lazy"/>
            <div class="movie-info">
                <h1 class="movie-title">
                    {{ movie.title }}
                    <span class="movie-year">
                        ({{ movie.year }})
                    </span>
                </h1>
                <div class="genres">
                    {{ movie.date }}
                    <span v-if="index !== 0" class="dot"> • </span>
                    <span v-for="(genre, index) in movie.genre_names" :key="index">
                        {{ genre }}<span v-if="index < movie.genre_names.length - 1">, </span>
                    </span>
                    <span v-if="index !== 0" class="dot"> • </span>
                    <span>{{ movie.duration }}</span>
                </div>
                <p class="movie-director"><strong>Director:</strong> {{ movie.Director }}</p>
                <p class="movie-rating"><strong>IMDB Rating:</strong> {{ movie.imdbRating }}</p>
                <p class="movie-plot">{{ movie.Plot }}</p>

                <div v-if="isAuthenticated" class="favorite-actions">
                <button v-if="!isFavorite" class="btn-favorite" @click="addToFavorites">Add to Favorites</button>
                <button v-else class="btn-remove-favorite" @click="removeFromFavorites">Remove from Favorites</button>
                </div>

                <button class="btn-back" @click="goBack">Back to Search</button>
            </div>
        </div>
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
        const { movie_id, slug } = this.$route.params;
        try {
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

.movie-detail-container {
    display: flex;
    align-items: flex-start;
    background-color: #1c1c1c;
    color: #fff;
    padding: 20px;
    border-radius: 10px;
    max-width: 900px;
    margin: auto;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.movie-header {
    display: flex;
    gap: 20px;
    align-items: flex-start;
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    flex-wrap: wrap;
    justify-content: space-around;
}

.movie-poster {
    width: 250px;
    height: auto;
    object-fit: cover;
    border-radius: 8px;
    margin-right: 20px;
}

.movie-info {
    flex: 1;
    color: #ddd;
    max-width: 600px;
    padding: 10px;
}

.movie-title {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 10px;
    color: #ffffff;
}

.movie-meta {
    font-size: 1.1rem;
    margin: 10px 0;
    color: #b5b5b5;
}

.movie-rating {
    font-size: 1.5rem;
    font-weight: bold;
    color: #4caf50;
}

.movie-overview {
    margin: 20px 0;
    font-size: 1rem;
    line-height: 1.5;
}

.movie-year, .movie-director, .movie-plot {
    font-size: 1.1rem;
    margin-bottom: 15px;
    color: #cccccc;
}

.movie-plot {
  line-height: 1.6;
}

.favorite-actions {
  margin-top: 20px;
}

.btn-favorite, .btn-remove-favorite, .btn-back {
  padding: 10px 20px;
  margin-right: 10px;
  border-radius: 25px;
  border: none;
  font-size: 1rem;
  cursor: pointer;
}

.btn-favorite {
  background-color: #ff9800;
  color: white;
}

.btn-remove-favorite {
  background-color: #f44336;
  color: white;
}

.btn-back {
  background-color: #607d8b;
  color: white;
}

.loader {
  margin: 20px 0;
  font-size: 18px;
  color: #333;
}

@media (max-width: 768px) {
  .movie-header {
    flex-direction: column;
    align-items: center;
  }

  .movie-poster {    /*color: #555;*/
    width: 100%;
    max-width: 400px;
  }

  .movie-title {
    text-align: center;
  }

  .movie-info {
    text-align: center;
  }
}
</style>
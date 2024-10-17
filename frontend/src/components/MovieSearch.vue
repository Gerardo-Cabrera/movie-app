<template>
  <div class="search-container">
    <input 
      type="text" 
      v-model="query" 
      placeholder="Search for a movie..." 
      class="search-input"
      @keydown.enter="applyFilter"
    />
    <button :disabled="!hasActiveFilters" @click="applyFilter" class="search-button">Search</button>

    <div class="filters">
      <div>
        <label for="year" class="filter-label">Year: </label>
        <input 
            type="number" 
            v-model="filters.year" 
            placeholder="Min year 1882" 
            class="filter-input" 
            @input="limitYearDigits" 
            @keydown.enter="handleSearch"
            maxlength="4"
            min="1882"
        />
      </div>
      <div>
        <label for="rating" class="filter-label">Rating: </label>
        <input type="number" v-model="filters.rating" step="0.1" min="0" max="10" placeholder="e.g., 8.5" class="filter-input" @keydown.enter="applyFilter"/>
      </div>
      <div>
        <label for="genre" class="filter-label">Genre: </label>
        <select v-model="filters.genre" @change="applyFilter" class="filter-select">
            <option value="">All Genres</option>
            <option v-for="genre in genres" :key="genre.genre_id" :value="genre.genre_id">
              {{ genre.name }}
            </option>
        </select>
      </div>
    </div>

    <div v-if="isAuthenticated" class="auth-options">
      <p class="auth-switch">
        Welcome back! 
        <button @click="logout" class="logout-button">Logout</button>
      </p>
    </div>
    <div v-else class="auth-switch">
      Don't have an account? 
      <router-link to="/register" class="auth-link">Register here</router-link>
      Or
      Already have an account? 
      <router-link to="/login" class="auth-link">Login here</router-link>
    </div>

    <div v-if="isLoading" class="loader">Loading...</div>

    <div v-if="movies && movies.length" class="results-container">
      <h2 class="results-title">Results</h2>
      <ul v-if="movies.length" class="movies-list">
        <li v-for="movie in movies" :key="movie.imdbID" class="movie-item">
          <!-- <div class="movie-info">
            <template v-if="movie.poster_url != null">
              <a :href="tmdbUrl" :movie="movie" target="_blank" rel="noopener noreferrer">
                <img v-if="movie.poster_url && movie.poster_url.trim() !== null" :src="movie.poster_url" alt="Movie poster">
              </a>
            </template>
            <template v-else>
              <i class="bi bi-image" style="font-size: 100px;"></i>
            </template>
            <h5 class="movie-title">{{ movie.original_title }}</h5>
            <p>{{ movie.release_date }}</p>
            <button 
              @click="viewDetails(movie.id)" 
              class="details-button"
              >
              View Details
            </button>
          </div> -->
          <movie-component :movie="movie"></movie-component>
        </li>
      </ul>
      <p v-else-if="!movies.length && yearErrorMessage && hasSearched || hasSearched && errorMessage">{{ errorMessage }}</p>

      <div class="pagination-buttons">
        <button v-if="page > 1" @click="prevPage" class="page-button">Previous</button>
        <button v-if="hasMorePages" @click="nextPage" class="page-button">Next</button>
      </div>
    </div>
    <div v-if="errorMessage" class="results-container">
      <h2 class="results-title">Results</h2>
      <p class="error">
        {{ errorMessage }}
      </p>
    </div>
    <p v-if="yearErrorMessage" class="error">
      {{ yearErrorMessage }}
    </p>
  </div>
</template>
  
<script>
  import axios from '@/axios';
  import MovieComponent from './MovieComponent';
  import { AuthService } from '@/utils/auth';
  import { API_CONFIG } from '@/config';
  
  export default {
    data() {
      return {
        query: '',
        movies: [],
        genres: [],
        filters: {
            year: '',
            rating: '',
            genre: ''
        },
        page: 1,
        hasMorePages: false,
        hasPreviousPage: false,
        isAuthenticated: AuthService.isAuthenticated(),
        isLoading: false,
        errorMessage: null,
        yearError: false,
        yearErrorMessage: '',
        currentYear: new Date().getFullYear(),
        hasSearched: false,
      };
    },
    components: {
      MovieComponent
    },
    props: {
      movie: Object,
    },
    computed: {
      hasActiveFilters() {
        return this.query.trim() || this.filters.rating || this.filters.year || this.filters.genre;
      },
      tmdbUrl() {
        console.log(this.movie);
        return `${API_CONFIG.tmdbMovie}${this.movie}`;
      },
    },
    mounted() {
        this.getGenres();
    },
    methods: {
      async searchMovies() {
        console.log(this.yearErrorMessage);
        this.movies = [];
        this.errorMessage = null;
        this.yearErrorMessage = '';
        this.hasSearched = true;
        this.isLoading = true;
        console.log(this.filters.year);

        const params = Object.fromEntries(
          Object.entries({
            q: this.query,
            page: this.page || 1,
            page_size: 10,
            rating: this.filters.rating,
            year: this.filters.year && this.filters.year.length === 4 ? this.filters.year : '',
            genre: this.filters.genre
          }).filter(([, value]) => value !== null && value !== '')
        );
        console.log(params);

        try {
          const response = await axios.get(`movies/search/`, { params });
          console.log(response);
          this.movies = response?.data?.movies;
          this.hasMorePages = this.movies.length > 0;
          if (!this.movies && (this.filters.year || this.query || this.filters.genre || this.filters.rating) || response.error) {
            this.errorMessage = "There are no movies available";
            console.log(this.errorMessage);
          }
        } catch (error) {
          console.error('Error fetching movies:', error);
          this.errorMessage = "There are no movies available";
        } finally {
          this.isLoading = false;
        }
      },
      async nextPage() {
        this.page += 1;
        await this.searchMovies();
      },
      async prevPage() {
        this.page -= 1;
        await this.searchMovies();
      },
      async getGenres() {
        try {
          const response = await axios.get('genres/');
          this.genres = response.data;
        } catch (error) {
          console.error('Error loading genres:', error);
        }
      },
      viewDetails(movie_id) {
        //this.$router.push({ name: 'MovieDetail', params: { movie_id } });
        window.open(`/movies/${movie_id}`, '_blank');
      },
      logout() {
        AuthService.logout();
        this.isAuthenticated = false;
        this.$router.push({ name: 'LoginForm' });
      },
      getImageUrl(poster_path) {
        if (poster_path != null) {
            return '<img :src="movie.poster_path" alt="Movie poster">'
        } else {
            return '<i class="bi bi-image"></i>';
        }
      },
      formatDate(dateString) {
        if (!dateString) return '';
        const date = new Date(dateString);
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return date.toLocaleDateString('en-US', options);
      },
      limitYearDigits() {
        const year = this.filters.year;
        const yearString = this.filters.year.toString();
        if (year && yearString.length >= 4) {
          this.filters.year = yearString.slice(0, 4);
        }
      },
      handleSearch() {
        this.validateYear();
        //const year = this.filters.year ? this.filters.year.toString() : '';

        if (!this.yearErrorMessage) {
          this.searchMovies();
        }
      },
      validateYear() {
        //const currentYear = new Date().getFullYear();
        const minYear = 1882;
        const year = this.filters.year;
        console.log(year);
        this.yearErrorMessage = '';

        if (year && (parseInt(year) < minYear || year.length !== 4)) {
          this.yearErrorMessage = `Please enter a valid 4-digit min year ${minYear}.`;
          this.filters.year = '';
        }
      },
      applyFilter() {
        this.page = 1;
        this.searchMovies();
      }
    },
    watch: {
      filters: {
        handler() {
          this.page = 1;
          //this.searchMovies();
        },
        deep: true
      }
    },
  };
</script>
  
<style scoped>
.error {
  color: red;
}

.search-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
}

.search-input {
  width: 350px;
  padding: 12px;
  margin-bottom: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
  font-size: 16px;
}

.search-button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.search-button:hover {
  background-color: #45a049;
}

.search-button:disabled {
  cursor: not-allowed;
  background-color: #ccc;
  color: #666;
}

.search-button:disabled:hover {
  background-color: #ccc;
}

.results-container {
  margin-top: 30px;
  text-align: center;
  width: 80%;
}

.results-title {
  font-size: 28px;
  margin-bottom: 20px;
  color: #333;
}

.movies-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(236px, 1fr));
  grid-gap: 20px;
  padding: 0;
  list-style: none;
}

.movie-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.movie-poster {
  width: 150px;
  height: 220px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 15px;
}

.movie-info {
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}

.movie-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
  text-align: center;
  flex-grow: 1;
}

.movie-info img,
.movie-info i.bi-image {
  height: 200px;
  object-fit: cover;
}

.movie-info i.bi-image {
  font-size: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: gray;
}

.details-button {
  margin-top: auto;
  padding: 5px 10px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  align-self: center
}

.details-button:hover {
  background-color: #0b7dda;
}

.pagination-buttons {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

.page-button {
  padding: 10px 15px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin: 0 10px;
}

.page-button:hover {
  background-color: #45a049;
}

.filters {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  gap: 20px;
}

.filter-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.filter-label {
  font-size: 14px;
  margin-bottom: 5px;
  color: #555;
}

.filter-input, .filter-select {
  padding: 10px;
  border: 2px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  width: 150px;
  transition: border-color 0.3s;
}

.filter-input:focus, .filter-select:focus {
  border-color: #4CAF50;
  outline: none;
}

.auth-options {
  margin-top: 20px;
  text-align: center;
}

.logout-button {
  padding: 10px 20px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
}

.logout-button:hover {
  background-color: #e53935;
}

.auth-options {
  margin-top: 20px;
  text-align: center;
}

.auth-switch {
  margin-top: 20px;
  text-align: center;
}

.auth-link {
  color: #2196F3;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s;
}

.auth-link:hover {
  color: #0b7dda;
}

.loader {
  margin: 20px 0;
  font-size: 18px;
  color: #333;
}
</style>
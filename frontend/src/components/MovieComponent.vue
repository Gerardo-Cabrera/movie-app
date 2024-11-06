<template>
    <div class="movie-info">
        <template v-if="movie.poster_url != null">
            <a @click.prevent="viewDetails" target="_blank" rel="noopener noreferrer">
                <img v-if="movie.poster_url && movie.poster_url.trim() !== null" :src="movie.poster_url" alt="Movie poster" loading="lazy">
            </a>
        </template>
        <template v-else>
            <i class="bi bi-image" style="font-size: 100px;"></i>
        </template>
        <h5 class="movie-title" @click="viewDetails" >
            {{ movie.original_title }}
        </h5>
        <p>
            {{ movie.release_date }}
        </p>
        <button 
            @click="viewDetails" 
            class="details-button">
            View Details
        </button>
    </div>
</template>
  
<script>
    export default {
        props: {
            movie: Object
        },
        methods: {
            generateSlug(title) {
                return title
                .toLowerCase()                 // Convert to lower
                .replace(/&/g, 'and')          // Replace the ampersand (&)
                .replace(/[^\w\s]/g, '')       // Delete special chars
                .replace(/\s+/g, '-')          // Replace spaces with hyphens
                .trim();                       // Remove spaces at the ends
            },
            viewDetails() {
                console.log(this.movie.id);

                // Navigation with Vue Router using slug in URL
                const slug = this.generateSlug(this.movie.original_title);
                const routeData = this.$router.resolve({
                    name: 'MovieDetail',                                                // Make sure you have a route with this name in Vue Router
                    params: { movie_id: this.movie.id, slug: slug ? slug : undefined }  // Passes both the ID and the slug to the route data object
                });
                console.log(routeData);
                window.open(routeData.href, '_blank');                                  // Open the details page
            }
        }
    };
</script>
  
<style scoped>
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
        cursor: pointer;
    }

    .movie-title:hover {
        color: #2596be;
    }

    .movie-info img,
    .movie-info i.bi-image {
        height: 200px;
        object-fit: cover;
        cursor: pointer;
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
</style>
  
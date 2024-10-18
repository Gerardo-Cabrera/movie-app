# movies/views.py
import requests
from django.http import JsonResponse
from django.conf import settings
from decouple import config
from .models import Genre, Movie, Favorite, Review, CustomUser
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.utils.text import slugify
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import GenreSerializer, MovieSerializer
from datetime import datetime
from urllib.parse import urlencode

def search_movies(request):
    api_token = config('API_TOKEN_TMDB')

    query = request.GET.get('q', '')
    page = request.GET.get('page', 1)
    rating = request.GET.get('rating', None)
    year = request.GET.get('year', None)
    genre = request.GET.get('genre', None)

    params = {k: v for k, v in {
        'query': query if query else None,
        'page': page,
        'rating': rating,
        'year': year,
        'with_genres': genre
    }.items() if v is not None}

    api_url = config('API_URL_TMDB_SEARCH_MOVIE') if query else config('API_URL_TMDB_DISCOVER_MOVIE')
    url = f"{api_url}?{urlencode(params)}"

    headers = {
        "accept": config('HEADERS_ACCEPT'),
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    if data.get('total_results') == 0:
        return JsonResponse({'error': 'Movie not found'}, status=404)
    
    movies = data.get('results', [])

    poster_url = config('POSTER_URL_TMDB')
    filtered_movies = movie_filter(movies, genre, rating, year)
    
    for movie in movies:
        if movie.get('poster_path'):
            movie['poster_url'] = f"{poster_url}{movie.get('poster_path', '')}"

        if movie.get('release_date'):
            movie['release_date'] = datetime.strptime(movie['release_date'], "%Y-%m-%d").strftime("%B %d, %Y")

    return JsonResponse({
        'movies': filtered_movies,
        'total_results': data.get('total_results', 0),
        'current_page': page
    }, safe=False)

def movie_filter(movies, genre=None, rating=None, year=None):
    filtered_movies = movies

    filters = [
        lambda movie: int(genre) in movie.get('genre_ids', []) if genre else True,
        lambda movie: float(movie.get('vote_average', 0)) >= float(rating) if rating else True,
        lambda movie: movie.get('release_date', '').startswith(str(year)) if year else True
    ]

    for filter_func in filters:
        filtered_movies = [movie for movie in movies if filter_func(movie)]
    
    return filtered_movies

def movie_detail(request, movie_id, slug=None):
    print("Movie ID: ", movie_id)
    print("Slug: ", slug)
    try:
        api_token = config('API_TOKEN_TMDB')
        api_url = config('API_URL_TMDB_MOVIE_DETAIL')
        url = f'{api_url}{movie_id}'
        headers = {
            "accept": config('HEADERS_ACCEPT'),
            "Authorization": f"Bearer {api_token}"
        }
        response = requests.get(url, headers=headers)
        data = response.json() # Parse the JSON response
        
        movie, _ = Movie.objects.get_or_create(
            movie_id = data['id'],
            defaults = {
                'title': data['original_title'],
                'date': data['release_date'],
                'popularity': data['popularity'],
                'poster_path': data['poster_path'] if data['poster_path'] else None,
            }
        )

        genres = data['genres']
        for genre_data in genres: # Get the list of genres 
            genre_id = genre_data['id']
            genre_name = genre_data['name']
            genre, _ = Genre.objects.get_or_create(genre_id=genre_id,name=genre_name)
            movie.genre.add(genre)

        if not movie.slug:
            movie.slug = slugify(movie.title.lower().replace('&', 'and'))
            movie.save()

        movie_serialized = MovieSerializer(movie)                     # Serialize the movie object
        return JsonResponse(movie_serialized.data)                    # Return the serialized data as a JSON response
    except Movie.DoesNotExist:                                        # If the movie does not exist in the database, return a 404 error
        return JsonResponse({'error': 'Movie not found'}, status=404) # Return a 404 error response

@api_view(['POST'])
def register(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if len(password) < 8:
        return Response({'detail': 'Password must be at least 8 characters long'}, status=status.HTTP_400_BAD_REQUEST)

    if CustomUser.objects.filter(email=email).exists():
        return Response({'detail': 'Email already exists'}, status=status.HTTP_409_CONFLICT)

    user = CustomUser.objects.create_user(email=email, password=password)
    refresh = RefreshToken.for_user(user)

    return Response({
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    })

@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    user = authenticate(username=email, password=password)

    if user is None:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)

    return Response({
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_favorite(request, movie_id):
    user = request.user
    try:
        movie = Movie.objects.get(movie_id=movie_id)
        is_favorite = Favorite.objects.filter(user=user, movie=movie).exists()

        return Response({'is_favorite': is_favorite}, status=200)
    except Movie.DoesNotExist:
        return Response({'error': 'Movie not found'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite(request, movie_id):
    user = request.user
    try:
        movie = Movie.objects.get(movie_id=movie_id)
        _, created = Favorite.objects.get_or_create(user=user, movie=movie)

        if not created:
            return Response({'message': 'Movie is already in favorites!'}, status=409)
        
        return Response({'message': 'Movie added to favorites!'}, status=200)
    except Movie.DoesNotExist:
        return Response({'error': 'Movie not found'}, status=404)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_favorite(request, movie_id):
    user = request.user
    try:
        movie = Movie.objects.get(movie_id=movie_id)
        favorite = Favorite.objects.filter(user=user, movie=movie)

        if favorite.exists():
            favorite.delete()
            return Response({'message': 'Movie removed from favorites!'}, status=200)
        else:
            return Response({'message': 'Movie not in favorites!'}, status=400)
    except Movie.DoesNotExist:
        return Response({'error': 'Movie not found'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request, imdb_id):
    user = request.user
    try:
        movie = Movie.objects.get(imdb_id=imdb_id)
        content = request.data.get('content')
        rating = request.data.get('rating')

        if Review.objects.filter(user=user, movie=movie).exists():
            return Response({'message': 'You have already reviewed this movie!'}, status=status.HTTP_409_CONFLICT)
        
        Review.objects.create(user=user, movie=movie, content=content, rating=rating)
        return Response({'message': 'Review submitted!'}, status=200)
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'}, status=404)

class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class MoviePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class MovieListView(generics.ListAPIView):
    serializer_class = MovieSerializer
    pagination_class = MoviePagination

    def get_queryset(self):
        queryset = Movie.objects.all()
        genre = self.request.query_params.get('genre', None)
        if genre:
            queryset = queryset.filter(genres__id=genre)
        return queryset
    
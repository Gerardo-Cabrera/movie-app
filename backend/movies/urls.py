# movies/urls.py
from django.urls import path
from .views import search_movies, movie_detail, login_user, check_favorite, add_favorite, remove_favorite, add_review, register, GenreListView


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login_user'),
    path('movies/search/', search_movies, name='search_movies'),
    path('movies/detail/<str:movie_id>/', movie_detail, name='movie_detail'),
    path('movies/detail/<str:movie_id>/<slug:slug>/', movie_detail, name='movie_detail'),
    path('movies/favorites/<str:movie_id>/', check_favorite, name='check_favorite'),
    path('movies/favorites/add/<str:movie_id>/', add_favorite, name='add_favorite'),
    path('movies/favorites/remove/<str:movie_id>/', remove_favorite, name='remove_favorite'),
    path('movies/review/<str:movie_id>/', add_review, name='add_review'),
    path('genres/', GenreListView.as_view(), name='genre-list'),
]

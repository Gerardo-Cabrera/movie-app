# movies/serializers.py
from rest_framework import serializers
from .models import Genre, Movie

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre_id', 'name']

class MovieSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['movie_id', 'title', 'date', 'popularity', 'poster_path', 'genre']
from rest_framework import serializers
from .models import Movie

class MovieListSerializer(serializers.ModelSerializer):
    """
    영화 목록 조회용 Serializer (간단한 정보만 포함)
    """
    class Meta:
        model = Movie
        fields = ['id', 'movie_title', 'movie_genre', 'movie_rating', 'poster_url','technologies']

class MovieDetailSerializer(serializers.ModelSerializer):
    """
    영화 상세 정보 조회용 Serializer (모든 정보 + 연관 기술 포함)
    """

    class Meta:
        model = Movie
        fields = [
            'id',
            'movie_title',
            'movie_genre',
            'movie_synopsis',
            'movie_rating',
            'technologies',
            'poster_url'
        ]
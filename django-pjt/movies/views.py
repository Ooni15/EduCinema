from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import Movie
from .serializers import MovieListSerializer, MovieDetailSerializer

@api_view(['GET'])
@permission_classes([AllowAny])  # 명시적으로 모든 접근 허용
def movie_list(request):
    """
    전체 영화 목록 조회 (간단한 정보만 포함)
    """
    movies = Movie.objects.all()
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])  # 명시적으로 모든 접근 허용
def movie_detail(request, movie_pk):
    """
    특정 영화 상세 정보 조회 (연관 기술 포함)
    """
    try:
        movie = Movie.objects.get(pk=movie_pk)
    except Movie.DoesNotExist:
        return Response(
            {'error': '영화를 찾을 수 없습니다.'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = MovieDetailSerializer(movie)
    return Response(serializer.data)

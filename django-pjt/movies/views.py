from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Movie
from .serializers import MovieListSerializer, MovieDetailSerializer

@api_view(['GET'])
def movie_list(request):
    """
    전체 영화 목록 조회 (간단한 정보만 포함)
    """
    movies = Movie.objects.all()
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
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

# from rest_framework import viewsets
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from .models import Movie, Technology
# from .serializers import MovieSerializer, TechnologySerializer

# class TechnologyViewSet(viewsets.ModelViewSet):
#     queryset = Technology.objects.all()
#     serializer_class = TechnologySerializer

#     def create(self, request, *args, **kwargs):
#         # 이미 존재하는 기술인지 확인
#         name = request.data.get('name')
#         technology, created = Technology.objects.get_or_create(
#             name=name,
#             defaults={'description': request.data.get('description', '')}
#         )
#         serializer = self.get_serializer(technology)
#         return Response(serializer.data)

# class MovieViewSet(viewsets.ModelViewSet):
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer

#     @action(detail=True, methods=['post'])
#     def add_technology(self, request, pk=None):
#         movie = self.get_object()
#         technology_id = request.data.get('technology_id')
        
#         try:
#             technology = Technology.objects.get(id=technology_id)
#             movie.technologies.add(technology)
#             return Response({'status': 'technology added'})
#         except Technology.DoesNotExist:
#             return Response({'error': 'Technology not found'}, status=400)
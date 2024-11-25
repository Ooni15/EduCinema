from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Like
from .serializers import LikeSerializer
from articles.models import Article

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def likes_list(request):
    if request.method == 'GET':
        likes = Like.objects.all()
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        article_id = request.data.get('article')
        article = get_object_or_404(Article, pk=article_id)
        like, created = Like.objects.get_or_create(
            user=request.user,
            article=article
        )
        if created:
            return Response({'detail': 'Like created'}, status=status.HTTP_201_CREATED)
        like.delete()
        return Response({'detail': 'Like removed'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def likes_detail(request, like_pk):
    like = get_object_or_404(Like, pk=like_pk)
    
    if request.method == 'GET':
        serializer = LikeSerializer(like)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        if request.user != like.user:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def article_likes(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    likes = Like.objects.filter(article=article)
    likes_count = likes.count()
    is_liked = likes.filter(user=request.user).exists()
    
    return Response({
        'likes_count': likes_count,
        'is_liked': is_liked
    })
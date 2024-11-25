from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Article
from .serializers import ArticleSerializer, ArticleListSerializer
from comments.models import Comment
from comments.serializers import CommentSerializer
from likes.models import Like

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()  # user를 여기서 전달하지 않음
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        data = serializer.data
        # 댓글 정보 추가
        comments = Comment.objects.filter(article=article)
        comment_serializer = CommentSerializer(comments, many=True)
        data['comments'] = comment_serializer.data
        # 좋아요 정보 추가
        likes_count = Like.objects.filter(article=article).count()
        is_liked = Like.objects.filter(article=article, user=request.user).exists()
        data['likes_count'] = likes_count
        data['is_liked'] = is_liked
        return Response(data)

    elif request.method == 'PUT':
        if request.user != article.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ArticleSerializer(article, data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        if request.user != article.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def article_comments(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, article=article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def article_likes(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    like, created = Like.objects.get_or_create(
        user=request.user,
        article=article
    )
    
    if not created:
        like.delete()
        return Response({'detail': 'unliked'}, status=status.HTTP_200_OK)
    
    return Response({'detail': 'liked'}, status=status.HTTP_201_CREATED)
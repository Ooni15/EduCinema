from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Article, Movie
from .serializers import ArticleSerializer, ArticleListSerializer, MovieSerializer
from comments.models import Comment
from comments.serializers import CommentSerializer
from likes.models import Like
from django.conf import settings
from openai import OpenAI

# 랑운 user_articles profile용 만들어가유~
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_articles(request, user_id):
    articles = Article.objects.filter(user_id=user_id)
    serializer = ArticleListSerializer(articles, many=True)
    return Response(serializer.data)

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

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_comments(request, article_pk):
    if request.method == 'GET':
        comments = Comment.objects.filter(article_id=article_pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article_id=article_pk, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
def article_comment(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, article_id=article_pk)
    
    if request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_article_recommendations(request):
    user_major = request.data.get('user_major')
    
    # movies.json에서 전공 관련 기술을 가진 영화들 필터링
    movies = Movie.objects.all()
    related_movies = []
    
    for movie in movies:
        if user_major.lower() in movie.technologies.lower():
            related_movies.append(movie)
    
    # 관련 영화들의 기술 정보 수집
    movie_technologies = [movie.technologies for movie in related_movies[:3]]
    
    prompt = (
        f"전공: {user_major}\n"
        f"관련 기술: {', '.join(movie_technologies)}\n\n"
        f"위 전공을 가진 교사가 영화에 등장하는 기술을 활용하여 교육 자료나\n"
        f"수업 계획을 작성할 수 있는 아이디어를 3가지 제안해주세요.\n"
    )
    
    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "당신은 교육 전문가입니다. 영화에 등장하는 기술을 활용하여 효과적인 교육 방법을 제안합니다."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        recommendations = response.choices[0].message.content
        
        return Response({
            'recommendations': recommendations,
            'related_movies': MovieSerializer(related_movies, many=True).data
        })
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=500)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def article_gpt_query(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    user_query = request.data.get('user_query')
    
    prompt = (
        f"Article content: {article.content}\n\n"
        f"User question: {user_query}\n\n"
        "Answer:"
    )
    
    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers questions based on the given article content."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        answer = response.choices[0].message.content
        
        return Response({'answer': answer})
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=500)
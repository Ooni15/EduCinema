from rest_framework import serializers
from articles.models import Article
from movies.models import Movie
from accounts.models import User
from comments.models import Comment
from likes.models import Like

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'major', 'profile_picture', 'major']

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'movie_title', 'movie_genre', 'poster_url']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']

class ArticleListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'user', 'movie', 'created_at', 'comments_count', 'likes_count']

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_likes_count(self, obj):
        return obj.likes.count()
    
class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'user', 'movie', 
                 'created_at', 'updated_at', 'comments', 
                 'likes_count', 'is_liked', 'related_major', 
                 'movie_description', 'technology_type']

    def get_likes_count(self, obj):
        return Like.objects.filter(article=obj).count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(
                article=obj, 
                user=request.user
            ).exists()
        return False

    def create(self, validated_data):
        try:
            movie_id = self.context['request'].data.get('movie')
            movie = Movie.objects.get(id=movie_id)
            user = self.context['request'].user
            
            # validated_data에서 user와 movie 필드 제외
            if 'user' in validated_data:
                validated_data.pop('user')
            if 'movie' in validated_data:
                validated_data.pop('movie')
                
            article = Article.objects.create(
                user=user,
                movie=movie,
                **validated_data
            )
            return article
        except Movie.DoesNotExist:
            raise serializers.ValidationError({"movie": "Movie not found"})
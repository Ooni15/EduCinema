from rest_framework import serializers
from .models import Comment
from django.contrib.auth import get_user_model

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_major = serializers.CharField(source='user.major', read_only=True)
    
    class Meta:
        model = Comment
        fields = [
            'id', 
            'content', 
            'article', 
            'username',
            'user_major', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']
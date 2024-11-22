from django.conf import settings  # settings를 import
from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework import serializers
from .models import ProfileComment, UserLike

class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    major = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

class UserLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLike
        fields = ['id', 'user', 'liked_user', 'created_at']


class ProfileCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ProfileComment
        fields = ['id', 'username', 'content', 'created_at', 'updated_at']

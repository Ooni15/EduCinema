from rest_framework import serializers
from .models import Like

class LikeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Like
        fields = [
            'id', 
            'article', 
            'username', 
            'created_at'
        ]
        read_only_fields = ['user', 'created_at']
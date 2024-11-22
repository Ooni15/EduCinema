from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from accounts.models import User
from rest_framework.authtoken.models import Token
from articles.models import Article  # Post 모델 가져오기
from .models import ProfileComment, UserLike


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_picture', 'major', 'bio']

class CustomRegisterSerializer(RegisterSerializer):
    major = serializers.CharField(required=True)  # 추가 필드
    profile_picture = serializers.ImageField(required=False)  # 프로필 사진 필드 (선택적)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['major'] = self.validated_data.get('major', '')  # major 필드 추가
        data['profile_picture'] = self.validated_data.get('profile_picture', None)  # profile_picture 필드 추가
        return data

    def save(self, request):
        user = super().save(request)
        user.major = self.validated_data.get('major', '')  # major 저장
        user.profile_picture = self.validated_data.get('profile_picture', None)  # profile_picture 저장
        user.save()  # 데이터 저장
        Token.objects.get_or_create(user=user)  # 토큰 생성
        return user


class UserLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLike
        fields = ['id', 'user', 'liked_user', 'created_at']


class ProfileCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ProfileComment
        fields = ['id', 'username', 'content', 'created_at', 'updated_at']

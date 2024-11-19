from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from accounts.models import User
from rest_framework.authtoken.models import Token
from articles.models import Article  # Post 모델 가져오기



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_picture', 'major', 'bio']

class CustomRegisterSerializer(RegisterSerializer):
    major = serializers.CharField(required=True)  # 추가 필드 예시

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['major'] = self.validated_data.get('major', '')  # major 필드 추가
        return data

    # def save(self, request):
    #     user = super().save(request)  # 사용자 생성
    #     # 사용자 생성 후 Post 자동 생성
    #     Article.objects.create(
    #         user=user,
    #         title=f"Welcome {user.username}!",
    #         content=f"{user.username}님이 가입했습니다.",
    #         related_major=user.major
    #     )
    #     Token.objects.get_or_create(user=user)  # 자동으로 토큰 생성
    #     return user

    def save(self, request):
        user = super().save(request)
        Article.objects.create(
            user=user,
            title=f"Welcome {user.username}!",
            content=f"{user.username}님이 가입했습니다.",
            related_major=user.major,
            movie_description="가입을 축하합니다!",
            technology_type="General",
            learning_material_url="",
            short_description="환영합니다!"
        )
        Token.objects.get_or_create(user=user)
        return user

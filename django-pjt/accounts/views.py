from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import CustomRegisterSerializer, UserSerializer
from rest_framework.authtoken.models import Token

# 사용자 목록 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def user_list(request):
    # print(f"Headers: {request.META}")
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# 회원가입
@api_view(['POST'])
@permission_classes([AllowAny])  # 인증 없이 접근 가능
def signup(request):
    serializer = CustomRegisterSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save(request)
        # 토큰 생성 및 반환
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "major": user.major,
            "bio": user.bio,
            "profile_picture": user.profile_picture.url if user.profile_picture else None,  # URL 반환
            "token": token.key  # 반환된 토큰 추가
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 사용자 상세 조회, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def user_detail(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)  # User 객체를 가져옴

    if request.method == 'GET':
        serializer = UserSerializer(user)  # UserSerializer 사용
        return Response(serializer.data)

    elif request.method == 'PUT':
        if request.user.pk != user.pk:  # 자신의 데이터만 수정 가능
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(user, data=request.data)  # UserSerializer 사용
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        if not request.user.is_staff:  # 관리자인 경우에만 삭제 가능
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
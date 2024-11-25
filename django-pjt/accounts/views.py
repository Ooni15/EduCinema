from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import User, UserLike, ProfileComment
from .serializers import CustomRegisterSerializer, UserSerializer, ProfileCommentSerializer, UserLikeSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate



# 로그인
@api_view(['POST'])
@permission_classes([AllowAny])  # 인증 없이 접근 가능
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is not None:
        # 로그인 성공
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'email': user.email,
            'major': user.major,
            'bio': user.bio,
            'profile_picture': user.profile_picture.url if user.profile_picture else None
        }, status=status.HTTP_200_OK)
    else:
        # 로그인 실패
        return Response({'error': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)

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

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def logout(request):
    try:
        # 현재 사용자와 연결된 토큰 삭제
        request.user.auth_token.delete()
        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# 사용자 목록 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def user_list(request):
    # print(f"Headers: {request.META}")
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

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



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, user_id):
    try:
        if request.user.id == user_id:
            return Response({'error': '자기 자신을 좋아요할 수 없습니다.'}, status=400)
        
        liked_user = User.objects.get(id=user_id)
        user_like, created = UserLike.objects.get_or_create(user=request.user, liked_user=liked_user)
        if not created:
            user_like.delete()
            return Response({'message': '좋아요 취소 완료'}, status=200)
        return Response({'message': '좋아요 완료'}, status=201)
    except User.DoesNotExist:
        return Response({'error': '존재하지 않는 사용자입니다.'}, status=404)



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def profile_comments(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    
    if request.method == 'GET':
        # 특정 사용자의 프로필에 달린 모든 댓글 조회
        comments = ProfileComment.objects.filter(target_user=target_user)
        serializer = ProfileCommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # 항상 새 댓글을 생성
        serializer = ProfileCommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user, target_user=target_user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def profile_comment_detail(request, comment_id):
    comment = get_object_or_404(ProfileComment, id=comment_id)

    # 수정 요청
    if request.method == 'PUT':
        if comment.user != request.user:
            return Response({'error': '권한이 없습니다.'}, status=403)
        serializer = ProfileCommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # 삭제 요청
    elif request.method == 'DELETE':
        if comment.user != request.user:
            return Response({'error': '권한이 없습니다.'}, status=403)
        comment.delete()
        return Response({'message': '댓글이 삭제되었습니다.'}, status=204)

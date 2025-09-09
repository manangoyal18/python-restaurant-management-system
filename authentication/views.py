from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from .models import User
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserSerializer,
    UserUpdateSerializer,
    PasswordChangeSerializer
)


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens for the new user
        refresh = RefreshToken.for_user(user)
        user.token = str(refresh.access_token)
        user.refresh_token = str(refresh)
        user.save()
        
        user_data = UserSerializer(user).data
        
        return Response({
            'success': True,
            'message': 'User registered successfully',
            'user': user_data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        }, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # Generate new tokens
        refresh = RefreshToken.for_user(user)
        user.token = str(refresh.access_token)
        user.refresh_token = str(refresh)
        user.save()
        
        user_data = UserSerializer(user).data
        
        return Response({
            'success': True,
            'message': 'Login successful',
            'user': user_data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        }, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            user.token = None
            user.refresh_token = None
            user.save()
            
            return Response({
                'success': True,
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            # Update user's token in database
            refresh_token = request.data.get('refresh')
            try:
                refresh = RefreshToken(refresh_token)
                user = User.objects.get(id=refresh['user_id'])
                user.token = response.data['access']
                user.save()
            except:
                pass
                
        return response


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_users(request):
    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('recordPerPage', 10))
        
        users = User.objects.all()
        total_count = users.count()
        
        # Pagination
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_users = users[start_index:end_index]
        
        users_data = UserSerializer(paginated_users, many=True).data
        
        return Response({
            'success': True,
            'total_count': total_count,
            'users': users_data,
            'page': page,
            'per_page': per_page
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Error occurred while fetching users',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_user(request, user_id):
    try:
        user = get_object_or_404(User, user_id=user_id)
        user_data = UserSerializer(user).data
        
        return Response({
            'success': True,
            'user': user_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Error occurred while fetching user',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_data = UserSerializer(request.user).data
        return Response({
            'success': True,
            'user': user_data
        }, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        user_data = UserSerializer(user).data
        
        return Response({
            'success': True,
            'message': 'Profile updated successfully',
            'user': user_data
        }, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data, 
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'success': True,
            'message': 'Password changed successfully'
        }, status=status.HTTP_200_OK)

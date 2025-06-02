from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserSerializer,
    UserProfileUpdateSerializer,
    PasswordChangeSerializer
)

class RegisterView(generics.CreateAPIView):
    """
    User registration endpoint
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens for the new user
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'User created successfully',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

class LoginView(TokenObtainPairView):
    """
    User login endpoint using JWT tokens
    """
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    """
    User logout endpoint - blacklist the refresh token
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({
                    'message': 'Logout successful'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Refresh token is required'
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)

class RefreshTokenView(TokenRefreshView):
    """
    Token refresh endpoint
    """
    permission_classes = [AllowAny]

class ProfileView(APIView):
    """
    User profile view - GET and PUT
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get user profile information
        """
        user = request.user
        user_data = UserSerializer(user).data
        
        return Response({
            'user': user_data
        }, status=status.HTTP_200_OK)
    
    def put(self, request):
        """
        Update user profile information
        """
        user = request.user
        profile = user.profile
        
        # Update user basic information
        user_fields = ['first_name', 'last_name', 'email']
        for field in user_fields:
            if field in request.data:
                setattr(user, field, request.data[field])
        
        # Validate email uniqueness if changed
        if 'email' in request.data and request.data['email'] != user.email:
            if User.objects.filter(email=request.data['email']).exists():
                return Response({
                    'error': 'A user with this email already exists.'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        user.save()
        
        # Update profile information
        profile_serializer = UserProfileUpdateSerializer(
            profile, 
            data=request.data, 
            partial=True
        )
        
        if profile_serializer.is_valid():
            profile_serializer.save()
            
            return Response({
                'message': 'Profile updated successfully',
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'errors': profile_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class PasswordChangeView(APIView):
    """
    Change user password
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data, 
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Password changed successfully'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class UserListView(generics.ListAPIView):
    """
    List all users (for admin purposes)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Only superusers can see all users, regular users see only themselves
        """
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=user.id)

# Test view for development
@api_view(['GET'])
@permission_classes([AllowAny])
def test_auth_view(request):
    return Response({'message': 'Authentication app is working!'})

# apps/authentication/views.py